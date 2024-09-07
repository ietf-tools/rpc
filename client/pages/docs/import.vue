<template>
  <TitleBlock
    class="pb-3"
    :title="`Add Document: ${submission?.name || '&hellip;'}`"
    summary="Pull the submission into the queue so the editing process can begin."/>
  <form>
    <div v-if="!backendPending" class="space-y-12">
      <div class="border-b border-gray-900/10 pb-12">
        <h2 class="text-base font-semibold leading-7 text-gray-900">Document Info</h2>

        <!-- DRAFT INFO SUMMARY -->
        <div class="overflow-hidden max-w-xl rounded-lg bg-white shadow">
          <div class="px-4 py-5 sm:p-2">
            <ul class="px-2">
              <li>
                <NuxtLink
                  v-if="submission?.datatrackerUrl"
                  :to="submission.datatrackerUrl"
                  class="text-violet-900 hover:text-violet-500 dark:text-violet-300 hover:dark:text-violet-100">
                  {{ submission?.name }}-{{ submission?.rev }}
                </NuxtLink>
                <span v-else>
                  {{ submission?.name }}-{{ submission?.rev }}
                </span>
              </li>
              <li><span v-for="auth of submission?.authors" class="pr-2 ">{{ auth.plainName }}</span></li>
              <li>Submitted pages: {{ submission?.pages }}</li>
              <li>Document shepherd: {{ submission?.shepherd }}</li>
              <li>Stream: {{ submission?.stream.name }}</li>
              <li>Submitted standard level: {{ submission?.stdLevel?.name }}</li>
              <li>Submitted format: {{ submission?.sourceFormat.name }}</li>
            </ul>
          </div>
        </div>

        <!-- Source Format -->
        <div class="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
          <div class="sm:col-span-4">
            <HeadlessListbox v-model="state.sourceFormat" as="div" by="slug">
              <HeadlessListboxLabel class="block text-sm font-medium leading-6 text-gray-900">Source Format
              </HeadlessListboxLabel>
              <div class="relative mt-2">
                <HeadlessListboxButton
                  class="relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-10 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-600 sm:text-sm sm:leading-6">
                  <span class="block truncate">{{ state.sourceFormat?.name || 'Select&hellip;' }}</span>
                  <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                    <Icon name="heroicons:chevron-up-down-solid" class="h-5 w-5 text-gray-400" aria-hidden="true"/>
                  </span>
                </HeadlessListboxButton>

                <transition
                  leave-active-class="transition ease-in duration-100" leave-from-class="opacity-100"
                  leave-to-class="opacity-0">
                  <HeadlessListboxOptions
                    class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                    <HeadlessListboxOption
                      v-for="fmtChoice in sourceFormatChoices" :key="fmtChoice.slug" v-slot="{ active, selected }"
                      as="template" :value="fmtChoice">
                      <li
                        :class="[active ? 'bg-indigo-600 text-white' : 'text-gray-900', 'relative cursor-default select-none py-2 pl-8 pr-4']">
                        <span :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate']">{{
                            fmtChoice.name
                          }}</span>
                        <p :class="[active ? 'text-indigo-200' : 'text-gray-500', 'ml-2']">{{ fmtChoice.desc }}</p>

                        <span
                          v-if="selected"
                          :class="[active ? 'text-white' : 'text-indigo-600', 'absolute inset-y-0 left-1 flex items-center pr-1.5']">
                          <Icon name="heroicons:check" class="h-5 w-5" aria-hidden="true"/>
                        </span>
                      </li>
                    </HeadlessListboxOption>
                  </HeadlessListboxOptions>
                </transition>
              </div>
            </HeadlessListbox>
          </div>
        </div>

        <!-- Stream -->
        <div class="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
          <div class="sm:col-span-4">
            <HeadlessListbox v-model="state.stream" as="div" by="slug">
              <HeadlessListboxLabel class="block text-sm font-medium leading-6 text-gray-900">Stream
              </HeadlessListboxLabel>
              <div class="relative mt-2">
                <HeadlessListboxButton
                  class="relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-10 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-600 sm:text-sm sm:leading-6">
                  <span class="block truncate">{{ state.stream?.name || 'Select&hellip;' }}</span>
                  <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                    <Icon name="heroicons:chevron-up-down-solid" class="h-5 w-5 text-gray-400" aria-hidden="true"/>
                  </span>
                </HeadlessListboxButton>

                <transition
                  leave-active-class="transition ease-in duration-100" leave-from-class="opacity-100"
                  leave-to-class="opacity-0">
                  <HeadlessListboxOptions
                    class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                    <HeadlessListboxOption
                      v-for="streamChoice in streamChoices" :key="streamChoice.slug" v-slot="{ active, selected }"
                      as="template" :value="streamChoice">
                      <li
                        :class="[active ? 'bg-indigo-600 text-white' : 'text-gray-900', 'relative cursor-default select-none py-2 pl-8 pr-4']">
                        <span :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate']">{{
                            streamChoice.name
                          }}</span>
                        <p :class="[active ? 'text-indigo-200' : 'text-gray-500', 'ml-2']">{{ streamChoice.desc }}</p>

                        <span
                          v-if="selected"
                          :class="[active ? 'text-white' : 'text-indigo-600', 'absolute inset-y-0 left-1 flex items-center pr-1.5']">
                          <Icon name="heroicons:check" class="h-5 w-5" aria-hidden="true"/>
                        </span>
                      </li>
                    </HeadlessListboxOption>
                  </HeadlessListboxOptions>
                </transition>
              </div>
            </HeadlessListbox>
          </div>
        </div>

        <!-- Standard Level -->
        <div class="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
          <div class="sm:col-span-4">
            <HeadlessListbox v-model="state.stdLevel" as="div" by="slug">
              <HeadlessListboxLabel class="block text-sm font-medium leading-6 text-gray-900">Standard Level
              </HeadlessListboxLabel>
              <div class="relative mt-2">
                <HeadlessListboxButton
                  class="relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-10 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-600 sm:text-sm sm:leading-6">
                  <span class="block truncate">{{ state.stdLevel?.name || 'Select&hellip;' }}</span>
                  <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                    <Icon name="heroicons:chevron-up-down-solid" class="h-5 w-5 text-gray-400" aria-hidden="true"/>
                  </span>
                </HeadlessListboxButton>

                <transition
                  leave-active-class="transition ease-in duration-100" leave-from-class="opacity-100"
                  leave-to-class="opacity-0">
                  <HeadlessListboxOptions
                    class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                    <HeadlessListboxOption
                      v-for="stdLevChoice in stdLevelChoices" :key="stdLevChoice.slug"
                      v-slot="{ active, selected }" as="template" :value="stdLevChoice">
                      <li
                        :class="[active ? 'bg-indigo-600 text-white' : 'text-gray-900', 'relative cursor-default select-none py-2 pl-8 pr-4']">
                        <span :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate']">{{
                            stdLevChoice.name
                          }}</span>
                        <p :class="[active ? 'text-indigo-200' : 'text-gray-500', 'ml-2']">{{ stdLevChoice.desc }}</p>

                        <span
                          v-if="selected"
                          :class="[active ? 'text-white' : 'text-indigo-600', 'absolute inset-y-0 left-1 flex items-center pr-1.5']">
                          <Icon name="heroicons:check" class="h-5 w-5" aria-hidden="true"/>
                        </span>
                      </li>
                    </HeadlessListboxOption>
                  </HeadlessListboxOptions>
                </transition>
              </div>
            </HeadlessListbox>
          </div>
        </div>

        <!-- TLP Boilerplate -->
        <div class="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
          <div class="sm:col-span-4">
            <HeadlessListbox v-model="state.boilerplate" as="div" by="slug">
              <HeadlessListboxLabel class="block text-sm font-medium leading-6 text-gray-900">TLP Boilerplate
              </HeadlessListboxLabel>
              <div class="relative mt-2">
                <HeadlessListboxButton
                  class="relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-10 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-600 sm:text-sm sm:leading-6">
                  <span class="block truncate">{{ state.boilerplate?.name || 'Select&hellip;' }}</span>
                  <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                    <Icon name="heroicons:chevron-up-down-solid" class="h-5 w-5 text-gray-400" aria-hidden="true"/>
                  </span>
                </HeadlessListboxButton>

                <transition
                  leave-active-class="transition ease-in duration-100" leave-from-class="opacity-100"
                  leave-to-class="opacity-0">
                  <HeadlessListboxOptions
                    class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                    <HeadlessListboxOption
                      v-for="bpChoice in boilerplateChoices" :key="bpChoice.slug" v-slot="{ active, selected }"
                      as="template" :value="bpChoice">
                      <li
                        :class="[active ? 'bg-indigo-600 text-white' : 'text-gray-900', 'relative cursor-default select-none py-2 pl-8 pr-4']">
                        <span :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate']">{{
                            bpChoice.name
                          }}</span>
                        <p :class="[active ? 'text-indigo-200' : 'text-gray-500', 'ml-2']">{{ bpChoice.desc }}</p>

                        <span
                          v-if="selected"
                          :class="[active ? 'text-white' : 'text-indigo-600', 'absolute inset-y-0 left-1 flex items-center pr-1.5']">
                          <Icon name="heroicons:check" class="h-5 w-5" aria-hidden="true"/>
                        </span>
                      </li>
                    </HeadlessListboxOption>
                  </HeadlessListboxOptions>
                </transition>
              </div>
            </HeadlessListbox>
          </div>
        </div>

        <!-- DEADLINE -->
        <div class="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
          <div class="sm:col-span-4">
            <label for="deadline" class="block text-sm font-medium leading-6 text-gray-900">Deadline</label>
            <div class="mt-2">
              <div
                class="flex rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-600  sm:max-w-md">
                <input
                  id="deadline"
                  v-model="state.deadline"
                  type="date"
                  name="deadline"
                  class="block flex-1 rounded-md border-0 ring-1 ring-inset ring-gray-300 bg-white py-1.5 pl-1 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm sm:leading-6"
                  placeholder="Deadline">
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
                  <RpcLabel v-if="labels" :label="labels.find(l => l.id === lbl)"/>
                </div>
              </div>
            </div>
            <div class="max-w-xl">
              <RpcLabelPicker v-model="state.labels" :labels="labels" item-label="slug"/>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="mt-6 flex items-center justify-end gap-x-6">
      <Button btn-type="cancel">Cancel</Button>
      <Button btn-type="default" :disabled="!haveRequiredValues" @click="importSubmission">Save</Button>
    </div>
  </form>

</template>

<script setup lang="ts">
import { DateTime } from 'luxon'
import humanizeDuration from 'humanize-duration'
import type { SourceFormatName, StdLevelName, StreamName, TlpBoilerplateChoiceName } from '~/rpctracker_client'

const route = useRoute()
const api = useApi()
const snackbar = useSnackbar()
const currentTime = useCurrentTime()

const today = computed(() => currentTime.value.startOf('day'))

type State = {
  boilerplate: TlpBoilerplateChoiceName | null,
  sourceFormat: SourceFormatName | null,
  stdLevel: StdLevelName | null,
  stream: StreamName | null,
  deadline: string | null,
  labels: number[]
}

const state = reactive<State>({
  boilerplate: null,
  sourceFormat: null,
  stdLevel: null,
  stream: null,
  deadline: today.value.plus({ weeks: 6 }).toISODate(),
  labels: []
})

// COMPUTED

const submission = computed(() => fetchedData?.value?.submission)
const boilerplateChoices = computed(() => fetchedData?.value?.boilerplateChoices)
const sourceFormatChoices = computed(() => fetchedData?.value?.sourceFormatChoices)
const stdLevelChoices = computed(() => fetchedData?.value?.stdLevelChoices)
const streamChoices = computed(() => fetchedData?.value?.streamChoices)

const timeToDeadline = computed(() => {
  try {
    if (state.deadline) {
      const dt = DateTime.fromISO(state.deadline).diff(today.value, 'days')
      return humanizeDuration(
        dt.toMillis(),
        { units: (dt.as('days') < 14) ? ['d'] : ['w', 'd'], round: true }
      )
    }
  } catch {
    return ''
  }
})

const haveRequiredValues = computed(() => Boolean(
  submission.value && state.boilerplate && state.sourceFormat && state.stdLevel && state.stream && state.deadline
))

// FUNCTIONS

async function importSubmission () {
  if (!(submission.value &&
    state.boilerplate &&
    state.sourceFormat &&
    state.stdLevel &&
    state.stream &&
    state.deadline
  )) {
    return
  }
  let imported
  if (!state.deadline) {
    throw Error('state.deadline not available')
  }
  try {
    imported = await api.submissionsImport({
      documentId: submission.value.id,
      createRfcToBe: {
        submittedBoilerplate: state.boilerplate.slug,
        submittedFormat: state.sourceFormat.slug,
        submittedStdLevel: state.stdLevel.slug,
        submittedStream: state.stream.slug,
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

const { data: fetchedData, pending: backendPending } = await useAsyncData(
  'backendFetch',
  async () => {
    try {
      const documentId = Number(route.query.documentId)
      if (!Number.isInteger(documentId)) {
        throw Error('Expected an integer value for documentId')
      }

      // Retrieve the submission, first....
      const submission = await api.submissionsRetrieve({ documentId })
      // ...then the various name choices, which ensures that the backend has created any that
      // were new with this draft.
      const [boilerplateChoices, sourceFormatChoices, stdLevelChoices, streamChoices] = await Promise.all([
        api.tlpBoilerplateChoiceNamesList(),
        api.sourceFormatNamesList(),
        api.stdLevelNamesList(),
        api.streamNamesList()
      ])

      // Initialize the state
      // state.boilerplate = boilerplateChoices ? boilerplateChoices[0] : null
      state.sourceFormat = submission.sourceFormat
      state.stream = submission.stream
      state.stdLevel = submission.stdLevel || stdLevelChoices ? stdLevelChoices[0] : null
      return {
        submission, boilerplateChoices, sourceFormatChoices, stdLevelChoices, streamChoices
      }
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
