<template>
    <TitleBlock title="Final Reviews"
              summary="Where the magic mercifully stops happening.">
  </TitleBlock>

  <!-- TABS -->

  <div class="flex justify-center items-center">
    <TabNav :tabs="tabs" :selected="currentTab" />
    <RefreshButton :pending="pending" @refresh="refresh" class="ml-3"/>
    <button type="button" @click="" class="btn-secondary ml-3">
      <span class="sr-only">Filter</span>
      <Icon name="solar:filter-line-duotone" size="1.5em" class="text-gray-500 dark:text-neutral-300"
            aria-hidden="true"/>
    </button>
  </div>

  <div class="mt-8 flow-root">
    <DocumentTable
      :columns="columns"
      :data="docs"
      row-key="id"
    />
  </div>

  <p class="pt-5 text-center text-gray-500">(data are mocked)</p>
</template>

<script setup>
const route = useRoute()

// COMPUTED

const currentTab = computed(() => route.params.section)

const docs = computed(() => {
  switch (currentTab.value) {
    case 'inprogress':
      return [
        {
          id: 0,
          name: 'RFC NNNNN <draft-ietf-sipcore-rfc3261bis-78>',
          ed: {
            id: 0,
            name: 'A. Travis'
          },
          ah: 'author'
        },
        {
          id: 1,
          name: 'RFC YYYY <draft-ietf-stir-stuff-10>',
          ed: {
            id: 1,
            name: 'B. Jenkins'
          },
          ah: 'editor'
        },
        {
          id: 2,
          name: 'RFC AAAA3 <draft-string>',
          ed: {
            id: 1,
            name: 'B. Jenkins'
          },
          ah: 'IANA'
        }
      ]

    case 'done':
      return [
        {
          id: 3,
          name: 'RFC AAAA1 <draft-string>',
          ed: {
            id: 0,
            name: 'A. Travis'
          }
        },
        {
          id: 4,
          name: 'RFC AAAA2 <draft-string>',
          ed: {
            id: 0,
            name: 'A. Travis'
          }
        },
        {
          id: 5,
          name: 'RFC CCCC <draft-string>',
          ed: {
            id: 1,
            name: 'B. Jenkins'
          }
        }
      ]

    case 'forpub':
      return [
        {
          id: 6,
          name: 'RFC BBBB <draft-string>',
          ed: {
            id: 2,
            name: 'K. Strawberry'
          }
        }
      ]
  }
})

// DATA

const columns = computed(() => {
  const cols = [
    {
      key: 'ed',
      label: 'Managing Editor',
      field: 'ed',
      format: (v) => v.name,
      link: (row, val) => `/team/${val}`
    },
    {
      key: 'name',
      label: 'Document',
      field: 'name',
      classes: 'text-sm font-medium',
      link: row => `/docs/${row.name}`
    }
  ]
  if (currentTab.value === 'inprogress') {
    cols.push({
      key: 'ah',
      label: 'Action Holder',
      field: 'ah',
      classes: 'text-sm font-medium'
    })
  }
  return cols
})

const tabs = [
  { id: 'inprogress', name: 'In progress', to: '/auth48/inprogress', icon: 'uil:bolt-alt' },
  { id: 'done', name: 'AUTH48 Done', to: '/auth48/done', icon: 'solar:verified-check-linear' },
  { id: 'forpub', name: 'For PUB', to: '/auth48/forpub', icon: 'solar:file-smile-linear' }
]
</script>
