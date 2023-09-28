<template>
  <table class="min-w-full divide-y divide-gray-300 dark:divide-neutral-600">
    <thead class="bg-gray-50 dark:bg-neutral-800">
      <tr>
        <th class="w-4">&nbsp;</th>
        <th
          v-for="col of columns"
          :key="col.key"
          scope="col"
          class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900 dark:text-neutral-400"
        >
          <a v-if="col.sortable !== false" href="#" @click.prevent="sortBy(col.field)">
            <span>{{ col.label }}</span>
            <template v-if="state.sortField === col.field">
              <Icon v-if="state.sortDirection === 'asc'" name="uil:arrow-up" class="text-lg -mt-0.5" />
              <Icon v-else name="uil:arrow-down" class="text-lg -mt-0.5" />
            </template>
          </a>
          <span v-else>{{ col.label }}</span>
        </th>
      </tr>
    </thead>
    <tbody class="text-sm divide-y divide-gray-200 dark:divide-neutral-700 bg-white dark:bg-neutral-900">
      <tr v-for="row of rows" :key="row[rowKey]">
        <td class="pl-3">
          <Icon name="uil:file-alt" size="1.25rem" class="text-gray-400 dark:text-neutral-500" />
        </td>
        <td
          v-for="col of columns"
          :key="col.key"
          :class="[
            'px-3 py-4 text-gray-500 dark:text-neutral-400',
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
import { isFunction, orderBy } from 'lodash-es'

// PROPS

const props = defineProps({
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

// DATA

const state =  reactive({
  sortField: '',
  sortDirection: 'asc'
})

const rows = computed(() => {
  if (state.sortField) {
    return orderBy(props.data, [state.sortField], [state.sortDirection])
  } else {
    return props.data
  }
})

// METHODS

function sortBy (fieldName) {
  if (state.sortField === fieldName) {
    state.sortDirection = state.sortDirection === 'asc' ? 'desc' : 'asc'
  } else {
    state.sortDirection = 'asc'
  }
  state.sortField = fieldName
}

</script>