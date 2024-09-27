<template>
  <Card>
    <template #header>
      <h3 class="text-base font-semibold">Complexity Checks</h3>
    </template>

    <fieldset>
      <RpcCheckbox
        v-for="capability in capabilities"
        :key="capability.slug"
        :label="capability.name"
        :desc="capability.desc"/>
    </fieldset>
  </Card>

</template>

<script setup lang="ts">

import type { Capability, RfcToBe } from '~/rpctracker_client'

type Props = {
  capabilities: Capability[]
  rfcToBe: RfcToBe
}

defineProps<Props>()

</script>
