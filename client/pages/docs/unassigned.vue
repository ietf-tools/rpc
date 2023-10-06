<template>
  <TitleBlock title="Manage Unassigned Documents"/>

  <div class="mt-8 flow-root">
    <h2>Documents for assignment</h2>
    <div v-for="doc of documents" :key="doc.id"
         class="w-full max-w-5xl p-4 bg-white border border-gray-200 rounded-lg shadow sm:p-6 md:p-8 dark:bg-gray-800 dark:border-gray-700">
      <div class="space-y-1">
        <h5 class="text-xl font-medium text-gray-900 dark:text-white">{{ doc.name }}</h5>
        <div>{{ doc.title }}</div>
        <div>Labels here</div>
        <div>Pages: {{ doc.pages }}</div>
        <div>View Notes (with count)</div>

        <label :for="'editor' + doc.id" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
          Assign editor
        </label>
        <select :id="'editor' + doc.id"
                v-model="doc.assignTo"
                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
          <option value="">Leave unassigned</option>
          <option v-for="editor of editors" :key="editor.id" :value="editor.id">
            {{ editor.name }}
          </option>
        </select>
      </div>
    </div>
    <Button @click="saveAssignments()">Save Changes</Button>
  </div>
</template>

<script setup>
const csrf = useCookie('csrftoken', { sameSite: 'strict' })

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
    pages: doc.pages || 'unknown',
    assignTo: ''
  }))
})

// METHODS

async function saveAssignments () {
  documents.value?.filter((doc) => !!doc.assignTo).forEach((docToAssign) => {
    $fetch('/api/rpc/assignments/', {
      body: {
        rfc_to_be: Number(docToAssign.id),
        person: Number(docToAssign.assignTo),
        role: 'first_editor'
      },
      method: 'POST',
      headers: { 'X-CSRFToken': csrf.value }
    })
  })
}

// DATA RETRIEVAL

const { data: people } = await useFetch('/api/rpc/rpc_person/', {
  baseURL: '/',
  server: false
})

const { data: queue } = await useFetch('/api/rpc/queue/', {
  baseURL: '/',
  server: false,
  transform: (resp) => (resp?.queue || [])
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
