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
            <td><RpcLabel :label="labelById[stat.labelId]"/></td>
            <td>{{ documentById[stat.documentId]?.name }}</td>
            <td>{{ stat.seconds }} seconds</td>
        </tr>
    </tbody>
  </table>
</template>

<script setup>

const api = useApi()

// COMPUTED

const labelById = computed(() => Object.fromEntries(labels?.value.map(lbl => [lbl.id, lbl])))

const documentById = computed(() => Object.fromEntries(documents?.value.map(doc => [doc.id, doc])))

// DATA

const { data: labels, pending: labelsPending } = await useAsyncData(() => api.labelsList(), { server: false, default: () => [] })

const { data: documents, pending: documentsPending } = await useAsyncData(() => api.documentsList(), { server: false, default: () => [] })

const { data: labelStats, pending: labelStatsPending } = await useAsyncData(() => api.statsLabels(), { server: false, default: () => [] })

</script>
