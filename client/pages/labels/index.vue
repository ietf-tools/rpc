<template>
  <div class="px-4 sm:px-6 lg:px-8">
    <div class="sm:flex sm:items-center">
      <div class="sm:flex-auto">
        <h1 class="text-base font-semibold leading-6 text-gray-900">Labels</h1>
      </div>
      <div class="mt-4 sm:ml-16 sm:mt-0 sm:flex-none">
        <button @click="addLabel()" type="button" class="block rounded-md bg-indigo-600 px-3 py-2 text-center text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Add Label</button>
      </div>
    </div>
    <div class="mt-8 flow-root">
      <div class="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
        <div class="inline-block min-w-fit py-2 align-middle sm:px-6 lg:px-8">
          <div class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 sm:rounded-lg">
            <table class="min-w-fit divide-y divide-gray-300">
              <thead class="bg-gray-50">
                <tr>
                  <th scope="col" class="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-6">Name</th>
                  <th scope="col" class="relative py-3.5 pl-3 pr-4 sm:pr-6">
                    <span class="sr-only">Edit</span>
                  </th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-200 bg-white">
                <tr v-for="label in labels" :key="label.slug">
                  <td class="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-6"><Icon v-if="label.is_exception" class="mr-2" name="pajamas:warning" /><Badge :label="label.slug" :color="label.color" /></td>
                  <td class="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
                    <Icon name="circum:edit" class="text-indigo-600 hover:text-indigo-900 cursor-pointer"  @click="editLabel(label)" /><span class="sr-only">Edit {{ label.slug }}</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { LabelEditDialog } from '#components'

const { data: labels, pending, refresh } = await useFetch('/api/rpc/labels/', {
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

const { openOverlayModal } = inject('overlayModal')

async function addLabel () {
  const result = await openOverlayModal({
    component: LabelEditDialog,
    componentProps: {
      label: {slug: '', is_exception: false, color: 'slate'},
      create: true
    }
  })
  refresh()
}

async function editLabel (label) {
  const result = await openOverlayModal({
    component: LabelEditDialog,
    componentProps: {
      label,
      create: false
    }
  })
  refresh()
}

</script>
