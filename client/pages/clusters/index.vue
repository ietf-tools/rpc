<template>
  <div class="sm:flex sm:items-center">
    <div class="sm:flex-auto">
      <h1 class="text-base font-semibold leading-6 text-gray-900 dark:text-neutral-200">
        Cluster Management
      </h1>
      <div>
        <label for="cluster-select">Cluster: </label>
        <select id="cluster-select" v-model="state.selectedClusterNumber">
          <option disabled value="">Select</option>
          <option v-for="cluster in clusters">{{ cluster.number }}</option>
        </select>
      </div>
    </div>
    <div class="mt-4 sm:ml-16 sm:mt-0 sm:flex">
      <button type="button" class="btn-secondary mr-3">
        <span class="sr-only">Refresh</span>
        <Icon name="solar:refresh-line-duotone" size="1.5em" @click="refresh"
              :class="[pending ? 'animate-spin text-orange-600' : 'text-gray-500 dark:text-neutral-300']"
              aria-hidden="true"/>
      </button>
      <button type="button" @click="state.createDialogShown = true"
              class="flex items-center rounded-md bg-violet-600 px-3 py-2 text-center text-sm font-semibold text-white shadow-sm hover:bg-violet-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
        <Icon name="uil:plus" class="-ml-1 h-5 w-5 mr-2" aria-hidden="true"/>
        New Cluster
      </button>
    </div>
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
  <NotificationDialog v-model:isShown="state.notifDialogShown" type="negative" title="Fetch Error"
                      :caption="state.notifDialogMessage"/>
</template>

<script setup>
useHead({
  title: 'Manage Clusters'
})

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
    state.notifDialogMessage = error
    state.notifDialogShown = true
  },
  onResponseError ({ response, error }) {
    state.notifDialogMessage = response.statusText ?? error
    state.notifDialogShown = true
  }
})
</script>
