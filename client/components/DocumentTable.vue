<template>
  <div>
    <table class="min-w-full divide-y divide-gray-300 dark:divide-neutral-600">
      <thead class="bg-gray-50 dark:bg-neutral-800">
        <tr>
          <th class="pl-3 w-9">&nbsp;</th>
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
      <tbody v-if="!loading" class="text-sm divide-y divide-gray-200 dark:divide-neutral-700 bg-white dark:bg-neutral-900">
        <tr v-for="row of rows" :key="row[rowKey]">
          <td class="pl-3">
            <Icon name="uil:file-alt" size="1.25em" class="text-gray-400 dark:text-neutral-500" />
          </td>
          <td
            v-for="col of columns"
            :key="col.key"
            :class="[
              'px-3 py-4 text-gray-500 dark:text-neutral-400',
              col.classes && isFunction(col.classes) ? col.classes(row[col.field]) : col.classes
            ]"
          >
            <component :is="buildCell(col, row)" />
          </td>
        </tr>
      </tbody>
    </table>
    <div v-if="loading" class="w-full">
      <div class="h-0.5 w-full bg-emerald-100 dark:bg-emerald-900 overflow-hidden">
        <div class="progress w-full h-full bg-emerald-500 left-right" />
      </div>
    </div>
    <div
      v-if="!data || data.length < 1"
      class="p-8 text-sm bg-white dark:bg-neutral-900 text-gray-500 dark:text-neutral-400"
    >
      <Icon v-if="loading" name="ei:spinner-3" size="1.5em" class="animate-spin mr-2" />
      <em>{{ loading ? 'Fetching data...' : 'No documents to display.' }}</em>
    </div>
  </div>
</template>

<script setup>
import { Label, Icon, NuxtLink } from '#components'
import { isArray, isFunction, orderBy } from 'lodash-es'

// PROPS

const props = defineProps({
  /**
   * Rows to display
   */
  data: {
    type: Array,
    default: () => ([])
  },
  /**
   * Column definitions
   */
  columns: {
    type: Array,
    default: () => ([]),
    required: true
  },
  /**
   * The property to use as the unique key for each row
   */
  rowKey: {
    type: String,
    default: 'id'
  },
  /**
   * Whether to show the loading animation or not
   */
  loading: {
    type: Boolean,
    default: false
  }
})

// DATA

const state = reactive({
  sortField: '',
  sortDirection: 'asc'
})

const rows = computed(() => {
  if (!props.data) { return [] }
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

/**
 * Build cell node
 *
 * @param {Object} col Column properties
 * @param {Object} row Current row object
 */
function buildCell (col, row) {
  const values = isArray(row[col.field]) ? row[col.field] : [row[col.field]]
  const formattedValues = col.format ? values.map(v => col.format(v)) : values
  const children = []

  const isLink = isFunction(col.link)

  for (const [idx, val] of formattedValues.entries()) {
    const contents = [h('span', val)]
    const cssClasses = []
    if (col.icon) {
      contents.unshift(
        h(Icon, {
          name: col.icon,
          size: '1.1rem',
          class: 'mr-2',
          'aria-hidden': 'true'
        })
      )
      cssClasses.push('flex items-center')
    }

    if (isLink) {
      children.push(h(NuxtLink, {
        class: [
          ...cssClasses,
          'text-violet-900 hover:text-violet-500 dark:text-violet-300 hover:dark:text-violet-100'
        ],
        to: col.link(row, val)
      }, () => contents))
    } else {
      children.push(h('span', {
        class: cssClasses
      }, contents))
    }

    if (idx < formattedValues.length - 1) {
      children.push(h('span', ', '))
    }
  }

  if (isFunction(col.labels)) {
    for (const lbl of transformLabels(col.labels(row), col.labelDefaultColor ?? 'violet')) {
      children.push(h(Label, { label: lbl }))
    }
  }

  return h('div', children)
}

/**
 * Handle labels array in either string or object format
 *
 * @param {Array} val Array of labels
 * @param {String} defaultColor Default color name
 */
function transformLabels (val, defaultColor) {
  return val.map(item => {
    if (typeof item === 'string') {
      return {
        label: item,
        color: defaultColor
      }
    } else {
      return item
    }
  })
}

</script>

<style>
.progress {
  animation: progress 1s infinite linear;
}

.left-right {
  transform-origin: 0% 50%;
}
@keyframes progress {
  0% {
    transform: translateX(0) scaleX(0);
  }
  40% {
    transform: translateX(0) scaleX(0.4);
  }
  100% {
    transform: translateX(100%) scaleX(0.5);
  }
}
</style>

<docs>
## Column Definition

The `columns` property is an arrow of objects with the following possible options:

| Option | Type | Description | Required |
|---|---|---|:-:|
| `key` | *String* | Unique ID for the column | ✅ |
| `label` | *String* | Column title | ✅ |
| `field` | *String* | Row property to use / sort on | ✅ |
| `format` | *Function* | Optional lambda function to transform the cell value. e.g. `(val) => val.toLowerCase()` |
| `link` | *Function* | Lambda function that returns a URL. The value will be displayed as clickable link. `(row, val) => val.personUrl` |
| `icon` | *String* | If defined, the name of the icon to display to the left of the value. See the [Iconify reference](https://icon-sets.iconify.design/) for all possible options. |
| `labels` | *Array \| Function* | Either an array or a lambda function (e.g. `row => row.labels`) that return an array of / a mix of:<br>- strings *(the `labelDefaultColor` will be used)*<br>- an object `{ label: 'something', color: 'rose' }` |
| `labelDefaultColor` | *String* | The fallback color name to use for a label when not explicitly provided. Any of the [TailwindCSS color names](https://tailwindcss.com/docs/customizing-colors), in lowercase. e.g. `purple` |
| `classes` | *String \| Function* | List of space separated CSS classes to apply to the cell, or a lambda function e.g. `(row) => row.fooBar` |
| `sortable` | *Boolean* | Whether the column can be sorted or not. Defaults to `true`. | |
</docs>
