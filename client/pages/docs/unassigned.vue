<template>
  <TitleBlock title="Manage Unassigned Documents">
    <template #right>
      <button type="button" class="btn-secondary mr-3">
        <span class="sr-only">Refresh</span>
        <Icon name="solar:refresh-line-duotone" size="1.5em"
              class="text-gray-500 dark:text-neutral-300"
              aria-hidden="true"/>
      </button>
    </template>
  </TitleBlock>

  <div class="mt-8 flow-root">
    <h2>Documents for assignment</h2>
    <DocumentCards :documents="documents"
                   @assignEditorToDocument="(dId, edId) => saveAssignments([{rfcToBeId: dId, personId: edId}])"/>
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

async function saveAssignments (assignments) {
  assignments.forEach(({ rfcToBeId, personId }) => {
    $fetch('/api/rpc/assignments/', {
      body: {
        rfc_to_be: rfcToBeId,
        person: personId,
        role: 'first_editor'
      },
      method: 'POST',
      headers: { 'X-CSRFToken': csrf.value }
    })
  })
}

// DATA RETRIEVAL

const { data: people } = await useFetch('/api/rpc/rpc_person/', { baseURL: '/', server: false })
const { data: rfcsToBe } = await useFetch('/api/rpc/documents/', { baseURL: '/', server: false })
const { data: assignments } = await useFetch('/api/rpc/assignments/', { baseURL: '/', server: false })

/**
 * Todo
 * - indicate changed assignments
 * - buttons to refresh/reset the view
 * - compute stats for editors (see details on wireframe)
 * - order editors based on stats
 */
</script>
