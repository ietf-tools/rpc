<template>
  <TitleBlock title="Queue"
              summary="Where the magic happens.">
    <template #right>
      <div class="mt-2 text-right text-gray-700 dark:text-neutral-400 sm:ml-16 sm:mt-0">
        <div class="text-sm">Backlog <strong class="text-rose-700">larger
          <Icon name="uil:angle-double-up" class="text-lg -mt-0.5"/>
        </strong> than a week ago
        </div>
        <div class="text-xs"><strong>2 weeks</strong> to drain the queue <em>(was <strong>3 days</strong> a week
          ago)</em></div>
      </div>
    </template>
  </TitleBlock>

  <!-- TABS -->

  <div class="flex justify-center items-center">
    <TabNav :tabs="tabs" :selected="currentTab" />
    <button type="button" @click="refresh" class="btn-secondary ml-3">
      <span class="sr-only">Refresh</span>
      <Icon name="solar:refresh-line-duotone" size="1.5em"
            :class="[pending ? 'animate-spin text-orange-600' : 'text-gray-500 dark:text-neutral-300']"
            aria-hidden="true"/>
    </button>
    <button type="button" @click="" class="btn-secondary ml-3">
      <span class="sr-only">Filter</span>
      <Icon name="solar:filter-line-duotone" size="1.5em" class="text-gray-500 dark:text-neutral-300"
            aria-hidden="true"/>
    </button>
  </div>

  <!-- DATA TABLE -->

  <div class="mt-2 flow-root">
    <div class="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
      <div class="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
        <div class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 sm:rounded-lg">
          <DocumentTable
            :columns="columns"
            :data="filteredDocuments"
            row-key="id"
            :loading="pending"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { DateTime } from 'luxon'
import Fuse from 'fuse.js/dist/fuse.basic.esm'
import { useSiteStore } from '@/stores/site'

// ROUTING

const route = useRoute()

// STORES

const siteStore = useSiteStore()

// DIALOGS

const snackbar = useSnackbar()

// API

const api = useApi()

// DATA

const tabs = [
  { id: 'submissions', name: 'Submissions', to: '/queue/submissions', icon: 'uil:bolt-alt' },
  { id: 'pending', name: 'Pending Assignment', to: '/queue/pending', icon: 'uil:clock' },
  { id: 'exceptions', name: 'Exceptions', to: '/queue/exceptions', icon: 'uil:exclamation-triangle' },
  { id: 'inprocess', name: 'In Process', to: '/queue/inprocess', icon: 'solar:refresh-circle-line-duotone' },
  { id: 'published', name: 'Recently Published', to: '/queue/published', icon: 'uil:check-circle' }
]

// COMPUTED

const deadlineCol = {
  key: 'deadline',
  label: 'Deadline',
  field: 'deadline',
  format: val => val ? DateTime.fromISO(val).toLocaleString(DateTime.DATE_MED_WITH_WEEKDAY) : '',
  classes: 'text-xs'
}

const columns = computed(() => {
  const cols = [
    {
      key: 'name',
      label: 'Document',
      field: 'name',
      classes: 'text-sm font-medium',
      link: row => currentTab.value === 'submissions' ? `/docs/import/?draft=${row.name}` : `/docs/${row.name}`
    },
    {
      key: 'labels',
      label: 'Labels',
      labels: row => row.labels || []
    }
  ]
  if (['submissions', 'exceptions'].includes(currentTab.value)) {
    cols.push({
      key: 'submitted',
      label: 'Submitted',
      field: 'submitted',
      format: val => val ? DateTime.fromISO(val).toLocaleString(DateTime.DATE_MED_WITH_WEEKDAY) : '',
      classes: 'text-xs'
    })
  }
  if (currentTab.value === 'pending') {
    cols.push(deadlineCol)
  }
  if (currentTab.value === 'published') {
    cols.unshift({
      key: 'rfc',
      label: 'RFC',
      field: 'rfc',
      format: val => `RFC ${val}`
    })
  }
  if (currentTab.value === 'exception') {
    cols.push({
      key: 'exception',
      label: 'Exception',
      field: 'exception',
      classes: 'text-rose-600 dark:text-rose-500'
    })
  }
  if (['exceptions', 'inprocess'].includes(currentTab.value)) {
    cols.push(...[
      {
        key: 'assignee',
        label: 'Assignee (should allow multiple)',
        field: 'assignee',
        format: val => val?.name || 'No assignments',
        link: row => `/team/${row.assignee?.id}`
      }
    ])
    cols.push(...[
      {
        key: 'holder',
        label: 'Action Holder (should allow multiple)',
        field: 'holder',
        format: val => val?.name || 'No Action Holders',
        link: row => `/team/${row.holder?.id}`
      },
      deadlineCol
    ])
  }
  if (currentTab.value === 'inprocess') {
    cols.push(...[
      {
        key: 'currentState',
        label: 'Current State',
        field: 'currentState'
      },
      {
        key: 'estimatedCompletion',
        label: 'Estimated Completion',
        field: 'estimatedCompletion',
        format: val => {
          const dt = DateTime.fromISO(val)
          return dt.isValid ? dt.toLocaleString(DateTime.DATE_MED_WITH_WEEKDAY) : '---'
        },
        classes: 'text-xs'
      },
      {
        key: 'status',
        label: 'Status',
        field: 'status',
        classes: val => (val === 'overdue') ? 'font-medium text-rose-600 dark:text-rose-500' : 'text-emerald-600 dark:text-emerald-500'
      }
    ])
  }
  if (currentTab.value === 'pending') {
    cols.push({
      key: 'cluster',
      label: 'Cluster',
      field: 'cluster',
      icon: 'pajamas:group',
      link: val => val ? `/clusters/${val.cluster}` : ''
    })
  }
  if (currentTab.value === 'published') {
    cols.push(...[
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
    ])
  }
  return cols
})

const currentTab = computed(() => {
  return route.params.section || 'submissions'
})

const filteredDocuments = computed(() => {
  let docs = []

  // -> Filter based on selected tab
  switch (currentTab.value) {
    case 'submissions':
      docs = documents.value
      break
    case 'pending':
      docs = documents.value?.filter(d => d.assignmentSet?.length === 0)
      break
    case 'exceptions':
      docs = documents.value?.filter(d => d.labels.filter(lbl => lbl.isException).length)
      break
    case 'inprocess':
      docs = documents.value?.filter(d => d.assignmentSet?.length > 0).map(d => ({
        ...d,
        currentState: `${d.assignmentSet[0].role} (${d.assignmentSet[0].state})`,
        assignee: d.assignmentSet[0],
        holder: d.actionholderSet[0]
      }))
      break
    default:
      docs = []
      break
  }

  // -> Fuzzy search
  if (siteStore.search) {
    const fuse = new Fuse(docs, {
      keys: [
        'name',
        'rfc'
      ]
    })
    return fuse.search(siteStore.search).map(n => n.item)
  } else {
    return docs
  }
})

// INIT

const { data: documents, pending, refresh } = await useAsyncData(
  'queue',
  async () => {
    try {
      if (currentTab.value === 'submissions') {
        return await api.submissionsRetrieve()
      } else {
        return await api.queueList()
      }
    } catch (err) {
      snackbar.add({
        type: 'error',
        title: 'Fetch Failed',
        text: err
      })
    }
  },
  {
    server: false,
    lazy: true,
    default: () => ([]),
    transform: (resp) => {
      return currentTab.value === 'submissions' ? (resp?.submitted ?? []) : resp
    }
  })

onMounted(() => {
  siteStore.search = ''
})
</script>
