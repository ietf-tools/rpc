<!-- Editor Deck
Based on https://tailwindui.com/components/application-ui/lists/grid-lists#component-4ec337def61b547035ce908c128bca5c
-->
<template>
  <div>
    <h2 class="text-sm font-medium text-gray-500">Pinned Projects</h2>
    <ul role="list" class="mt-3 grid grid-cols-1 gap-5 sm:grid-cols-2 sm:gap-6 lg:grid-cols-4">
      <EditorCard v-for="ed in props.editors" :editor="ed"/>
    </ul>
  </div>
</template>

<script setup>
const props = defineProps({
  editors: Array
})

</script>
