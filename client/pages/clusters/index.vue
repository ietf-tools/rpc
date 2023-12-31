<template>
  <TitleBlock title="Cluster Management">
    <template #right>
      <RefreshButton :pending="pending" @refresh="refresh" class="mr-3"/>
      <button type="button" @click="state.createDialogShown = true"
              class="flex items-center rounded-md bg-violet-600 px-3 py-2 text-center text-sm font-semibold text-white shadow-sm hover:bg-violet-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
        <Icon name="uil:plus" class="-ml-1 h-5 w-5 mr-2" aria-hidden="true"/>
        New Cluster
      </button>
    </template>
  </TitleBlock>

  <div class="mt-8 flow-root">
    <label for="cluster-select">Cluster: </label>
    <select id="cluster-select" v-model="state.selectedClusterNumber">
      <option disabled value="">Select</option>
      <option v-for="cluster in clusters">{{ cluster.number }}</option>
    </select>
  </div>
  <div class="mt-8 flow-root">
    <div class="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
      <div class="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
        <div v-for="document of selectedCluster?.documents">
          <DocumentCard :document="document" />
        </div>
      </div>
    </div>
    <div class="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
      <div class="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
        <div class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 sm:rounded-lg">
          Add an editor
        </div>
      </div>
    </div>
    <div class="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
      <div class="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
        <div class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 sm:rounded-lg">
          Document list
        </div>
      </div>
    </div>
  </div>

  <!--    <UserCreateDialog v-model:isShown="state.createDialogShown"/>-->
</template>

<script setup>
import RefreshButton from '~/components/RefreshButton.vue'

useHead({
  title: 'Manage Clusters'
})

const snackbar = useSnackbar()

// COMPUTED
const selectedCluster = computed(() => {
  if (clusters && clusters.value && state.selectedClusterNumber) {
    return clusters.value.find(cluster => String(cluster.number) === state.selectedClusterNumber)
  }
  return null
})
// DATA

const state = reactive({
  selectedClusterNumber: '',
  createDialogShown: false,
  notifDialogShown: false,
  notifDialogMessage: ''
})

// METHODS

const { data: clusters, pending, refresh } = await useFetch('/api/rpc/clusters/', {
  baseURL: '/',
  server: false,
  onRequestError ({ error }) {
    snackbar.add({
      type: 'error',
      title: 'Fetch Failed',
      text: error
    })
  },
  onResponseError ({ response, error }) {
    snackbar.add({
      type: 'error',
      title: 'Server Error',
      text: response.statusText ?? error
    })
  }
})
</script>
