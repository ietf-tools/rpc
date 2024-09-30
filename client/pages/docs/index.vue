<template>
  <div>
    <TitleBlock title="My Documents" summary="Documents assigned to me">
      <template #right>
        <RefreshButton class="mr-3"/>
        <NuxtLink
          v-if="userStore.isManager"
          class="max-w-l items-center rounded-md bg-violet-600 px-3 py-2 text-center text-sm font-semibold text-white shadow-sm hover:bg-violet-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
          to="/docs/assignments">
          Manage Assignments
        </NuxtLink>
      </template>
    </TitleBlock>
    <div class="mt-8 flow-root">
      <DocumentTable
        :columns="columns"
        :data="tableRows"
        row-key="id"
        :loading="pending"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAsyncData } from '#app'
import type { Column } from '~/components/DocumentTableTypes'

const api = useApi()
const userStore = useUserStore()

// COMPUTED

const myAssignments = computed(() => allAssignments.value?.filter(
  (a) => a.person === userStore.rpcPersonId
).map(
  (a) => ({ ...a, rfcToBe: allDocuments.value?.find(d => d.id === a.rfcToBe) })
))

const tableRows = computed(() => myAssignments.value.map(a => ({ ...a.rfcToBe })).filter(row => !!row))

const pending = computed(() => assignmentsPending.value || documentsPending.value)

// DATA

function findLabel (labelId: number) {
  return labels.value.find((lbl) => lbl.id === labelId) ?? ''
}

const columns: Column<typeof tableRows.value[number]>[] = [
  {
    key: 'name',
    label: 'Document',
    field: 'name',
    classes: 'text-sm font-medium',
    link: row => `/docs/${row.name}`
  },
  {
    field: 'labels',
    key: 'labels',
    label: 'Labels',
    labels: row => {
      if (row.labels) {
        return row.labels.map(findLabel)
      }
      return []
    }
  }
]

const { data: allAssignments, pending: assignmentsPending } = await useAsyncData(
  'allAssignments',
  () => api.assignmentsList(),
  { server: false, default: () => ([]) }
)

const { data: allDocuments, pending: documentsPending } = await useAsyncData(
  'allDocuments',
  () => api.documentsList(),
  { server: false, default: () => ([]) }
)

const { data: labels } = await useAsyncData(
  'labels',
  () => api.labelsList(),
  { server: false, default: () => ([]) }
)

</script>
