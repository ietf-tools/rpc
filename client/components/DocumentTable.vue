<template>
  <table class="min-w-full divide-y divide-gray-300 dark:divide-neutral-600">
    <thead class="bg-gray-50 dark:bg-neutral-800">
      <tr>
        <th
          v-for="col of columns"
          :key="col.key"
          scope="col"
          class="px-4 py-3.5 text-left text-sm font-semibold text-gray-900 dark:text-neutral-400"
        >
          {{ col.label }}
        </th>
      </tr>
    </thead>
    <tbody class="text-sm divide-y divide-gray-200 dark:divide-neutral-700 bg-white dark:bg-neutral-900">
      <tr v-for="row of data" :key="row[rowKey]">
        <td
          v-for="col of columns"
          :key="col.key"
          :class="[
            'px-4 py-4 text-gray-500 dark:text-neutral-400',
            col.classes && isFunction(col.classes) ? col.classes(row[col.field]) : col.classes
          ]"
        >
          <NuxtLink
            v-if="col.link"
            :to="col.link(row)"
            class="text-violet-900 hover:text-violet-500 dark:text-violet-300 hover:dark:text-violet-100"
          >
            {{ col.format ? col.format(row[col.field]) : row[col.field] }}
          </NuxtLink>
          <span v-else>{{ col.format ? col.format(row[col.field]) : row[col.field] }}</span>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script setup>
import { isFunction } from 'lodash-es'

// PROPS

defineProps({
  data: {
    type: Array,
    default: () => ([]),
    required: true
  },
  columns: {
    type: Array,
    default: () => ([]),
    required: true
  },
  rowKey: {
    type: String,
    default: 'id'
  }
})


</script>
