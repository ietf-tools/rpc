<template>
  <form @submit.prevent="createUser" class="flex h-full flex-col divide-y divide-gray-200 bg-white dark:bg-neutral-800 shadow-xl">
    <div class="h-0 flex-1 overflow-y-auto">

      <!-- Header -->
      <div class="bg-violet-700 bg-gradient-to-tr from-violet-800 to-violet-600 px-4 py-6 sm:px-6">
        <div class="flex items-center justify-between">
          <HeadlessDialogTitle class="text-base font-semibold leading-6 text-white">New Team Member</HeadlessDialogTitle>
          <div class="ml-3 flex h-7 items-center">
            <button type="button" class="relative rounded-md bg-violet-700 text-violet-200 hover:text-white focus:outline-none focus:ring-2 focus:ring-white" @click="close">
              <span class="absolute -inset-2.5" />
              <span class="sr-only">Close panel</span>
              <Icon name="uil:times" class="h-6 w-6" aria-hidden="true" />
            </button>
          </div>
        </div>
        <div class="mt-1">
          <p class="text-sm text-violet-300">Get started by filling in the information below to create a new team member.</p>
        </div>
      </div>

      <!-- Divider container -->
      <div class="space-y-6 py-6 sm:space-y-0 sm:divide-y sm:divide-gray-200 dark:sm:divide-neutral-600 sm:py-0">
        <!-- Name -->
        <div class="space-y-2 px-4 sm:grid sm:grid-cols-3 sm:gap-4 sm:space-y-0 sm:px-6 sm:py-5">
          <div>
            <label for="name" class="block text-sm font-medium leading-6 text-gray-900 dark:text-neutral-200 sm:mt-1.5">Name</label>
          </div>
          <div class="sm:col-span-2">
            <input type="text" name="name" id="name" ref="nameIpt" v-model="state.name" class="form-input" />
          </div>
        </div>

        <!-- Email -->
        <div class="space-y-2 px-4 sm:grid sm:grid-cols-3 sm:gap-4 sm:space-y-0 sm:px-6 sm:py-5">
          <div>
            <label for="email" class="block text-sm font-medium leading-6 text-gray-900 dark:text-neutral-200 sm:mt-1.5">Email</label>
          </div>
          <div class="sm:col-span-2">
            <input type="text" name="email" id="email" v-model="state.email" class="form-input" />
          </div>
        </div>

        <!-- Datatracker Email -->
        <div class="space-y-2 px-4 sm:grid sm:grid-cols-3 sm:gap-4 sm:space-y-0 sm:px-6 sm:py-5">
          <div>
            <label for="datatracker" class="block text-sm font-medium leading-6 text-gray-900 dark:text-neutral-200 sm:mt-1.5">Datatracker Login Email</label>
          </div>
          <div class="sm:col-span-2">
            <input type="text" name="datatracker" id="datatracker" v-model="state.datatracker" class="form-input" />
          </div>
        </div>

        <!-- Timezone -->
        <div class="space-y-2 px-4 sm:grid sm:grid-cols-3 sm:gap-4 sm:space-y-0 sm:px-6 sm:py-5">
          <div>
            <label for="timezone" class="block text-sm font-medium leading-6 text-gray-900 dark:text-neutral-200 sm:mt-1.5">Timezone</label>
          </div>
          <div class="sm:col-span-2">
            <select id="timezone" name="timezone" v-model="state.timezone" class="form-select">
              <option v-for="timezone of timezones" :key="timezone">{{ timezone }}</option>
            </select>
          </div>
        </div>

        <!-- Hours per week -->
        <div class="space-y-2 px-4 sm:grid sm:grid-cols-3 sm:gap-4 sm:space-y-0 sm:px-6 sm:py-5">
          <div>
            <label for="hours" class="block text-sm font-medium leading-6 text-gray-900 dark:text-neutral-200 sm:mt-1.5">Hours</label>
          </div>
          <div class="sm:col-span-2">
            <input type="number" name="hours" id="hours" v-model.number="state.hours" class="form-input" />
          </div>
        </div>
      </div>

      <!-- Manager -->
      <div class="space-y-2 px-4 sm:grid sm:grid-cols-3 sm:gap-4 sm:space-y-0 sm:px-6 sm:py-5">
        <div>
          <label for="manager" class="block text-sm font-medium leading-6 text-gray-900 dark:text-neutral-200 sm:mt-1.5">Manager</label>
        </div>
        <div class="sm:col-span-2">
          <select id="manager" name="manager" v-model="state.manager" class="form-select">
            <option v-for="manager of managers" :key="manager">{{ manager }}</option>
          </select>
        </div>
      </div>

      <!-- Roles -->
      <div class="space-y-2 px-4 sm:grid sm:grid-cols-3 sm:gap-4 sm:space-y-0 sm:px-6 sm:py-5">
        <div>
          <label for="roles" class="block text-sm font-medium leading-6 text-gray-900 dark:text-neutral-200 sm:mt-1.5">Roles</label>
        </div>
        <div class="sm:col-span-2">
          <fieldset>
            <legend class="sr-only">Roles</legend>
            <div class="space-y-5">
              <div v-for="role of roles" :key="role.value" class="relative flex items-start">
                <div class="flex h-6 items-center">
                  <input :id="`role-${role.value}`"
                    :aria-describedby="`role-${role.value}-description`"
                    :name="`role-${role.value}`"
                    type="checkbox"
                    :value="role.value"
                    v-model="state.roles"
                    :class="[role.caution ? 'border-rose-300 dark:border-rose-500 text-rose-700 dark:text-rose-700 hover:border-rose-400 focus:ring-rose-600' : 'border-gray-300 dark:border-neutral-500 text-violet-600 dark:text-violet-500 hover:border-violet-400 dark:hover:border-violet-500 focus:ring-violet-600 dark:focus:ring-violet-500', 'h-4 w-4 bg-white dark:bg-neutral-900 rounded border-2']"
                    />
                </div>
                <div class="ml-3 text-sm leading-6">
                  <label :for="`role-${role.value}`" :class="[role.caution ? 'text-rose-800 dark:text-rose-400' : 'text-gray-900 dark:text-neutral-200', 'font-medium']">{{ role.label }}</label>
                  <p :id="`role-${role.value}-description`" :class="[role.caution ? 'text-rose-700 dark:text-rose-500' : 'text-gray-500 dark:text-neutral-400', 'text-xs']">{{ role.description }}</p>
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
  <ConfirmDialog v-model:isShown="state.confirmShown" title="Manager Role Selected" caption="Are you sure you want to create a new team member with the Manager role?" />
</template>

<script setup lang="ts">
import { overlayModalMethodsKey } from '~/providers/providerKeys';

// DIALOG

const overlayModalMethods = inject(overlayModalMethodsKey) 
if(!overlayModalMethods) throw Error('overlayModalMethods used outside provider');
const { ok, cancel } = overlayModalMethods

// DATA

type State = {
  name: string
  email: string
  datatracker: string
  timezone: string
  hours: number
  manager: string
  roles: string[]
  confirmShown: boolean
}

const state = reactive<State>({
  name: '',
  email: '',
  datatracker: '',
  timezone: process.client ? Intl.DateTimeFormat().resolvedOptions().timeZone : 'America/New_York',
  hours: 20,
  manager: '',
  roles: [],
  confirmShown: false
})

const managers: string[] = []
const timezones = process.client ? Intl.supportedValuesOf('timeZone') : []
const roles = [
  { value: 'formatting', label: 'Formatter', description: 'An editor for docs that require extensive XML formatting.' },
  { value: 'pe', label: 'Primary Editor', description: 'An editor who makes the first editing pass.' },
  { value: 're', label: 'RFC Editor', description: 'A more experienced editor who makes a 2nd pass and also checks things like code components and IANA actions.' },
  { value: 'finrev', label: 'Final Review', description: 'An editor who handles the interactions with authors during their final review (AUTH48).' },
  { value: 'pub', label: 'Publisher', description: 'An editor who does the final-final reviews after the author has signed off and publishes the RFC to the website.' },
  { value: 'manager', label: 'Manager', description: 'A manager can access restricted sections like Legal, Manage Team Members, Assign Docs, Change RFC Status, Withdraw Document and more.', caution: true }
]

const nameIpt = ref(null)

// METHODS

function close () {
  if (!state.confirmShown) {
    cancel()
  }
}

function createUser () {
  if (state.roles.includes('manager')) {
    state.confirmShown = true
  } else {
    ok()
  }
}
</script>
