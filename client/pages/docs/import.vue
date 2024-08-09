<template>
  <TitleBlock
    class="pb-3"
    :title="`Add Document: ${submission.name}`"
    summary="Pull the submission into the queue so the editing process can begin."/>
  <form>
    <div class="space-y-12">
      <div class="border-b border-gray-900/10 pb-12">
        <h2 class="text-base font-semibold leading-7 text-gray-900">Document Info</h2>

        <!-- DRAFT INFO SUMMARY -->
        <div class="overflow-hidden max-w-xl rounded-lg bg-white shadow">
          <div class="px-4 py-5 sm:p-2">
            <ul class="px-2">
              <li>
                <NuxtLink v-if="submission.datatrackerUrl"
                          :to="submission.datatrackerUrl"
                          class="text-violet-900 hover:text-violet-500 dark:text-violet-300 hover:dark:text-violet-100">
                  {{ submission.name }}-{{ submission.rev }}
                </NuxtLink>
                <span v-else>
                  {{ submission.name }}-{{ submission.rev }}
                </span>
              </li>
              <li><span v-for="auth of submission.authors" class="pr-2 ">{{ auth }}</span></li>
              <li>Submitted pages: {{ submission.pages }}</li>
              <li>Document shepherd: {{ submission.shepherd }}</li>
              <li>Stream manager: {{ submission.streamManager }}</li>
              <li>Submitted format: {{ submission.submittedFormat }}</li>
            </ul>
          </div>
        </div>

        <!-- DEADLINE -->
        <div class="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
          <div class="sm:col-span-4">
            <label for="username" class="block text-sm font-medium leading-6 text-gray-900">Deadline</label>
            <div class="mt-2">
              <div class="flex rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-600  sm:max-w-md">
                <input type="date"
                       name="deadline"
                       id="deadline"
                       v-model="state.deadline"
                       class="block flex-1 rounded-md border-0 ring-1 ring-inset ring-gray-300 bg-white py-1.5 pl-1 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm sm:leading-6"
                       placeholder="Deadline" />
              </div>
              <span v-if="timeToDeadline" class="text-sm leading-6 text-gray-500">{{ timeToDeadline }} from today</span>
            </div>
          </div>
        </div>

        <!-- LABELS -->
        <div class="col-span-full">
          <div class="mt-2">
            <div class="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
              <h2 class="text-base font-semibold leading-6 text-gray-900">Labels</h2>
              <div class="flex">
                <div v-for="lbl of state.labels" class="flex-shrink-0 p-1">
                  <RpcLabel :label="labels.find(l => l.id === lbl)"/>
                </div>
              </div>
            </div>
            <div class="max-w-xl">
              <RpcLabelPicker :labels="labels" v-model="state.labels" item-label="slug"/>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="mt-6 flex items-center justify-end gap-x-6">
      <button type="button" class="text-sm font-semibold leading-6 text-gray-900">Cancel</button>
      <button type="button"
              class="rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
              @click="importSubmission">
        Save
      </button>
    </div>
  </form>

</template>

<script setup>
import { DateTime } from 'luxon'
import humanizeDuration from 'humanize-duration'

const route = useRoute()
const api = useApi()
const snackbar = useSnackbar()

const today = DateTime.now().setZone('utc').startOf('day')

const state = reactive({
  deadline: today.plus({ weeks: 6 }).toISODate(),
  labels: []
})

// COMPUTED

const submission = computed(() => dtDraftData.value
  ? {
      datatrackerId: dtDraftData.value.id,
      name: dtDraftData.value.name,
      rev: dtDraftData.value.rev,
      authors: dtDraftData.value.authors.map(a => a.plain_name),
      pages: dtDraftData.value.pages,
      shepherd: 'Dolly Shepherd',
      streamManager: 'Ari Drecker',
      submittedFormat: 'v2',
      datatrackerUrl: `http://localhost:8000/doc/${dtDraftData.value.name}-${dtDraftData.value.rev}/`
    }
  : {}
)

const timeToDeadline = computed(() => {
  try {
    if (state.deadline) {
      const dt = DateTime.fromISO(state.deadline).diff(today, 'days')
      return humanizeDuration(
        dt,
        { units: (dt.as('days') < 14) ? ['d'] : ['w', 'd'], round: true }
      )
    }
  } catch {
    return ''
  }
})

// FUNCTIONS

async function importSubmission () {
  let imported
  try {
    imported = await api.submissionsImport({
      documentId: submission.value.datatrackerId,
      rfcToBe: {
        externalDeadline: DateTime.fromISO(state.deadline, { zone: 'utc' }).toJSDate(),
        labels: state.labels
      }
    })
  } catch (e) {
    snackbar.add({
      type: 'error',
      title: 'Error saving',
      text: e
    })
  }
  if (imported) {
    snackbar.add({
      type: 'success',
      title: 'Success',
      text: 'Document successfully added'
    })
    await navigateTo(`/docs/${imported.name}/`)
  }
}

// DATA

const { data: labels } = await useAsyncData(
  'labels',
  async () => {
    try {
      return await api.labelsList()
    } catch (e) {
      snackbar.add({
        type: 'error',
        title: 'Data fetch not successful',
        text: e
      })
    }
  }, {
    server: false,
    default: () => ([])
  }
)

const { data: dtDraftData } = await useAsyncData(
  'dtDraftData',
  async () => {
    try {
      return await api.submissionsRetrieve({ documentId: route.query.documentId })
    } catch (e) {
      snackbar.add({
        type: 'error',
        title: 'Data fetch not successful',
        text: e
      })
    }
  },
  { server: false }
)
</script>
