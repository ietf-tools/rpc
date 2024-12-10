<template>
  <BaseCard>
    <template #header>
      <CardHeader title="Complexity Checks"/>
    </template>
    <fieldset>
      <RpcCheckbox
        v-for="capability in capabilities"
        :key="capability.slug"
        :label="capability.name"
        :desc="capability.desc"/>
    </fieldset>
  </BaseCard>
</template>

<script setup lang="ts">

import type { Capability } from '~/purple_client'

type Props = {
  capabilities: Capability[]
}

defineProps<Props>()

</script>
