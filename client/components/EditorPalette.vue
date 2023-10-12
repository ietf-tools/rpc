<!-- Editor Palette
Based on https://tailwindui.com/components/application-ui/lists/grid-lists#component-4ec337def61b547035ce908c128bca5c
-->
<template>
  <div>
    <h2 class="text-sm font-medium text-gray-500">Available Editors</h2>
    <Sortable
      :list=props.editors
      item-key="id"
      class="mt-3 grid grid-cols-1 gap-5 sm:grid-cols-2 sm:gap-6 lg:grid-cols-4"
      :options="sortableOptions">
      <template #item="{ element: ed }">
        <div class="draggable" :data-editor-id="ed.id">
          <EditorPaletteItem :editor="ed"/>
        </div>
      </template>
    </Sortable>
  </div>
</template>

<script setup>
import { Sortable } from 'sortablejs-vue3'

const props = defineProps({
  editors: Array
})

const sortableOptions = {
  group: {
    name: 'editors',
    pull: 'clone',
    put: false
  },
  sort: false
}
</script>
