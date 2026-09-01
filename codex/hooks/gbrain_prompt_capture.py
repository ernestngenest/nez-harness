#!/usr/bin/env python3

import base64
import datetime
import hashlib
import json
import re
import subprocess
import sys

MAX_PROMPT_CHARS = 20_000
LOG_FILE = "/Users/tokshichiko/.codex/gbrain-sync/prompt-capture.log"
REMOTE_HOST = "root@43.133.142.103"
GBRAIN_BIN = "/usr/local/bin/gbrain"
SSH_ARGS = (
    "-o", "BatchMode=yes",
    "-o", "IdentitiesOnly=yes",
    "-o", "ConnectTimeout=15",
    "-i", "/Users/tokshichiko/.ssh/id_ed25519",
)
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN [^-]*PRIVATE KEY-----.*?-----END [^-]*PRIVATE KEY-----", re.DOTALL),
    re.compile(r"\b(?:sk|gh[pousr])[-_][A-Za-z0-9_-]{16,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b"),
    re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]{12,}"),
    re.compile(r"(?i)\b(?:api[_-]?key|token|password|secret|client[_-]?secret|authorization)\b\s*[:=]\s*[^\s,;]+"),
    re.compile(r"(?i)\b[a-z][a-z0-9+.-]*://[^/\s:@]+:[^@\s/]+@"),
)


def read_event():
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        return None
    if event.get("hook_event_name") != "UserPromptSubmit":
        return None
    return event


def redact_secrets(prompt):
    redacted_prompt = prompt[:MAX_PROMPT_CHARS]
    for pattern in SECRET_PATTERNS:
        redacted_prompt = pattern.sub("[REDACTED_SECRET]", redacted_prompt)
    return redacted_prompt


def build_payload(event):
    prompt = redact_secrets(event.get("prompt", "")).strip()
    if not prompt:
        return None
    return {
        "turn_text": prompt,
        "session_id": event.get("session_id"),
        "visibility": "private",
        "is_dream_generated": False,
    }


def encode_text(value):
    return base64.b64encode(value.encode("utf-8")).decode("ascii")


def build_extract_command(payload):
    payload_json = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    encoded_payload = encode_text(payload_json)
    return f'payload="$(printf %s \'{encoded_payload}\' | base64 -d)"; exec {GBRAIN_BIN} call extract_facts "$payload"'


def build_capture_slug(event, prompt):
    identity = f'{event.get("session_id")}:{event.get("turn_id")}:{prompt}'
    digest = hashlib.sha256(identity.encode("utf-8")).hexdigest()[:24]
    return f"codex-prompt-{digest}"


def build_capture_command(event, prompt):
    encoded_prompt = encode_text(prompt)
    slug = build_capture_slug(event, prompt)
    return f"printf %s '{encoded_prompt}' | base64 -d | {GBRAIN_BIN} capture --stdin --slug {slug} --type transcript --json"


def run_remote(command):
    return subprocess.run(
        ("/usr/bin/ssh", *SSH_ARGS, REMOTE_HOST, command),
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )


def summarize_capture_result(result):
    if result.returncode != 0:
        return f"failed exit={result.returncode}"
    try:
        response = json.loads(result.stdout)
    except json.JSONDecodeError:
        return "completed non_json_response"
    slug = str(response.get("slug", "unknown"))[:96]
    return f"completed slug={slug}"


def summarize_extract_result(result):
    if result.returncode != 0:
        return f"failed exit={result.returncode}"
    try:
        response = json.loads(result.stdout)
    except json.JSONDecodeError:
        return "completed non_json_response"
    counts = {key: value for key, value in response.items() if isinstance(value, int)}
    return f"completed counts={json.dumps(counts, separators=(',', ':'))}"


def run_remote_step(command, summarizer):
    try:
        return summarizer(run_remote(command))
    except subprocess.TimeoutExpired:
        return "failed timeout"


def capture_prompt(event, payload):
    command = build_capture_command(event, payload["turn_text"])
    return run_remote_step(command, summarize_capture_result)


def extract_prompt_facts(payload):
    command = build_extract_command(payload)
    return run_remote_step(command, summarize_extract_result)


def write_log(event, status):
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    session_id = str(event.get("session_id", "unknown"))[:64]
    turn_id = str(event.get("turn_id", "unknown"))[:64]
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(f"{timestamp} session={session_id} turn={turn_id} {status}\n")


def spawn_worker(event, payload):
    job = {
        "event": {
            "session_id": event.get("session_id"),
            "turn_id": event.get("turn_id"),
        },
        "payload": payload,
    }
    process = subprocess.Popen(
        (sys.executable, __file__, "--worker"),
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
        close_fds=True,
    )
    process.stdin.write(json.dumps(job, ensure_ascii=False).encode("utf-8"))
    process.stdin.close()


def hook_main():
    event = read_event()
    if event is None:
        return 0
    payload = build_payload(event)
    if payload is None:
        write_log(event, "skipped empty_prompt")
        return 0
    try:
        spawn_worker(event, payload)
    except OSError as error:
        write_log(event, f"failed_to_queue error={type(error).__name__}")
    return 0


def worker_main():
    try:
        job = json.load(sys.stdin)
        event = job["event"]
        payload = job["payload"]
        capture_status = capture_prompt(event, payload)
        extract_status = extract_prompt_facts(payload)
        write_log(event, f"capture={capture_status} facts={extract_status}")
    except (KeyError, OSError, subprocess.TimeoutExpired, json.JSONDecodeError) as error:
        write_log({}, f"failed error={type(error).__name__}")
    return 0


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--worker":
        return worker_main()
    return hook_main()


if __name__ == "__main__":
    raise SystemExit(main())
