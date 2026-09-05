---
name: render-images-in-cursor
description: 'Reliably show images, renders, mockups, screenshots, or plots to the human user inside the Cursor app chat. Use whenever the user must SEE an image the agent generated or found, or when the user says they cannot see an image you sent. Differentiator: fixes the silent failure where images saved outside the open workspace never render in Cursor chat.'
---

# Render Images in Cursor

Cursor chat renders an image reliably only when the file lives INSIDE the open workspace. Image tools often save to folders outside it (for example an assets folder under the Cursor projects directory) and claim the image "is already displayed" — the user then sees nothing, with no error. Inline chat rendering is also a newer, rollout-dependent Cursor feature, so always add the editor-tab fallback.

## Workflow

1. **Copy the image into the open workspace.** Any workspace folder works; prefer the repo's temp folder:

```bash
mkdir -p tmp/mockups
cp "$IMAGE_PATH" tmp/mockups/my-image.png
```

2. **Embed it in the chat reply** with plain markdown pointing at the in-workspace file, using its full absolute path:

```markdown
![Short description](ABSOLUTE-WORKSPACE-PATH/tmp/mockups/my-image.png)
```

One embed per image, each on its own line, with a bold one-line label above it. Never trust an image tool's "already displayed" output — embed explicitly every time.

3. **Also open each image as an editor tab** — guaranteed visible even when inline chat rendering fails. With the cursor-app-control MCP server, call `open_resource`:

```text
uri = file://ABSOLUTE-WORKSPACE-PATH/tmp/mockups/my-image.png
```

The file URI must point inside the workspace (or under the user's .cursor folder). Without that MCP server, run `cursor tmp/mockups/my-image.png` from the workspace root instead.

4. **Verify with the user.** Ask whether the images are visible. If inline rendering failed, the editor tabs from step 3 are the fallback — do not just resend the same markdown.

## Failure modes

- Image saved outside the workspace: chat renders nothing, silently. Copy it into the workspace first (step 1) and embed the in-workspace path.
- Markdown renders as a plain file link, not a picture: the user's Cursor build lacks inline chat images; rely on the editor tabs from step 3.
- `open_resource` rejects the URI: the file is outside the workspace; fix the path via step 1.
- macOS `open` shows the image in Preview, outside Cursor — last resort only.
