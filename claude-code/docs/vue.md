# Vue Rules (2 & 3)

```
❌ Don't                             ✅ Do
------------------------------------------------------
Heavy logic in template              Move to computed/methods
Copy-paste logic across components   Extract composable useXxx()
> 200 lines per .vue file            Split into components
Mutating props directly              Emit events to parent
fetch() inside template              Call in onMounted / action
```

**Correct .vue structure:**
```vue
<template>
  <!-- Display logic only, max 1 ternary per line -->
</template>

<script setup>
// imports first
// composables
// props & emits
// reactive state
// computed
// methods (max 20 lines each)
// lifecycle hooks
</script>

<style scoped>
/* always scoped unless there's a strong reason not to */
</style>
```

**No fragments** — vue-loader di project ini tidak support multiple root elements. Selalu gunakan satu root `<div>`:
```vue
❌ <template>
     <div>...</div>
     <div>...</div>
   </template>

✅ <template>
     <div>
       <div>...</div>
       <div>...</div>
     </div>
   </template>
```

**Composable pattern** — same logic in 2+ components → extract:
```js
// composables/useUserData.js
export function useUserData() {
  const data = ref(null)
  const isLoading = ref(false)
  const fetchData = async (id) => { ... }
  return { data, isLoading, fetchData }
}
```
