<template>
  <HeadlessTransitionRoot as="template" :show="isShown">
    <HeadlessDialog as="div" class="relative z-50" :initialFocus="nameIpt" @close="close">
      <HeadlessTransitionChild as="template" enter="ease-in-out duration-500" enter-from="opacity-0" enter-to="opacity-100" leave="ease-in-out duration-500" leave-from="opacity-100" leave-to="opacity-0">
        <div class="fixed inset-0 bg-gray-500 dark:bg-black bg-opacity-75 dark:bg-opacity-50 transition-opacity" />
      </HeadlessTransitionChild>
      <div class="fixed inset-0 overflow-hidden">
        <div class="absolute inset-0 overflow-hidden">
          <div class="pointer-events-none fixed inset-y-0 right-0 flex max-w-full pl-10 sm:pl-16">
            <HeadlessTransitionChild as="template" enter="transform transition ease-in-out duration-500 sm:duration-700" enter-from="translate-x-full" enter-to="translate-x-0" leave="transform transition ease-in-out duration-500 sm:duration-700" leave-from="translate-x-0" leave-to="translate-x-full">
              <HeadlessDialogPanel class="pointer-events-auto w-screen max-w-2xl">
                <form @submit.prevent="createUser" class="flex h-full flex-col divide-y divide-gray-200 bg-white dark:bg-neutral-800 shadow-xl">
                  <div class="h-0 flex-1 overflow-y-auto">

                    <!-- Header -->
                    <div class="bg-violet-700 bg-gradient-to-tr from-violet-800 to-violet-600 px-4 py-6 sm:px-6">
                      <div class="flex items-center justify-between">
                        <HeadlessDialogTitle class="text-base font-semibold leading-6 text-white">Import a Submission</HeadlessDialogTitle>
                        <div class="ml-3 flex h-7 items-center">
                          <button type="button" class="relative rounded-md bg-violet-700 text-violet-200 hover:text-white focus:outline-none focus:ring-2 focus:ring-white" @click="close">
                            <span class="absolute -inset-2.5" />
                            <span class="sr-only">Close panel</span>
                            <Icon name="uil:times" class="h-6 w-6" aria-hidden="true" />
                          </button>
                        </div>
                      </div>
                      <div class="mt-1">
                        <p class="text-sm text-violet-300">Fill in the information below to begin RPC processing of an I-D.</p>
                      </div>
                    </div>

                    <!-- Divider container -->
                    <div class="space-y-6 py-6 sm:space-y-0 sm:divide-y sm:divide-gray-200 dark:sm:divide-neutral-600 sm:py-0">
                      <!-- I-D Selector (input goes away when dialog opens per-I-D?)  -->
                      <div class="space-y-2 px-4 sm:grid sm:grid-cols-3 sm:gap-4 sm:space-y-0 sm:px-6 sm:py-5">
                        <div>
                          <label for="document" class="block text-sm font-medium leading-6 text-gray-900 dark:text-neutral-200 sm:mt-1.5">Draft</label>
                        </div>
                        <div class="sm:col-span-2">
                          <select id="document" name="document" v-model="state.documentId" class="form-select">
                            <option v-for="submission of submissions" :key="submission.id">{{ submission.name }}</option>
                          </select>
                        </div>
                      </div>
                    </div>

                    <!-- Labels -->
                    <div class="space-y-2 px-4 sm:grid sm:grid-cols-3 sm:gap-4 sm:space-y-0 sm:px-6 sm:py-5">
                      <div>
                        <label for="roles" class="block text-sm font-medium leading-6 text-gray-900 dark:text-neutral-200 sm:mt-1.5">
                          Labels
                        </label>
                      </div>
                      <div class="sm:col-span-2">
                        <fieldset>
                          <legend class="sr-only">Labels</legend>
                          <div class="space-y-5">
                            <div v-for="label of labels" :key="label.value" class="relative flex items-start">
                              <div class="flex h-6 items-center">
                                <input :id="`role-${label.value}`"
                                  :aria-describedby="`role-${label.value}-description`"
                                  :name="`role-${label.value}`"
                                  type="checkbox"
                                  :value="label.value"
                                  v-model="state.labelsApplied"
                                  :class="[label.caution ? 'border-rose-300 dark:border-rose-500 text-rose-700 dark:text-rose-700 hover:border-rose-400 focus:ring-rose-600' : 'border-gray-300 dark:border-neutral-500 text-violet-600 dark:text-violet-500 hover:border-violet-400 dark:hover:border-violet-500 focus:ring-violet-600 dark:focus:ring-violet-500', 'h-4 w-4 bg-white dark:bg-neutral-900 rounded border-2']"
                                  />
                              </div>
                              <div class="ml-3 text-sm leading-6">
                                <label :for="`role-${label.value}`" :class="[label.caution ? 'text-rose-800 dark:text-rose-400' : 'text-gray-900 dark:text-neutral-200', 'font-medium']">{{ label.label }}</label>
                                <p :id="`role-${label.value}-description`" :class="[label.caution ? 'text-rose-700 dark:text-rose-500' : 'text-gray-500 dark:text-neutral-400', 'text-xs']">{{ label.description }}</p>
                              </div>
                            </div>
                          </div>
                        </fieldset>
                      </div>
                    </div>

                    <!-- Complexity Checks -->
                    <div class="space-y-2 px-4 sm:grid sm:grid-cols-3 sm:gap-4 sm:space-y-0 sm:px-6 sm:py-5">
                      <div>
                        <label for="roles" class="block text-sm font-medium leading-6 text-gray-900 dark:text-neutral-200 sm:mt-1.5">
                          Complexity Checks
                        </label>
                      </div>
                      <div class="sm:col-span-2">
                        <fieldset>
                          <legend class="sr-only">Capabilities</legend>
                          <div class="space-y-5">
                            <div v-for="cap of capabilities" :key="cap.value" class="relative flex items-start">
                              <div class="flex h-6 items-center">
                                <input :id="`role-${cap.value}`"
                                  :aria-describedby="`role-${cap.value}-description`"
                                  :name="`role-${cap.value}`"
                                  type="checkbox"
                                  :value="cap.value"
                                  v-model="state.capabilitiesNeeded"
                                  :class="[cap.caution ? 'border-rose-300 dark:border-rose-500 text-rose-700 dark:text-rose-700 hover:border-rose-400 focus:ring-rose-600' : 'border-gray-300 dark:border-neutral-500 text-violet-600 dark:text-violet-500 hover:border-violet-400 dark:hover:border-violet-500 focus:ring-violet-600 dark:focus:ring-violet-500', 'h-4 w-4 bg-white dark:bg-neutral-900 rounded border-2']"
                                  />
                              </div>
                              <div class="ml-3 text-sm leading-6">
                                <label :for="`role-${cap.value}`" :class="[cap.caution ? 'text-rose-800 dark:text-rose-400' : 'text-gray-900 dark:text-neutral-200', 'font-medium']">{{ cap.label }}</label>
                                <p :id="`role-${cap.value}-description`" :class="[cap.caution ? 'text-rose-700 dark:text-rose-500' : 'text-gray-500 dark:text-neutral-400', 'text-xs']">{{ cap.description }}</p>
                              </div>
                            </div>
                          </div>
                        </fieldset>
                      </div>
                    </div>
                  </div>

                  <!-- Action buttons -->
                  <div class="flex flex-shrink-0 justify-end px-4 py-4">
                    <button type="button" class="btn-secondary" @click="close">Cancel</button>
                    <button type="submit" class="btn-primary ml-4">Save</button>
                  </div>
                </form>
              </HeadlessDialogPanel>
            </HeadlessTransitionChild>
          </div>
        </div>
      </div>
    </HeadlessDialog>
  </HeadlessTransitionRoot>
  <ConfirmDialog v-model:isShown="state.confirmShown" title="Manager Role Selected" caption="Are you sure you want to create a new team member with the Manager role?" />
</template>

<script setup lang="ts">
// PROPS / EMITS

type Submission = {
  id: string
  name: string
}

type Props = {
  isShown: boolean
  submissions: Submission[]
}

const props = withDefaults(defineProps<Props>(), {
  isShown: false
})

const emit = defineEmits(['update:isShown'])

// DATA

type State = {
  documentId: number
  email: string
  datatracker: string
  timezone: string
  hours: number
  manager: string
  roles: string[]
  confirmShown: boolean
  labelsApplied?: string
  capabilitiesNeeded?: string
}

const state = reactive<State>({
  documentId: 0,
  email: '',
  datatracker: '',
  timezone: process.client ? Intl.DateTimeFormat().resolvedOptions().timeZone : 'America/New_York',
  hours: 20,
  manager: '',
  roles: [],
  confirmShown: false
})

// const managers: string[] = []
// const timezones: string[] = process.client ? Intl.supportedValuesOf('timeZone') : []

type Label = {
  value: string
  label: string
  description: string
  caution?: boolean
}

// todo get these from backend
const capabilities: Label[] = [
  { value: 'clusters-beginner', label: 'Clusters: beginner', description: 'New to working with RFC clusters.' },
  { value: 'codecomp-abnf', label: 'Code components: ABNF', description: 'Can work on ABNF components.' },
  { value: 'codecomp-mib', label: 'Code components: MIB', description: 'Can work on MIB components.' },
  { value: 'codecomp-xml', label: 'Code components: XML', description: 'Can work on XML components.' },
  { value: 'codecomp-yang', label: 'Code components: YANG', description: 'Can work on YANG components.' },
  { value: 'ianaconsid-beginner', label: 'IANA considerations: beginner', description: 'New to IANA considerations.' }
]

// todo get these from backend
const labels: Label[] = [
  { value: 'badversion', label: 'Version mismatch', description: 'Version does not match' },
  { value: 'badfont', label: 'Font issues', description: 'A font problem has been identified.' },
  { value: 'badv3xml', label: 'v3 XML Conv Failed', description: 'Conversion to v3 XML failed.' },
  { value: 'badother', label: 'Other', description: 'A general problem has been identified.' }
]

const nameIpt = ref(null)

// METHODS

function close () {
  if (!state.confirmShown) {
    emit('update:isShown', false)
  }
}

function createUser () {
  if (state.roles.includes('manager')) {
    state.confirmShown = true
  }
}
</script>
