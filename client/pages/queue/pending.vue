<template>
  <div>
    <div class="mt-8 flow-root">
      <div class="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
        <div class="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
          <div class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 sm:rounded-lg">
            <div v-if="!pending">
              <DocumentTable
                :columns="columns"
                :data="documents.queue.filter(d => d.assignments.length === 0)"
                row-key="id"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
    <NotificationDialog v-model:isShown="state.notifDialogShown" type="negative" title="Fetch Error"
                        :caption="state.notifDialogMessage"/>
  </div>
</template>

<script setup>
import {DateTime} from 'luxon'

definePageMeta({
  layout: 'queue'
})
useHead({
  title: 'Pending Assignment - Queue'
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
    key: 'deadline',
    label: 'Deadline',
    field: 'deadline',
    format: val => val ? DateTime.fromISO(val).toLocaleString(DateTime.DATE_MED_WITH_WEEKDAY) : "-",
    classes: 'text-xs'
  },
  {
    key: 'cluster',
    label: 'Cluster',
    field: 'cluster',
    format: val => val || "-"
  },
]

const {data: documents, pending, refresh} = await useFetch('/api/rpc/queue/', {
  baseURL: '/',
  server: false,
})

</script>
