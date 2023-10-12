<template>
  <Sortable
    :list="props.assignments"
    item-key="id"
    class="container flex flex-wrap gap-2"
    :options="sortableOptions"
    @add="event => $emit('assignEditor', event.clone.dataset.editorId)"
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

defineEmits(['assignEditor'])

const sortableOptions = {
  group: {
    name: 'assignments',
    pull: false,
    put: ['editors']
  },
  sort: false
}
</script>
