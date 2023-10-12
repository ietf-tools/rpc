<template>
  <TitleBlock title="Manage Assignments">
    <template #right>
      <button type="button" class="btn-secondary mr-3">
        <span class="sr-only">Refresh</span>
        <Icon name="solar:refresh-line-duotone" size="1.5em" @click="refreshAssignments"
              :class="[pending ? 'animate-spin text-orange-600' : 'text-gray-500 dark:text-neutral-300']"
              aria-hidden="true"/>
      </button>
    </template>
  </TitleBlock>

  <div class="mt-8 flow-root">
    <h2>Documents for assignment</h2>
    <DocumentCards :documents="documents"
                   @assign-editor-to-document="(dId, edId) => saveAssignment({rfcToBeId: dId, personId: edId})"
                   @delete-assignment="deleteAssignment"/>
    <EditorPalette :editors="people"/>
  </div>
</template>

<script setup>
const csrf = useCookie('csrftoken', { sameSite: 'strict' })

// COMPUTED

const cookedAssignments = computed(() => assignments.value?.map(a => ({
  ...a,
  // person is a Person id - replace it with person details
  person: people.value?.find(ed => ed.id === a.person)
})))

const documents = computed(() => rfcsToBe.value?.map((rtb) => ({
  ...rtb,
  // augment with assignments
  assignments: cookedAssignments.value?.filter(a => a.rfc_to_be === rtb.id)
})))

// METHODS

async function saveAssignment (assignment) {
  await $fetch('/api/rpc/assignments/', {
    body: {
      rfc_to_be: assignment.rfcToBeId,
      person: assignment.personId,
      role: 'first_editor'
    },
    method: 'POST',
    headers: { 'X-CSRFToken': csrf.value }
  })
  if (refreshAssignments) {
    refreshAssignments()
  }
}

async function deleteAssignment (assignment) {
  await $fetch(`/api/rpc/assignments/${assignment.id}`, {
    method: 'DELETE',
    headers: { 'X-CSRFToken': csrf.value }
  })
  if (refreshAssignments) {
    refreshAssignments()
  }
}

// DATA RETRIEVAL

const { data: people } = await useFetch('/api/rpc/rpc_person/', { baseURL: '/', server: false })
const { data: rfcsToBe } = await useFetch('/api/rpc/documents/', { baseURL: '/', server: false })
const { data: assignments, pending, refresh: refreshAssignments } = await useFetch('/api/rpc/assignments/', { baseURL: '/', server: false })

</script>
