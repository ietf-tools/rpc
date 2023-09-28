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
  title: 'Exceptions - Queue'
})

// DATA

const state = reactive({
  notifDialogShown: false,
  notifDialogMessage: ''
})

const columns = [
  {
    key: 'name',
    label: 'Document',
    field: 'name',
    classes: 'text-sm font-medium',
    link: row => `/docs/${row.id}`
  },
  {
    key: 'submitted',
    label: 'Submitted',
    field: 'submitted',
    format: val => DateTime.fromISO(val).toLocaleString(DateTime.DATE_MED_WITH_WEEKDAY),
    classes: 'text-xs'
  },
  {
    key: 'exception',
    label: 'Exception',
    field: 'exception',
    classes: 'text-rose-600 dark:text-rose-500'
  },
  {
    key: 'holder',
    label: 'Action Holder',
    field: 'holder',
    format: val => val?.name || 'Unknown',
    link: row => `/team/${row.holder?.id}`
  },
  {
    key: 'deadline',
    label: 'Deadline',
    field: 'deadline',
    format: val => DateTime.fromISO(val).toLocaleString(DateTime.DATE_MED_WITH_WEEKDAY),
    classes: 'text-xs'
  }
]

const documents = [
  { id: 1, name: 'draft-ietf-foo-bar-04', submitted: '2023-07-25', deadline: '2023-08-28', exception: 'Font issues', holder: { id: 1, name: 'Ada Lovelace' } },
  { id: 3, name: 'draft-irtf-abcrg-edf-05', submitted: '2023-07-19', deadline: '2023-08-27', exception: 'Missing donuts', holder: { id: 2, name: 'Marie Curie' } },
]

</script>
