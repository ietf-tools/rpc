<template>
  <TitleBlock title="Manage Assignments">
    <template #right>
      <button type="button" class="btn-secondary mr-3">
        <span class="sr-only">Refresh</span>
        <Icon name="solar:refresh-line-duotone" size="1.5em" @click="refresh"
              :class="[pending ? 'animate-spin text-orange-600' : 'text-gray-500 dark:text-neutral-300']"
              aria-hidden="true"/>
      </button>
    </template>
  </TitleBlock>

  <div class="mt-8 flow-root">
    <h2>Documents for assignment</h2>
    <DocumentCards :documents="documents"
                   @assign-editor-to-document="(dId, edId) => saveAssignment({rfcToBeId: dId, personId: edId})"
                   @delete-assignment="deleteAssignment"
                   @selection-changed="doc => state.selectedDoc = doc"/>
    <EditorPalette :editors="editors?.toSorted(compareEditors)"/>
  </div>
</template>

<script setup>
import { DateTime } from 'luxon'

const csrf = useCookie('csrftoken', { sameSite: 'strict' })

const state = reactive({ selectedDoc: null })

const teamPagesPerHour = 1.0

// COMPUTED

const pending = computed(() => pendingPeople?.value || pendingDocs?.value || pendingAssignments?.value)
const cookedAssignments = computed(() => assignments.value?.map(a => ({
  ...a,
  // person is a Person id - replace it with person details
  person: people.value?.find(ed => ed.id === a.person)
})))

const documents = computed(() => rfcsToBe.value?.map((rtb) => ({
  ...rtb,
  // augment with assignments
  assignments: cookedAssignments.value?.filter(a => a.rfc_to_be === rtb.id)
})).sort(rtb => rtb.external_deadline))

const editors = computed(() => {
  const now = DateTime.now()
  return people.value?.map(person => ({
    ...person,
    assignments: assignments.value?.filter(a => a.person === person.id),
    completeBy: (
      state.selectedDoc
        ? now.plus({ days: 7 * state.selectedDoc.pages / teamPagesPerHour / person.hours_per_week })
        : null
    )
  }))
})

// METHODS

async function saveAssignment (assignment) {
  await $fetch('/api/rpc/assignments/', {
    body: {
      rfc_to_be: assignment.rfcToBeId,
      person: assignment.personId,
      role: 'first_editor'
    },
    method: 'POST',
    headers: { 'X-CSRFToken': csrf.value }
  })
  await refresh()
}

// Order editors for display
function compareEditors (a, b) {
  const comparisons = ['completeBy', 'name'].map(attr => {
    const aval = a[attr]
    const bval = b[attr]
    return (aval < bval) ? -1 : ((aval > bval) ? 1 : 0)
  })
  return comparisons.find(c => c !== 0) ?? 0
}

async function deleteAssignment (assignment) {
  await $fetch(`/api/rpc/assignments/${assignment.id}`, {
    method: 'DELETE',
    headers: { 'X-CSRFToken': csrf.value }
  })
  await refresh()
}

async function refresh () {
  const promises = []
  refreshPeople && promises.push(refreshPeople())
  refreshDocs && promises.push(refreshDocs())
  refreshAssignments && promises.push(refreshAssignments())
  await Promise.allSettled(promises)
}

// DATA RETRIEVAL

const { data: people, pending: pendingPeople, refresh: refreshPeople } = await useFetch('/api/rpc/rpc_person/', { baseURL: '/', server: false })
const { data: rfcsToBe, pending: pendingDocs, refresh: refreshDocs } = await useFetch('/api/rpc/documents/', { baseURL: '/', server: false })
const {
  data: assignments,
  pending: pendingAssignments,
  refresh: refreshAssignments
} = await useFetch('/api/rpc/assignments/', { baseURL: '/', server: false })

</script>
