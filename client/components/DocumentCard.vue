// template based on https://flowbite.com/docs/components/card/#default-card
<template>
  <div
     class="block max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700">
    <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
      {{ document.name }}
    </h5>
    <div>
    <draggable class="right-1" v-model="state.assignees" group="editors" item-key="id" add="addAssignee">
      <template #item="{element}">
        <div>{{ element.name }}</div>
      </template>
    </draggable>
  </div>
  </div>
</template>

<script setup>
defineProps({
  document: { type: Object, required: true }
})

const state = reactive({
  assignees: []
})

</script>
