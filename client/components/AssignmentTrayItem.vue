<template>
  <div class="bg-pink-600 rounded-md m-2 p-2 flex items-start" :key="assignment.id">
    <div class="flex-shrink-0">
      <dl>
        <dt class="sr-only">Editor</dt>
        <dd class="text-sm text-white text-center">{{ assignment.initials }}</dd>
        <dt class="sr-only">Role</dt>
        <dd class="text-xs text-pink-100 text-center">{{ assignment.description }}</dd>
      </dl>
    </div>
    <div class="flex flex-shrink-0">
      <button type="button" @click="deleteAssignment(props.assignment)"
              class="inline-flex rounded-md text-pink-300 hover:text-pink-100 focus:outline-none focus:ring-1 focus:ring-pink-500 focus:ring-offset-1">
        <span class="sr-only">Dismiss</span>
        <Icon name="uil:times-circle" class="h-5 w-5" aria-hidden="true"/>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { inject } from 'vue'
import { deleteAssignmentKey } from '~/providers/providerKeys'

const props = defineProps<{
  assignment: {
    id: string
    person?: {
      name: string
    }
    role: string
  }
}>()

const _deleteAssignment = inject(deleteAssignmentKey)
if (!_deleteAssignment) {
  throw Error('Expected delete assignment to be available')
}
const deleteAssignment = _deleteAssignment

const assignment = computed(() => ({
  id: props.assignment.id,
  initials: props.assignment.person?.name,
  description: props.assignment.role
}))
</script>
