<template>
  <Sortable
    :list="props.assignments"
    item-key="id"
    class="container flex flex-wrap gap-2"
    :options="sortableOptions"
    @add="addEditor"
  >
    <template #item="{element, index}">
      <div class="draggable">
        <AssignmentTrayItem :assignment="element"/>
      </div>
    </template>
  </Sortable>
</template>

<script setup>
import { Sortable } from 'sortablejs-vue3'

const props = defineProps({
  assignments: Array
})

const emit = defineEmits(['assignEditor'])

const sortableOptions = {
  group: {
    name: 'assignments',
    pull: false,
    put: ['editors']
  },
  sort: false
}

function addEditor (event) {
  event.item.remove() // remove the cloned editor from the DOM
  emit('assignEditor', event.clone.dataset.editorId)
}
</script>
