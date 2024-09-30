<template>
  <Card>
    <template #header>
      <TitleBlock
        class="pb-3"
        :title="`Prep for Queue: ${rfcToBe?.name || '&hellip;'}`"
        summary="Ready the incoming document for the editing queue."/>
    </template>

    <div class="space-y-12">
      <DocInfoCard :draft="rfcToBe"/>
      <div class="border-b border-gray-900/10 pb-12 flex">
        <DocComplexityCard :capabilities="capabilities"/>
        <DocExceptionsCard :labels="labels"/>
      </div>
      <Card>
        <template #header>
          <h3 class="text-base font-semibold">
            Document Dependencies
          </h3>
        </template>
        <DocumentTable
          :columns="columns"
          :data="relatedDocuments"
          row-key="name"/>
        <Button btn-type="default">Add Dependency</Button>
      </Card>
      <Card>
        <template #header>
          <h3 class="text-base font-semibold">
            Comments
          </h3>
        </template>
        <RpcTextarea/>
      </Card>
    </div>
    <template #footer>
      <Button btn-type="default">Document has exceptions&mdash;escalate</Button>
      <Button btn-type="default">Add to queue</Button>
    </template>
  </Card>
</template>

<script setup lang="ts">

import type { Capability, Label, RfcToBe } from '~/rpctracker_client'
import type { Column } from '~/components/DocumentTableTypes'

const route = useRoute()
const api = useApi()

const columns: Column[] = [
  {
    key: 'name',
    label: 'Document',
    field: 'name',
    classes: 'text-sm font-medium'
  },
  {
    key: 'relationship',
    label: 'Relationship',
    field: 'relationship',
    classes: 'text-sm font-medium'
  },
  {
    key: 'currentState',
    label: 'Current State',
    field: 'currentState',
    classes: 'text-sm font-medium'
  },
]

const relatedDocuments = [
  {
    name: 'draft-some-other-draft',
    relationship: 'Normative Reference',
    currentState: 'Active WG document'
  },
]

const { data: rfcToBe } = await useAsyncData<RfcToBe>(
  'rfcToBe',
  () => api.documentsRetrieve({ draftName: route.params.id.toString() }),
  { server: false }
)

const { data: capabilities } = await useAsyncData<Capability[]>(
  'capabilities',
  () => api.capabilitiesList(),
  { default: () => ([]), server: false }
)

const { data: labels } = await useAsyncData<Label[]>(
  'labels',
  () => api.labelsList(),
  { default: () => ([]), server: false }
)
</script>
