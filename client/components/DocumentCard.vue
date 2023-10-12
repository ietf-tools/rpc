<!-- Document Card
Based on https://tailwindui.com/components/application-ui/lists/grid-lists#component-2beafc928684743ff886c0b164edb126
-->
<template>
  <li :key="cookedDocument.name" class="overflow-hidden rounded-xl border border-gray-200">
    <div class="flex items-center gap-x-4 border-b border-gray-900/5 bg-gray-50 p-6">
      <Icon name="solar:document-text-line-duotone"
           class="h-8 w-8 flex-none"/>
      <div class="text-sm font-medium leading-6 text-gray-900">{{ cookedDocument.name }}</div>
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
        <dt class="text-gray-500">Assignments</dt>
        <dd class="grow flex items-start gap-x-2">
          <AssignmentTray :assignments="cookedDocument.assignments"
                          @assignEditor="editorId => $emit('assignEditor', cookedDocument.id, editorId)"
                          @deleteAssignment="assignment => $emit('deleteAssignment', assignment)"/>
        </dd>
      </div>
    </dl>
  </li>
</template>

<script setup>
const props = defineProps({
  document: { type: Object, required: true }
})

defineEmits(['assignEditor', 'deleteAssignment'])

const cookedDocument = computed(() => ({
  id: props.document.id,
  name: props.document.name,
  assignments: props.document.assignments
}))
</script>
