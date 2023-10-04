<template>
  <div class="sm:flex sm:items-center">
    <div class="sm:flex-auto">
      <h1 class="text-base font-semibold leading-6 text-gray-900 dark:text-neutral-200">
        {{ props.title }}
      </h1>
      <p v-if="props.summary" class="mt-2 text-sm text-gray-700 dark:text-neutral-400">
        {{ props.summary }}
      </p>
    </div>
    <div class="mt-4 sm:ml-16 sm:mt-0 sm:flex">
      <slot name="buttons" />
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  title: { type: String, required: true },
  summary: { type: String }
})
</script>
