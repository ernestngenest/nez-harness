# React Rules

```
❌ Don't                             ✅ Do
------------------------------------------------------
Heavy logic in JSX                   Extract to custom hook
Copy-paste logic across components   Extract custom hook useXxx()
> 200 lines per component            Split into sub-components
Props drilling > 2 levels            Use Context or state manager
useEffect for derived state          Use useMemo
Fetching directly in component       Use custom hook / React Query
Anonymous arrow functions in JSX     Use named functions
```

**Correct component structure:**
```tsx
import { ... }                       // 1. imports
interface Props { ... }              // 2. types

export function UserCard({ id, onSelect }: Props) {
  const { user, isLoading } = useUser(id)  // 3. hooks first

  if (isLoading) return <Skeleton />       // 4. early returns
  if (!user) return null

  const handleClick = () => onSelect(user.id)  // 5. handlers

  return <div onClick={handleClick}>{user.name}</div>  // 6. lean JSX
}
```

**Custom hook pattern:**
```tsx
// hooks/useUser.ts
export function useUser(id: string) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<Error | null>(null)

  useEffect(() => {
    fetchUser(id).then(setUser).catch(setError)
  }, [id])

  return { user, isLoading, error }
}
```

- Use **React Query / SWR** for data fetching, not manual `useEffect` + `fetch`
- Components only receive props they actually need
- Never put side effects in render body — always in `useEffect`
