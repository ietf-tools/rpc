<!-- Document Cards
Based on https://tailwindui.com/components/application-ui/lists/grid-lists#component-2beafc928684743ff886c0b164edb126
-->
<template>
  <ul role="list" class="grid grid-cols-1 gap-x-6 gap-y-8 lg:grid-cols-3 xl:gap-x-8">
    <DocumentCard
      v-for="doc of props.documents"
      :document="doc"
      :editors="props.editors"
      :selected="state.selectedDoc?.id === doc.id"
      :editorAssignedDocuments="editorAssignedDocuments"
    />
  </ul>
</template>

<script setup>
import { provide } from 'vue'

const props = defineProps({
  documents: Array,
  editors: Array
})

const state = reactive({
  selectedDoc: null
})

const emit = defineEmits(['assignEditorToDocument', 'deleteAssignment', 'selectionChanged'])

provide('assignEditor', (doc, editor) => emit('assignEditorToDocument', doc, editor))
provide('deleteAssignment', (assignment) => emit('deleteAssignment', assignment))

const editorAssignedDocuments = computed(() =>
  props.documents.reduce((document, editorAssignedDocuments) => {
    document.assignments?.forEach(assignment => {
      const editorId = assignment.person.id
      if (!editorAssignedDocuments[editorId]) {
        editorAssignedDocuments[editorId] = []
      }
      if (!editorAssignedDocuments[editorId].find(
        existingDocument => existingDocument.id === document.id
      )) {
        editorAssignedDocuments[editorId].push(document)
      }
    })
    return editorAssignedDocuments
  }, {})
)

</script>
