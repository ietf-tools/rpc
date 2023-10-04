<template>
  <TitleBlock title="Queue"
              summary="Where the magic happens.">
    <template v-slot:right>
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
    <nav class="isolate grow flex divide-x divide-gray-200 dark:divide-neutral-950 rounded-lg shadow max-w-7xl my-4"
      aria-label="Tabs"
      >
      <NuxtLink
        v-for="(tab, tabIdx) in tabs"
        :key="tab.id"
        :href="`/queue/${tab.id}`"
        :class="[
          tab.id === currentTab ? 'bg-white dark:bg-neutral-800 text-violet-700 dark:text-violet-300' : 'bg-white dark:bg-neutral-700 text-gray-500 dark:text-neutral-300 hover:text-gray-700 hover:dark:text-neutral-200',
          tabIdx === 0 ? 'rounded-l-lg' : '', tabIdx === tabs.length - 1 ? 'rounded-r-lg' : '',
          'group relative min-w-0 flex-1 overflow-hidden py-3 px-4 text-center text-sm font-medium hover:bg-gray-50 hover:dark:bg-neutral-800 focus:z-10'
        ]"
        :aria-current="tab.id === currentTab ? 'page' : undefined"
        >
        <Icon :name="tab.icon" :class="['h-5 w-5 mr-2', tab.iconAnimation ? `group-hover:animate-${tab.iconAnimation}` : '']" aria-hidden="true"/>
        <span>{{ tab.name }}</span>
        <span aria-hidden="true"
          :class="[tab.id === currentTab ? 'bg-violet-500' : 'bg-transparent', 'absolute inset-x-0 bottom-0 h-0.5']"
          />
      </NuxtLink>
    </nav>
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
  <NotificationDialog
    v-model:isShown="state.notifDialogShown"
    type="negative"
    title="Fetch Error"
    :caption="state.notifDialogMessage"
    />
</template>

<script setup>
import { DateTime } from 'luxon'
import Fuse from 'fuse.js/dist/fuse.basic.esm'
import { useSiteStore } from '@/stores/site'

// ROUTING

const route = useRoute()

// STORES

const siteStore = useSiteStore()

// DATA

const state = reactive({
  notifDialogShown: false,
  notifDialogMessage: ''
})

const tabs = [
  { id: 'submissions', name: 'Submissions', icon: 'uil:bolt-alt' },
  { id: 'pending', name: 'Pending Assignment', icon: 'uil:clock', iconAnimation: 'spin' },
  { id: 'exceptions', name: 'Exceptions', icon: 'uil:exclamation-triangle' },
  { id: 'inprocess', name: 'In Process', icon: 'uil:atom', iconAnimation: 'spin' },
  { id: 'published', name: 'Recently Published', icon: 'uil:check-circle' }
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
      link: row => `/docs/${row.name}`
    },
    {
      key: 'labels',
      label: 'Labels',
      field: 'labels',
      classes: 'text-xs font-small',
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
      docs = documents.value?.filter(d => d.assignments?.length === 0)
      break
    case 'inprocess':
      docs = documents.value?.filter(d => d.assignments?.length > 0).map(d => ({
        ...d,
        currentState: `${d.assignments[0].role} (${d.assignments[0].state})`,
        assignee: d.assignments[0],
        holder: d.action_holders[0]
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

const { data: documents, pending, refresh } = await useFetch(
  () => currentTab.value === 'submissions' ? '/api/rpc/submissions/' : '/api/rpc/queue/', {
    key: 'queue',
    baseURL: '/',
    server: false,
    lazy: true,
    data: () => ([]),
    transform: (resp) => {
      return currentTab.value === 'submissions' ? (resp?.submitted ?? []) : (resp?.queue ?? [])
    },
    onRequestError ({ error }) {
      state.notifDialogMessage = error
      state.notifDialogShown = true
    },
    onResponseError ({ response, error }) {
      state.notifDialogMessage = response.statusText ?? error
      state.notifDialogShown = true
    }
  }
)

onMounted(() => {
  siteStore.search = ''
})
</script>
