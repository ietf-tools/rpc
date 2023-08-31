<template>
  <Teleport to="body">
    <transition enter-active-class="transform ease-out duration-300 transition" enter-from-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2" enter-to-class="translate-y-0 opacity-100 sm:translate-x-0" leave-active-class="transition ease-in duration-100" leave-from-class="opacity-100" leave-to-class="opacity-0">
      <div v-if="isShown" class="pointer-events-auto w-full max-w-sm overflow-hidden rounded-lg bg-white dark:bg-neutral-800 shadow-xl ring-1 ring-black dark:ring-white ring-opacity-10 dark:ring-opacity-10 z-1000 fixed top-5 right-5">
        <div class="p-4">
          <div class="flex items-start">
            <div class="flex-shrink-0">
              <Icon v-if="type === 'positive'" name="uil:check-circle" class="h-6 w-6 text-green-400 dark:text-green-500" aria-hidden="true" />
              <Icon v-else-if="type === 'negative'" name="uil:exclamation-triangle" class="h-6 w-6 text-rose-600 dark:text-rose-600" aria-hidden="true" />
              <Icon v-else name="uil:question-circle" class="h-6 w-6 text-amber-900 dark:text-stone-300" aria-hidden="true" />
            </div>
            <div class="ml-3 w-0 flex-1 pt-0.5">
              <p v-if="type === 'negative'" class="text-sm font-medium text-rose-600 dark:text-rose-500">{{ title }}</p>
              <p v-else class="text-sm font-medium text-gray-900 dark:text-neutral-300">{{ title }}</p>
              <p class="mt-1 text-sm text-gray-500 dark:text-neutral-400">{{ caption }}</p>
            </div>
            <div class="ml-4 flex flex-shrink-0">
              <button type="button" @click="close" class="inline-flex rounded-md bg-white dark:bg-neutral-900 text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:ring-offset-2">
                <span class="sr-only">Dismiss</span>
                <Icon name="uil:times" class="h-5 w-5" aria-hidden="true" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </Teleport>
</template>

<script setup>
// PROPS / EMITS

defineProps({
  isShown: {
    type: Boolean,
    default: false,
    required: true
  },
  title: {
    type: String,
    default: 'Something happened',
  },
  caption: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    default: 'positive'
  }
})

const emit = defineEmits(['update:isShown'])

// METHODS

function close () {
  emit('update:isShown', false)
}
</script>
