<!-- Editor Card
Based on https://tailwindui.com/components/application-ui/lists/grid-lists#component-4ec337def61b547035ce908c128bca5c
-->
<template>
  <li :key="cookedEditor.id" class="col-span-1 flex rounded-md shadow-sm">
    <div
      :class="[cookedEditor.bgColor, 'flex w-16 flex-shrink-0 items-center justify-center rounded-l-md text-sm font-medium text-white']">
      {{ cookedEditor.initials }}
    </div>
    <div
      class="flex flex-1 items-center justify-between truncate rounded-r-md border-b border-r border-t border-gray-200 bg-white">
      <div class="flex-1 truncate px-4 py-2 text-sm">
        <a :href="cookedEditor.href" class="font-medium text-gray-900 hover:text-gray-600">{{ cookedEditor.name }}</a>
        <p class="text-gray-500">{{ cookedEditor.detail }}</p>
      </div>
      <div class="flex-shrink-0 pr-2">
        <button type="button"
                class="inline-flex h-8 w-8 items-center justify-center rounded-full bg-transparent bg-white text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">
          <span class="sr-only">Open options</span>
          <Icon class="h-5 w-5" name="heroicons:ellipsis-vertical-20-solid" aria-hidden="true"/>
        </button>
      </div>
    </div>
  </li>
</template>

<script setup>
const props = defineProps({
  editor: Object
})

// Compute data for the component
const cookedEditor = computed(() => ({
  name: props.editor.name,
  initials: props.editor.name[0],
  href: '#',
  detail: 'Some detail',
  bgColor: 'bg-pink-600'
}))

</script>
