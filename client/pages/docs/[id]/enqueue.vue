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
    </div>
  </Card>
</template>

<script setup lang="ts">

import type { Capability, Label, RfcToBe } from '~/rpctracker_client'

const route = useRoute()
const api = useApi()

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
