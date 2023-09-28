<template>
  <div>
    <div class="mt-8 flow-root">
      <div class="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
        <div class="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
          <div class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 sm:rounded-lg">
            <DocumentTable
              :columns="columns"
              :data="documents"
              row-key="id"
            />
          </div>
        </div>
      </div>
    </div>
    <NotificationDialog v-model:isShown="state.notifDialogShown" type="negative" title="Fetch Error" :caption="state.notifDialogMessage" />
  </div>
</template>

<script setup>
import { DateTime } from 'luxon'

definePageMeta({
  layout: 'queue'
})
useHead({
  title: 'Recently Published - Queue'
})

// DATA

const state = reactive({
  notifDialogShown: false,
  notifDialogMessage: ''
})

const columns = [
  {
    key: 'rfc',
    label: 'RFC',
    field: 'rfc',
    format: val => `RFC ${val}`
  },
  {
    key: 'name',
    label: 'Document',
    field: 'name',
    classes: 'text-sm font-medium',
    link: row => `/docs/${row.id}`
  },

  {
    key: 'owner',
    label: 'PUB Owner',
    field: 'owner',
    format: val => val?.name || 'Unknown',
    link: row => `/team/${row.holder?.id}`
  },
  {
    key: 'published',
    label: 'Published',
    field: 'published',
    format: val => DateTime.fromISO(val).toLocaleString(DateTime.DATE_MED_WITH_WEEKDAY),
    classes: 'text-xs'
  }
]

const documents = [
  { id: 1, rfc: '1234', name: 'draft-ietf-foo-bar-04', published: '2023-08-28', owner: { id: 1, name: 'Ada Lovelace' } },
  { id: 2, rfc: '3456', name: 'draft-irtf-abcrg-edf-05', published: '2023-08-27', owner: { id: 2, name: 'Marie Curie' } },
  { id: 3, rfc: '5678', name: 'draft-irtf-abcrg-edf-05', published: '2023-08-27', owner: { id: 2, name: 'Marie Curie' } },
]

</script>
