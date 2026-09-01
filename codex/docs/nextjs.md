# Next.js Rules (App Router)

```
❌ Don't                             ✅ Do
------------------------------------------------------
Client fetch when server can do it   Use Server Components (RSC)
Logic in page.tsx                    Extract to components / hooks
Duplicate fetch logic across pages   Extract to lib/api/ or service
'use client' everywhere              Default to Server Component first
Hardcoded API URLs                   Use env vars + lib/api client
```

**Correct App Router structure:**
```
app/
├── (auth)/login/page.tsx            # Server Component by default
├── dashboard/
│   ├── page.tsx                     # fetch here (server)
│   └── _components/
│       ├── DashboardChart.tsx       # 'use client' only if interactive
│       └── StatsCard.tsx            # Server Component if static
lib/
├── api/users.ts                     # reusable fetch functions
├── utils/
└── types/
```

**Server vs Client Component:**
```tsx
// ✅ Server Component — fetch directly, no useState
export default async function DashboardPage() {
  const stats = await getStats()
  return <StatsCard data={stats} />
}

// ✅ Client Component — only when hooks/interactivity needed
'use client'
export function FilterBar({ onFilter }: Props) {
  const [query, setQuery] = useState('')
  return <input onChange={e => setQuery(e.target.value)} />
}
```

**Thin Route Handler:**
```ts
// ✅ Good
export async function GET(request: Request) {
  const users = await UserService.getAll()
  return Response.json(users)
}
```

**Data fetching hierarchy:**
```
Server Component   → direct fetch(), cache / revalidate
Route Handler      → mutations or external webhooks
React Query / SWR  → dynamic client-side data
Server Actions     → form submissions from Client Components
```

- Use `loading.tsx` and `error.tsx` per route segment
- Always `next/image` for images, `next/link` for links
- Always define `export const metadata` in `page.tsx`
