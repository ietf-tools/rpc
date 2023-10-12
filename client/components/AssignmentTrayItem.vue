<template>
  <div
    :key="assignment.id"
    class="bg-pink-600 rounded-md">
    <dl class="m-2 p-2">
      <dt class="sr-only">Editor</dt>
      <dd class="text-sm text-white text-center">{{ assignment.initials }}</dd>
      <dt class="sr-only">Role</dt>
      <dd class="text-xs text-pink-100 text-center">{{ assignment.description }}</dd>
    </dl>
  </div>
</template>

<script setup>
const props = defineProps({
  assignment: Object
})

const assignment = computed(() => ({
  id: props.assignment.id,
  initials: props.assignment.person?.name,
  description: props.assignment.role
}))
</script>
