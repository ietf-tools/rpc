<!-- Document Cards
Based on https://tailwindui.com/components/application-ui/lists/grid-lists#component-2beafc928684743ff886c0b164edb126-->
<template>
  <ul role="list" class="grid grid-cols-1 gap-x-6 gap-y-8 lg:grid-cols-3 xl:gap-x-8">
    <DocumentCard v-for="doc of props.documents" :document="doc" />
  </ul>
</template>

<script setup>
const props = defineProps({
  documents: Array
})
</script>
