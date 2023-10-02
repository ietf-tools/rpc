<template>
  <div class="px-4 py-10 sm:px-6 lg:px-8 lg:py-6">
    <div class="sm:flex sm:items-center">
      <div class="sm:flex-auto">
        <h1 class="text-base font-semibold leading-6 text-gray-900 dark:text-neutral-200">
          Manage Clusters
        </h1>
        <p class="mt-2 text-sm text-gray-700 dark:text-neutral-400">
          Document clusters known to this tool.
        </p>
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
          <div class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 sm:rounded-lg">
            <table class="min-w-full divide-y divide-gray-300 dark:divide-neutral-600">
              <thead class="bg-gray-50 dark:bg-neutral-800">
              <tr>
                <th scope="col"
                    class="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 dark:text-neutral-400 sm:pl-6">
                  Number
                </th>
              </tr>
              </thead>
              <tbody class="divide-y divide-gray-200 dark:divide-neutral-700 bg-white dark:bg-neutral-900">
              <tr v-for="cluster in clusters" :key="cluster.number">
                <td
                  class="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900 dark:text-neutral-100 sm:pl-6">
                  <NuxtLink :to="`/clusters/${cluster.number}`"
                            class="text-violet-900 hover:text-violet-500 dark:text-violet-300 hover:dark:text-violet-100">
                    {{ cluster.number }}
                  </NuxtLink>
                </td>
              </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

<!--    <UserCreateDialog v-model:isShown="state.createDialogShown"/>-->
    <NotificationDialog v-model:isShown="state.notifDialogShown" type="negative" title="Fetch Error"
                        :caption="state.notifDialogMessage"/>
  </div>
</template>

<script setup>
useHead({
  title: 'Manage Clusters'
})

// DATA

const state = reactive({
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
