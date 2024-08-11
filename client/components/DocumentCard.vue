<!-- Document Card
Based on https://tailwindui.com/components/application-ui/lists/grid-lists#component-2beafc928684743ff886c0b164edb126
-->
<template>
  <li :key="cookedDocument.name"
      :class="[props.selected ? 'border-violet-700' : 'border-gray-200', 'overflow-hidden rounded-xl border']">
    <div class="flex items-center gap-x-4 border-b border-gray-900/5 bg-gray-50 p-6">
      <Icon name="solar:document-text-line-duotone"
            class="h-8 w-8 flex-none"/>
      <div class="text-sm font-medium leading-6 text-gray-900">{{ cookedDocument.name }}</div>
      <Badge v-if="cookedDocument.needsAssignment" :label="`Needs ${cookedDocument.needsAssignment.name}`"/>
      <HeadlessMenu as="div" class="relative ml-auto">
        <HeadlessMenuButton class="-m-2.5 block p-2.5 text-gray-400 hover:text-gray-500">
          <span class="sr-only">Open options</span>
          <Icon name="heroicons:ellipsis-horizontal-20-solid" class="h-5 w-5" aria-hidden="true"/>
        </HeadlessMenuButton>
        <transition enter-active-class="transition ease-out duration-100"
                    enter-from-class="transform opacity-0 scale-95" enter-to-class="transform opacity-100 scale-100"
                    leave-active-class="transition ease-in duration-75"
                    leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
          <HeadlessMenuItems
            class="absolute right-0 z-10 mt-0.5 w-32 origin-top-right rounded-md bg-white py-2 shadow-lg ring-1 ring-gray-900/5 focus:outline-none">
            <HeadlessMenuItem v-slot="{ active }">
              <a href="#" :class="[active ? 'bg-gray-50' : '', 'block px-3 py-1 text-sm leading-6 text-gray-900']"
              >View<span class="sr-only">, {{ cookedDocument.name }}</span></a
              >
            </HeadlessMenuItem>
            <HeadlessMenuItem v-slot="{ active }">
              <a href="#" :class="[active ? 'bg-gray-50' : '', 'block px-3 py-1 text-sm leading-6 text-gray-900']">
                Edit<span class="sr-only">, {{ cookedDocument.name }}</span>
              </a>
            </HeadlessMenuItem>
          </HeadlessMenuItems>
        </transition>
      </HeadlessMenu>
    </div>
    <dl class="-my-3 divide-y divide-gray-100 px-6 py-4 text-sm leading-6">
      <div class="flex justify-between gap-x-4 py-3">
        <dt class="text-gray-500">Deadline</dt>
        <dd class="grow flex items-start gap-x-2">
          {{ cookedDocument.external_deadline?.toLocaleString(DateTime.DATE_FULL) || '-' }}</dd>
      </div>
      <div class="flex justify-between gap-x-4 py-3">
        <dt class="text-gray-500">Pages</dt>
        <dd class="grow flex items-start gap-x-2">{{ cookedDocument.pages || '-' }}</dd>
      </div>
      <div class="flex justify-between gap-x-4 py-3">
        <dt class="text-gray-500">Assignments</dt>
        <dd class="grow flex items-start gap-x-2">
          <AssignmentTray :assignments="cookedDocument.assignments"
                          @assignEditor="(editorId) => assignEditor(cookedDocument.id, editorId)"/>
        </dd>
      </div>
    </dl>
  </li>
</template>

<script setup lang="ts">
import { inject } from 'vue'
import { DateTime } from 'luxon'
import { assignEditorKey } from '~/providers/providerKeys';

type Props = {
  document: {
    id: string
    name:string
    external_deadline: string
    needsAssignment?: {
      name: string
    }
    assignments: string[]
    pages: number
  }
  selected: boolean
}

const props = defineProps<Props>()

const _assignEditor = inject(assignEditorKey)
if(!_assignEditor) throw Error("Required assignEditor provider")
const assignEditor = _assignEditor

const cookedDocument = computed(() => ({
  ...props.document,
  external_deadline: props.document.external_deadline && DateTime.fromISO(props.document.external_deadline),
  assignments: props.document.assignments
}))

</script>
