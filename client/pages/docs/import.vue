<template>
  <TitleBlock
    class="pb-3"
    :title="`Add Document: ${submission?.name}`"
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
                <NuxtLink v-if="submission?.datatrackerUrl"
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
              <li>Submitted standard level: {{ submission?.stdLevel.name }}</li>
              <li>Submitted format: {{ submission?.sourceFormat.name }}</li>
            </ul>
          </div>
        </div>

        <!-- Source Format -->
        <div class="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
          <div class="sm:col-span-4">
            <HeadlessListbox as="div" v-model="state.sourceFormatSlug">
              <HeadlessListboxLabel class="block text-sm font-medium leading-6 text-gray-900">Source Format</HeadlessListboxLabel>
              <div class="relative mt-2">
                <HeadlessListboxButton class="relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-10 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-600 sm:text-sm sm:leading-6">
                  <span class="block truncate">{{ state.sourceFormatSlug }}</span>
                  <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                    <Icon name="heroicons:chevron-up-down-solid" class="h-5 w-5 text-gray-400" aria-hidden="true"/>
                  </span>
                </HeadlessListboxButton>

                <transition leave-active-class="transition ease-in duration-100" leave-from-class="opacity-100" leave-to-class="opacity-0">
                  <HeadlessListboxOptions class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                    <HeadlessListboxOption as="template" v-for="fmtChoice in sourceFormatChoices" :key="fmtChoice.slug" :value="fmtChoice.slug" v-slot="{ active, selected }">
                      <li :class="[active ? 'bg-indigo-600 text-white' : 'text-gray-900', 'relative cursor-default select-none py-2 pl-8 pr-4']">
                        <span :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate']">{{ fmtChoice.slug }}</span>
                        <p :class="[active ? 'text-indigo-200' : 'text-gray-500', 'ml-2']">{{ fmtChoice.desc }}</p>

                        <span v-if="selected" :class="[active ? 'text-white' : 'text-indigo-600', 'absolute inset-y-0 left-1 flex items-center pr-1.5']">
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
            <HeadlessListbox as="div" v-model="state.streamSlug">
              <HeadlessListboxLabel class="block text-sm font-medium leading-6 text-gray-900">Stream</HeadlessListboxLabel>
              <div class="relative mt-2">
                <HeadlessListboxButton class="relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-10 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-600 sm:text-sm sm:leading-6">
                  <span class="block truncate">{{ state.streamSlug }}</span>
                  <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                    <Icon name="heroicons:chevron-up-down-solid" class="h-5 w-5 text-gray-400" aria-hidden="true"/>
                  </span>
                </HeadlessListboxButton>

                <transition leave-active-class="transition ease-in duration-100" leave-from-class="opacity-100" leave-to-class="opacity-0">
                  <HeadlessListboxOptions class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                    <HeadlessListboxOption as="template" v-for="streamChoice in streamChoices" :key="streamChoice.slug" :value="streamChoice.slug" v-slot="{ active, selected }">
                      <li :class="[active ? 'bg-indigo-600 text-white' : 'text-gray-900', 'relative cursor-default select-none py-2 pl-8 pr-4']">
                        <span :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate']">{{ streamChoice.slug }}</span>
                        <p :class="[active ? 'text-indigo-200' : 'text-gray-500', 'ml-2']">{{ streamChoice.desc }}</p>

                        <span v-if="selected" :class="[active ? 'text-white' : 'text-indigo-600', 'absolute inset-y-0 left-1 flex items-center pr-1.5']">
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
            <HeadlessListbox as="div" v-model="state.stdLevelSlug">
              <HeadlessListboxLabel class="block text-sm font-medium leading-6 text-gray-900">Standard Level</HeadlessListboxLabel>
              <div class="relative mt-2">
                <HeadlessListboxButton class="relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-10 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-600 sm:text-sm sm:leading-6">
                  <span class="block truncate">{{ state.stdLevelSlug }}</span>
                  <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                    <Icon name="heroicons:chevron-up-down-solid" class="h-5 w-5 text-gray-400" aria-hidden="true"/>
                  </span>
                </HeadlessListboxButton>

                <transition leave-active-class="transition ease-in duration-100" leave-from-class="opacity-100" leave-to-class="opacity-0">
                  <HeadlessListboxOptions class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                    <HeadlessListboxOption as="template" v-for="stdLevChoice in stdLevelChoices" :key="stdLevChoice.slug" :value="stdLevChoice.slug" v-slot="{ active, selected }">
                      <li :class="[active ? 'bg-indigo-600 text-white' : 'text-gray-900', 'relative cursor-default select-none py-2 pl-8 pr-4']">
                        <span :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate']">{{ stdLevChoice.slug }}</span>
                        <p :class="[active ? 'text-indigo-200' : 'text-gray-500', 'ml-2']">{{ stdLevChoice.desc }}</p>

                        <span v-if="selected" :class="[active ? 'text-white' : 'text-indigo-600', 'absolute inset-y-0 left-1 flex items-center pr-1.5']">
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
            <HeadlessListbox as="div" v-model="state.submittedBoilerplateSlug">
              <HeadlessListboxLabel class="block text-sm font-medium leading-6 text-gray-900">TLP Boilerplate</HeadlessListboxLabel>
              <div class="relative mt-2">
                <HeadlessListboxButton class="relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-10 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-600 sm:text-sm sm:leading-6">
                  <span class="block truncate">{{ state.submittedBoilerplateSlug }}</span>
                  <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                    <Icon name="heroicons:chevron-up-down-solid" class="h-5 w-5 text-gray-400" aria-hidden="true"/>
                  </span>
                </HeadlessListboxButton>

                <transition leave-active-class="transition ease-in duration-100" leave-from-class="opacity-100" leave-to-class="opacity-0">
                  <HeadlessListboxOptions class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                    <HeadlessListboxOption as="template" v-for="bpChoice in boilerplateChoices" :key="bpChoice.slug" :value="bpChoice.slug" v-slot="{ active, selected }">
                      <li :class="[active ? 'bg-indigo-600 text-white' : 'text-gray-900', 'relative cursor-default select-none py-2 pl-8 pr-4']">
                        <span :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate']">{{ bpChoice.slug }}</span>
                        <p :class="[active ? 'text-indigo-200' : 'text-gray-500', 'ml-2']">{{ bpChoice.desc }}</p>

                        <span v-if="selected" :class="[active ? 'text-white' : 'text-indigo-600', 'absolute inset-y-0 left-1 flex items-center pr-1.5']">
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
                  <RpcLabel v-if="labels" :label="labels.find(l => l.id === lbl)"/>
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

<script setup lang="ts">
import { DateTime } from 'luxon'
import humanizeDuration from 'humanize-duration'

const route = useRoute()
const api = useApi()
const snackbar = useSnackbar()

const today = DateTime.now().setZone('utc').startOf('day')

type State = {
  submittedBoilerplateSlug: string,
  sourceFormatSlug: string,
  stdLevelSlug: string,
  streamSlug: string,
  deadline: string | null,
  labels: number[]
}

const state = reactive<State>({
  submittedBoilerplateSlug: 'trust200902',
  sourceFormatSlug: 'xml-v2',
  stdLevelSlug: 'ps',
  streamSlug: 'ietf',
  deadline: today.plus({ weeks: 6 }).toISODate(),
  labels: []
})

// COMPUTED

const timeToDeadline = computed(() => {
  try {
    if (state.deadline) {
      const dt = DateTime.fromISO(state.deadline).diff(today, 'days')
      return humanizeDuration(
        dt.toMillis(),
        { units: (dt.as('days') < 14) ? ['d'] : ['w', 'd'], round: true }
      )
    }
  } catch {
    return ''
  }
})

// FUNCTIONS

async function importSubmission () {
  if (!submission?.value || !state.deadline) {
    return
  }
  let imported
  try {
    imported = await api.submissionsImport({
      documentId: submission.value.id,
      createRfcToBe: {
        submittedFormat: state.sourceFormatSlug,
        submittedBoilerplate: state.submittedBoilerplateSlug,
        submittedStdLevel: state.stdLevelSlug,
        submittedStream: state.streamSlug,
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

const { data: submission } = await useAsyncData(
  'submission',
  async () => {
    try {
      const { documentId } = route.query
      // This check fails and prevents the page from loading
      // if (typeof documentId !== 'number') {
      //   throw Error('Expected documentId')
      // }
      return await api.submissionsRetrieve({ documentId })
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

const { data: boilerplateChoices } = await useAsyncData(
  'boilerplateChoices',
  async () => {
    try {
      return await api.tlpBoilerplateChoiceNamesList()
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

const { data: sourceFormatChoices } = await useAsyncData(
  'sourceFormatChoices',
  async () => {
    try {
      return await api.sourceFormatNamesList()
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

const { data: stdLevelChoices } = await useAsyncData(
  'stdLevelChoices',
  async () => {
    try {
      return await api.stdLevelNamesList()
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

const { data: streamChoices } = await useAsyncData(
  'streamChoices',
  async () => {
    try {
      return await api.streamNamesList()
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
</script>
