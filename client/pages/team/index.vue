<template>
  <TitleBlock title="Manage Team Members"
              summary="A list of all the users having access to this tool.">
    <template v-slot:buttons>
      <button type="button" class="btn-secondary mr-3">
        <span class="sr-only">Refresh</span>
        <Icon name="solar:refresh-line-duotone" size="1.5em" @click="refresh"
              :class="[pending ? 'animate-spin text-orange-600' : 'text-gray-500 dark:text-neutral-300']"
              aria-hidden="true"/>
      </button>
      <button type="button" @click="state.createDialogShown = true"
              class="flex items-center rounded-md bg-violet-600 px-3 py-2 text-center text-sm font-semibold text-white shadow-sm hover:bg-violet-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
        <Icon name="uil:plus" class="-ml-1 h-5 w-5 mr-2" aria-hidden="true"/>
        New Team Member
      </button>
    </template>
  </TitleBlock>
  <div class="mt-8 flow-root">
    <div class="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
      <div class="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
        <div class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 sm:rounded-lg">
          <table class="min-w-full divide-y divide-gray-300 dark:divide-neutral-600">
            <thead class="bg-gray-50 dark:bg-neutral-800">
              <tr>
                <th scope="col" class="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 dark:text-neutral-400 sm:pl-6">Name</th>
                <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900 dark:text-neutral-400">Roles</th>
                <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900 dark:text-neutral-400">Expertise</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200 dark:divide-neutral-700 bg-white dark:bg-neutral-900">
              <tr v-for="person in people" :key="person.email">
                <td class="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900 dark:text-neutral-100 sm:pl-6">
                  <NuxtLink :to="`/team/${person.id}`" class="text-violet-900 hover:text-violet-500 dark:text-violet-300 hover:dark:text-violet-100">{{ person.name }}</NuxtLink>
                </td>
                <td class="px-3 py-4 text-xs text-gray-500 dark:text-neutral-400">{{ person.roles.map(r => r.name).join(', ') }}</td>
                <td class="px-3 py-4 text-xs text-gray-500 dark:text-neutral-400">{{ person.capabilities.map(r => r.name).join(', ') }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>

  <UserCreateDialog v-model:isShown="state.createDialogShown" />
  <NotificationDialog v-model:isShown="state.notifDialogShown" type="negative" title="Fetch Error" :caption="state.notifDialogMessage" />
</template>

<script setup>
useHead({
  title: 'Manage Team Members'
})

// DATA

const state = reactive({
  createDialogShown: false,
  notifDialogShown: false,
  notifDialogMessage: ''
})

// METHODS

const { data: people, pending, refresh } = await useFetch('/api/rpc/rpc_person/', {
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
