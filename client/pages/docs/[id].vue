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
        <div class="flex items-center gap-x-6">
          <Icon name="solar:document-text-line-duotone" class="w-10 h-10"/>
          <h1>
            <div class="mt-1 text-xl font-semibold leading-6 text-gray-900 dark:text-white">
              <span v-if="draft">{{ draft.name }}-{{ draft.rev }}</span>
            </div>
          </h1>
        </div>
      </div>
    </div>
  </header>

  <div class="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
    <div
      class="mx-auto grid max-w-2xl grid-cols-1 grid-rows-1 items-start gap-x-8 gap-y-8 lg:mx-0 lg:max-w-none lg:grid-cols-3">

      <!-- Status summary -->
      <div class="lg:col-start-3 lg:row-end-1">
        <h2 class="sr-only">Status Summary (mockup)</h2>
        <div class="rounded-lg bg-white dark:bg-neutral-900 shadow-sm ring-1 ring-gray-900/5">
          <dl class="grid grid-cols-3">
            <div class="col-span-2 pl-6 pt-6">
              <dt class="text-sm font-semibold leading-6 text-gray-900">Current Assignments<br>(panel mocked)</dt>
              <dd class="mt-1 text-base font-semibold leading-6 text-gray-900">Someone</dd>
            </div>
            <div class="col-span-1 self-end px-6 pt-4">
              <dt class="sr-only">Reason</dt>
              <dd
                class="rounded-md bg-green-50 px-2 py-1 text-xs font-medium text-green-600 ring-1 ring-inset ring-green-600/20">
                PE
              </dd>
            </div>
            <div class="col-span-2 self-start pl-6 pt-6">
              <dt class="text-sm font-semibold leading-6 text-gray-900">Current Queue State</dt>
              <dd class="mt-1 text-base font-semibold leading-6 text-gray-900">EDIT-in-process</dd>
            </div>
            <div class="col-span-2 self-start pl-6 pt-6">
              <dt class="text-sm font-semibold leading-6 text-gray-900">Estimated Completion</dt>
              <dd class="mt-1 text-base font-semibold leading-6 text-gray-900">30 July 2023</dd>
            </div>
            <div class="col-span-1 self-end px-6 pt-4">
              <dt class="sr-only">Reason</dt>
              <dd
                class="rounded-md bg-red-50 px-2 py-1 text-xs font-medium text-red-600 ring-1 ring-inset ring-red-600/20">
                Overdue
              </dd>
            </div>
          </dl>
          <div class="py-3"/>
        </div>
      </div>

      <!-- Document Info -->
      <div
        class="-mx-4 px-4 py-8 bg-white dark:bg-neutral-900 shadow-sm ring-1 ring-gray-900/5 sm:mx-0 sm:rounded-lg sm:px-8 sm:pb-14 lg:col-span-2 lg:row-span-2 lg:row-end-2 xl:px-16 xl:pb-20 xl:pt-16">
        <h2 class="text-base font-semibold leading-6 text-gray-900">Document Info (mocked)</h2>
        <dl class="mt-6 grid grid-cols-1 text-sm leading-6 sm:grid-cols-2">
          <div class="sm:pr-4">
            <dt class="inline text-gray-500">Issued on</dt>
            {{ ' ' }}
            <dd class="inline text-gray-700">
              <time datetime="2023-23-01">January 23, 2023</time>
            </dd>
          </div>
          <div class="mt-2 sm:mt-0 sm:pl-4">
            <dt class="inline text-gray-500">Due on</dt>
            {{ ' ' }}
            <dd class="inline text-gray-700">
              <time datetime="2023-31-01">January 31, 2023</time>
            </dd>
          </div>
        </dl>
      </div>

    </div>

    <!-- Labels -->
    <div
      class="mx-auto grid max-w-2xl grid-cols-1 grid-rows-1 items-start gap-x-8 gap-y-8 lg:mx-0 lg:max-w-none lg:grid-cols-3">
        <div
          class="-mx-4 px-4 py-8 bg-white dark:bg-neutral-900 shadow-sm ring-1 ring-gray-900/5 sm:mx-0 sm:rounded-lg sm:px-8 sm:pb-14 lg:col-span-2 lg:row-span-2 lg:row-end-2 xl:px-16 xl:pb-20 xl:pt-16">
          <h2 class="text-base font-semibold leading-6 text-gray-900">Labels</h2>
          <div class="flex">
            <div v-for="lbl of appliedLabels" class="flex-shrink-0 p-1">
              <RpcLabel :label="lbl"/>
            </div>
          </div>
          <RpcLabelPicker :labels="labels" :model-value="draft?.labels" @update:model-value="saveLabels" item-label="slug"/>
        </div>
    </div>

    <!-- History -->
    <div
      class="mx-auto grid max-w-2xl grid-cols-1 grid-rows-1 items-start gap-x-8 gap-y-8 lg:mx-0 lg:max-w-none lg:grid-cols-3">
      <div
        class="-mx-4 px-4 py-8 bg-white dark:bg-neutral-900 shadow-sm ring-1 ring-gray-900/5 sm:mx-0 sm:rounded-lg sm:px-8 sm:pb-14 lg:col-span-2 lg:row-span-2 lg:row-end-2 xl:px-16 xl:pb-20 xl:pt-16">
        <h2 class="text-base font-semibold leading-6 text-gray-900">History</h2>
        <div class="flex">
          <table class="min-w-full divide-y divide-gray-300">
            <thead class="bg-gray-50">
              <tr>
                <th scope="col" class="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-6">Date</th>
                <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">By</th>
                <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Description</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200 bg-white">
              <tr v-for="entry of draft?.history ?? []" :key="entry.id">
                <td class="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-6">{{ entry.date }}</td>
                <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                  <NuxtLink v-if="entry.by?.personId"
                            :to="`/team/${entry.by.personId}`"
                            class="text-violet-900 hover:text-violet-500 dark:text-violet-300 hover:dark:text-violet-100">
                    {{ entry.by.name }}
                  </NuxtLink>
                  <span v-else>
                    {{ entry.by?.name }}
                  </span>
                </td>
                <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{{ entry.desc }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>

</template>

<script setup>

const route = useRoute()
const api = useApi()

const appliedLabels = computed(() => labels.value.filter((lbl) => draft.value?.labels.includes(lbl.id)))

const { data: labels } = await useAsyncData(() => api.labelsList(), { server: false, default: () => [] })

const { data: draft, pending: draftPending } = await useAsyncData(
  () => api.documentsRetrieve({ draftName: route.params.id }),
  { server: false }
)

async function saveLabels (labels) {
  if (!draftPending.value) {
    draft.value = await api.documentsPartialUpdate({
      draftName: draft.value.name,
      patchedRfcToBe: { labels }
    })
  }
}
</script>
