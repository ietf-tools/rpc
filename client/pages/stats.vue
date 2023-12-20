<template>
  <table>
    <thead>
    <tr>
      <th>Label</th>
      <th>Document</th>
      <th>Time applied</th>
    </tr>
    </thead>
    <tbody>
    <tr v-for="stat of labelStats.labelStats">
      <td>
        <RpcLabel v-if="labelById.hasOwnProperty(stat.labelId)"
                  :label="labelById[stat.labelId]"/>
        <span v-else>?</span>
      </td>
      <td>{{ documentById[stat.documentId]?.name }}</td>
      <td>
        {{ humanizeDuration(Duration.fromObject({ seconds: stat.seconds }), { largest: 1, round: true}) }}</td>
    </tr>
    </tbody>
  </table>
</template>

<script setup>

import { Duration } from 'luxon'
import humanizeDuration from 'humanize-duration'

const api = useApi()

// COMPUTED

const labelById = computed(() => Object.fromEntries(labels?.value.map(lbl => [lbl.id, lbl])))

const documentById = computed(() => Object.fromEntries(documents?.value.map(doc => [doc.id, doc])))

// DATA

const { data: labels } = await useAsyncData(() => api.labelsList(), { server: false, default: () => [] })

const { data: documents } = await useAsyncData(() => api.documentsList(), { server: false, default: () => [] })

const { data: labelStats } = await useAsyncData(() => api.statsLabels(), { server: false, default: () => [] })

</script>
