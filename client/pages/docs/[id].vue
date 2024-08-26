<template>
  <header class="relative isolate">
    <div class="absolute inset-0 -z-10 overflow-hidden" aria-hidden="true">
      <div class="absolute left-16 top-full -mt-16 transform-gpu opacity-50 blur-3xl xl:left-1/2 xl:-ml-80">
        <div class="aspect-[1154/678] w-[72.125rem] bg-gradient-to-br from-[#FF80B5] to-[#9089FC]"
             style="clip-path: polygon(100% 38.5%, 82.6% 100%, 60.2% 37.7%, 52.4% 32.1%, 47.5% 41.8%, 45.2% 65.6%, 27.5% 23.4%, 0.1% 35.3%, 17.9% 0%, 27.7% 23.4%, 76.2% 2.5%, 74.2% 56%, 100% 38.5%)"/>
      </div>
      <div class="absolute inset-x-0 bottom-0 h-px bg-gray-900/5"/>
    </div>

    <div class="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
      <div class="mx-auto flex max-w-2xl items-center justify-between gap-x-8 lg:mx-0 lg:max-w-none">
        <div class="flex items-center gap-x-6 text-gray-900 dark:text-white">
          <Icon name="solar:document-text-line-duotone" class="w-10 h-10"/>
          <h1>
            <div class="mt-1 text-xl font-semibold leading-6">
              <span v-if="draft">{{ draft.name }}-{{ draft.rev }}</span>
            </div>
          </h1>
        </div>
      </div>
    </div>
  </header>

  <div class="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
    <div
      class="mx-auto grid max-w-2xl grid-cols-1 grid-rows-1 place-items-stretch gap-x-8 gap-y-8 lg:mx-0 lg:max-w-none lg:grid-cols-3">

      <!-- Status summary -->
      <div class="lg:col-start-3 lg:row-start-1 lg:row-span-1 grid place-items-stretch">
        <h2 class="sr-only">Status Summary</h2>
        <div class="rounded-lg bg-white text-gray-900 dark:bg-neutral-900 dark:text-neutral-300 shadow-sm ring-1 ring-gray-900/5">
          <div class="px-4 pt-6 sm:px-6">
            <h3 class="text-base font-semibold leading-7">Current Assignments</h3>
            <div class="mx-4 text-sm font-medium ">
              <div v-if="draftAssignments.length === 0">
                None
              </div>
              <dl v-else>
                <div v-for="assignment of draftAssignments"
                     class="py-1 grid grid-cols-2">
                  <dt>{{ people.find(p => p.id === assignment.person)?.name }}</dt>
                  <dd class="relative">
                    <Badge class="absolute right-0" :label="assignment.role"/>
                  </dd>
                </div>
              </dl>
            </div>
          </div>
          <div class="px-4 py-6 sm:px-6 text-gray-900 dark:text-neutral-300">
            <h3 class="text-base font-semibold leading-7 ">Queue Information (mocked)</h3>
            <div class="mx-4 text-sm font-medium">
              <dl>
                <div class="py-1 grid grid-cols-2">
                  <dt>Current State</dt>
                  <dd>EDIT-in-process</dd>
                </div>
                <div class="py-1 grid grid-cols-2">
                  <!-- Showing externalDeadline here - what about internal_goal? -->
                  <dt>Deadline</dt>
                  <dd>
                    <time v-if="draft?.externalDeadline" :datetime="draft.externalDeadline.toISODate()?.toString()">
                      {{ draft.externalDeadline.toLocaleString(DateTime.DATE_MED) }}
                    </time>
                    <span v-else>-</span>
                  </dd>
                </div>
                <div class="py-1 grid grid-cols-2">
                  <dt>Est. Completion</dt>
                  <dd>
                    <time datetime="2024-07-30">Jul 30, 2024</time>
                    <Badge label="Overdue" color="red"/>
                  </dd>
                </div>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <!-- Document Info -->
      <div class="lg:col-span-2 lg:row-span-2 lg:row-start-1 grid place-items-stretch text-gray-900 dark:bg-neutral-900 text-gray-900 dark:text-neutral-300">
        <h2 class="sr-only">Main panel</h2>
        <div class="rounded-lg bg-white dark:bg-neutral-900 shadow-sm ring-1 ring-gray-900/5">
          <div class="px-4 py-6 sm:px-6">
            <h3 class="text-base font-semibold leading-7">Document Info</h3>
            <div class="mx-4 pb-3 text-sm font-medium">
              <dl>
                <div class="px-4 pt-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt>Title</dt>
                  <dd class="mt-1 leading-6 sm:col-span-2 sm:mt-0">
                    {{ draft?.title ?? '-' }}
                  </dd>
                </div>
                <div class="px-4 pt-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt>Authors</dt>
                  <dd class="mt-1 leading-6 sm:col-span-2 sm:mt-0">
                    J. Doe (mocked)
                  </dd>
                </div>
                <div class="px-4 pt-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt>Submitted Pages</dt>
                  <dd class="mt-1 leading-6 sm:col-span-2 sm:mt-0">
                    {{ draft?.pages ?? '-' }}
                  </dd>
                </div>
                <div class="px-4 pt-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt>Document Shepherd</dt>
                  <dd class="mt-1 leading-6 sm:col-span-2 sm:mt-0">
                    Dolly Shepherd (mocked)
                  </dd>
                </div>
                <div class="px-4 pt-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt>Stream</dt>
                  <dd class="mt-1 leading-6 sm:col-span-2 sm:mt-0">
                    {{ draft?.stream ?? '-' }}
                    <span v-if="draft?.submittedStream !== draft?.stream">
                      (submitted as {{ draft?.submittedStream }})
                    </span>
                  </dd>
                </div>
                <div class="px-4 pt-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt>Stream Manager</dt>
                  <dd class="mt-1 leading-6 sm:col-span-2 sm:mt-0">
                    Ari Drecker (mocked)
                  </dd>
                </div>
                <div class="px-4 pt-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt>Submitted Format</dt>
                  <dd class="mt-1 leading-6 sm:col-span-2 sm:mt-0">
                    {{ draft?.submittedFormat ?? '-' }}
                  </dd>
                </div>
                <div class="px-4 pt-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt>Submitted Boilerplate</dt>
                  <dd class="mt-1 leading-6 sm:col-span-2 sm:mt-0">
                    {{ draft?.intendedBoilerplate ?? '-' }}
                    <span v-if="draft?.submittedBoilerplate !== draft?.intendedBoilerplate">
                      (submitted as {{ draft?.submittedBoilerplate }})
                    </span>
                  </dd>
                </div>
                <div class="px-4 pt-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt>Standard Level</dt>
                  <dd class="mt-1 leading-6 sm:col-span-2 sm:mt-0">
                    {{ draft?.intendedStdLevel ?? '-' }}
                    <span v-if="draft?.submittedStdLevel !== draft?.intendedStdLevel">
                      (submitted as {{ draft?.submittedStdLevel }})
                    </span>
                  </dd>
                </div>
                <div class="px-4 pt-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt>Disposition</dt>
                  <dd class="mt-1 leading-6 sm:col-span-2 sm:mt-0">
                    {{ draft?.disposition ?? '-' }}
                  </dd>
                </div>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <!-- Labels -->
      <div class="lg:col-start-3 lg:row-start-2 lg:row-span-1 grid place-items-stretch text-gray-900 dark:text-neutral-300">
        <h2 class="sr-only">Label panel</h2>
        <div class="rounded-lg bg-white dark:bg-neutral-900 shadow-sm ring-1 ring-gray-900/5">
          <div class="px-4 py-6 sm:px-6">
            <h3 class="text-base font-semibold leading-7">Labels</h3>
            <div class="flex">
              <div v-for="lbl of appliedLabels" class="flex-shrink-0 p-1">
                <RpcLabel :label="lbl"/>
              </div>
            </div>
            <RpcLabelPicker :labels="labels" :model-value="draft?.labels" @update:model-value="saveLabels"
                            item-label="slug"/>
          </div>
        </div>
      </div>

      <!-- History -->
      <div class="lg:col-span-full grid place-items-stretch text-gray-900 dark:text-neutral-300">
        <h2 class="sr-only">History panel</h2>
        <div class="rounded-lg bg-white dark:bg-neutral-900 shadow-sm ring-1 ring-gray-900/5">
          <div class="px-4 py-6 sm:px-6">
            <h3 class="text-base font-semibold leading-7">History</h3>
            <div class="flex">
              <table class="min-w-full divide-y divide-gray-300">
                <thead class="bg-gray-50 dark:bg-neutral-800">
                  <tr>
                    <th scope="col" class="py-3.5 pl-4 pr-3 text-left text-sm font-semibold sm:pl-6">Date</th>
                    <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold">By</th>
                    <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold">Description</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-200">
                  <tr v-for="entry of draft?.history ?? []" :key="entry.id">
                    <td class="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium sm:pl-6">
                      <time :datetime="DateTime.fromJSDate(entry.date).toISO()?.toString()">
                        {{ DateTime.fromJSDate(entry.date).toLocaleString(DateTime.DATE_MED) }}
                      </time>
                    </td>
                    <td class="whitespace-nowrap px-3 py-4 text-sm">
                      <NuxtLink v-if="entry.by?.personId"
                                :to="`/team/${entry.by.personId}`"
                                class="text-violet-900 hover:text-violet-500 dark:text-violet-300 hover:dark:text-violet-100">
                        {{ entry.by.name }}
                      </NuxtLink>
                      <span v-else>
                        {{ entry.by?.name }}
                      </span>
                    </td>
                    <td class="whitespace-nowrap px-3 py-4 text-sm">{{ entry.desc }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">

import { DateTime } from 'luxon'

const route = useRoute()
const api = useApi()

// COMPUTED

const appliedLabels = computed(() => labels.value.filter((lbl) => rawDraft.value?.labels.includes(lbl.id)))

const draftAssignments = computed(() => assignments.value.filter((a) => a.rfcToBe === draft.value?.id))

const draft = computed(() => {
  if (rawDraft?.value) {
    return {
      ...rawDraft.value,
      externalDeadline:
        rawDraft.value.externalDeadline
          ? DateTime.fromJSDate(rawDraft.value.externalDeadline)
          : null
    }
  }
  return null
})

// DATA

const { data: labels } = await useAsyncData(() => api.labelsList(), { server: false, default: () => [] })

const { data: rawDraft, pending: draftPending, refresh: draftRefresh } = await useAsyncData(
  () => api.documentsRetrieve({ draftName: route.params.id.toString() }),
  { server: false }
)

// todo retrieve assignments for a single draft more efficiently
const { data: assignments } = await useAsyncData(
  () => api.assignmentsList(),
  { server: false, default: () => [] }
)

const { data: people } = await useAsyncData(
  () => api.rpcPersonList(),
  { server: false, default: () => [] }
)

async function saveLabels (labels: number[]) {
  if (!draftPending.value) {
    await api.documentsPartialUpdate({
      draftName: draft.value?.name ?? '',
      patchedRfcToBe: { labels }
    })
  }
  draftRefresh()
}
</script>
