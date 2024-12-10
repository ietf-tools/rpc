<template>
  <BaseCard>
    <template #header>
      <CardHeader title="Exceptions"/>
    </template>

    <fieldset>
      <RpcCheckbox
        v-for="exception in exceptionLabels"
        :key="exception.id"
        :label="exception.slug"/>
    </fieldset>
  </BaseCard>
</template>

<script setup lang="ts">
import type { Label } from '~/purple_client'

type Props = { labels: Label[] }

const props = defineProps<Props>()

// COMPUTED

const exceptionLabels = computed(() => props.labels.filter((lbl) => lbl.isException))

</script>
