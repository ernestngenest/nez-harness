# React Native Rules

```
❌ Don't                             ✅ Do
------------------------------------------------------
Inline styles                        StyleSheet.create()
Duplicate StyleSheet per file        Shared styles in styles/shared.js
Heavy logic in JSX                   Extract to custom hook
> 200 lines per component            Split component
Copy-paste similar components        Extract reusable component
```

**Shared StyleSheet pattern:**
```js
// styles/shared.js
export const shared = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff', padding: 16 },
  title: { fontSize: 18, fontWeight: '700' },
})

// ScreenA.js
import { shared } from '../styles/shared'
```

**Custom hook for repeated logic:**
```js
// hooks/useAuth.js
export function useAuth() {
  const [user, setUser] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  return { user, isLoading, login, logout }
}
```
