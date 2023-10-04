<template>
  <TitleBlock title="Manage Unassigned Documents"/>

  <div class="mt-8 flow-root">
    <h2>Documents for assignment</h2>
    <div v-for="doc of documents" :key="item.id"
         class="w-full max-w-5xl p-4 bg-white border border-gray-200 rounded-lg shadow sm:p-6 md:p-8 dark:bg-gray-800 dark:border-gray-700">
      <div class="space-y-1">
        <h5 class="text-xl font-medium text-gray-900 dark:text-white">{{ doc.name }}</h5>
        <div>{{ doc.title }}</div>
        <div>Labels here</div>
        <div>Pages: {{ doc.pages }}</div>
        <div>View Notes (with count)</div>

        <label :for="'editor' + doc.id" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Assign
          editor</label>
        <select :id="'editor' + doc.id"
                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
          <option selected>Leave unassigned</option>
          <option v-for="editor of editors" :key="editor.id" value="editor.id">
            {{ editor.short_name }} - {{ editor.summary }}
          </option>
        </select>

      </div>
    </div>
  </div>
</template>

<script setup>
const documents = [
  { id: 1, name: 'draft-ietf-fat-cat-03', title: 'The Fat Cat Sat on the Hat', pages: 98 },
  { id: 2, name: 'draft-ietf-dog-skinny-04', title: 'The Skinny Brown Dog Jumped Over the Lazy Fox', pages: 10 }
]

const editors = [
  { id: 1, short_name: 'atravis', summary: 'could complete by 2023-06-06' },
  { id: 2, short_name: 'kfield', summary: '2 AUTH48 open' }
]
/**
 * Todo
 * - retrieve data
 * - update assignments on the fly
 * - submit changes (first POST api endpoint)
 * - think about how much of the useful info we can reasonably calculate (do we have rates, vacation info, etc?)
 */
</script>
