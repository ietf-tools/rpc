<template>
  <BaseCard>
    <template #header>
      <h3 class="text-base font-semibold">Exceptions</h3>
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
import type { Label } from '~/rpctracker_client'

type Props = { labels: Label[] }

const props = defineProps<Props>()

// COMPUTED

const exceptionLabels = computed(() => props.labels.filter((lbl) => lbl.isException))

</script>
