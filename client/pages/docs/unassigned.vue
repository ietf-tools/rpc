<template>
  <TitleBlock title="Manage Unassigned Documents">
    <template #right>
      <button type="button" class="btn-secondary mr-3">
        <span class="sr-only">Refresh</span>
        <Icon name="solar:refresh-line-duotone" size="1.5em" @click="refresh"
              :class="[(queuePending || peoplePending) ? 'animate-spin text-orange-600' : 'text-gray-500 dark:text-neutral-300']"
              aria-hidden="true"/>
      </button>
    </template>
  </TitleBlock>

  <div class="mt-8 flow-root">
    <h2>Documents for assignment</h2>
    <!--    <div v-for="(doc, index) of documents" :key="doc.id"-->
    <!--         class="w-full max-w-5xl p-4 bg-white border border-gray-200 rounded-lg shadow sm:p-6 md:p-8 dark:bg-gray-800 dark:border-gray-700">-->
    <!--      <div class="space-y-1">-->
    <!--        <h5 class="text-xl font-medium text-gray-900 dark:text-white">{{ doc.name }}</h5>-->
    <!--        <div>{{ doc.title }}</div>-->
    <!--        <div>Labels here</div>-->
    <!--        <div>Pages: {{ doc.pages }}</div>-->
    <!--        <div>View Notes (with count)</div>-->

    <!--        <label :for="'editor' + doc.id" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">-->
    <!--          Assign editor-->
    <!--        </label>-->
    <!--        <select :id="'editor' + doc.id"-->
    <!--                v-model="state.newAssignments[index].personId"-->
    <!--                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">-->
    <!--          <option :value="null">Leave unassigned</option>-->
    <!--          <option v-for="editor of editors" :key="editor.id" :value="editor.id">-->
    <!--            {{ editor.name }}-->
    <!--          </option>-->
    <!--        </select>-->
    <!--      </div>-->
    <!--    </div>-->
    <!--    <Button @click="saveAssignments(state.newAssignments)">Save Changes</Button>-->
    <!--    <Button @click="state.newAssignments = buildAssignments(documents, [])">Reset</Button>-->
    <!--  </div>-->
    <DocumentCards :documents="documents"/>
    <EditorDeck :editors="editors"/>
  </div>
</template>

<script setup>
const csrf = useCookie('csrftoken', { sameSite: 'strict' })

const state = reactive({
  // newAssignments is an array of { rfcToBeId, personId } in the same order as the documents list
  newAssignments: []
})

// COMPUTED

const editors = computed(() => {
  if (!people.value) {
    return []
  }
  return people.value.map((person) => ({
    id: person.id,
    name: person.name
  }))
})

const documents = computed(() => {
  if (!queue.value) {
    return []
  }
  return queue.value.filter((doc) => doc.assignments.length === 0).map((doc) => ({
    id: doc.id,
    name: doc.name,
    title: doc.title || 'unknown title',
    pages: doc.pages || 'unknown'
  }))
})

// METHODS

async function saveAssignments (assignments) {
  state.newAssignments.forEach(({ rfcToBeId, personId }) => {
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

// Build assignments for a doc list, preserving old any old assignments
function buildAssignments (newDocuments, oldAssignments) {
  const oldAssignmentMap = Object.fromEntries(oldAssignments.map(oa => [oa.rfcToBeId, oa.personId]))
  return newDocuments.map((doc) => ({
    rfcToBeId: doc.id,
    personId: oldAssignmentMap[doc.id] ?? null
  }))
}

async function refresh () {
  await peopleRefresh()
  await queueRefresh()
}

// DATA RETRIEVAL

const { data: people, pending: peoplePending, refresh: peopleRefresh } = await useFetch('/api/rpc/rpc_person/', {
  baseURL: '/',
  server: false
})

const { data: queue, pending: queuePending, refresh: queueRefresh } = await useFetch('/api/rpc/queue/', {
  baseURL: '/',
  server: false,
  transform: (resp) => (resp?.queue || [])
})

onMounted(() => {
  watch(documents, (newDocuments) => {
    state.newAssignments = buildAssignments(newDocuments, state.newAssignments)
  })
})

/**
 * Todo
 * - use state instead of mutating computed values
 * - indicate changed assignments
 * - buttons to refresh/reset the view
 * - compute stats for editors (see details on wireframe)
 * - order editors based on stats
 */
</script>
