<!-- based on https://tailwindui.com/components/application-ui/forms/textareas#component-784309f82e9913989c2196a2d47eff4a -->
<!-- todo refactor this into a better form -->
<template>
  <div class="flex items-start space-x-4">
    <div class="flex-shrink-0">
      <img class="inline-block h-10 w-10 rounded-full"
           src="https://images.unsplash.com/photo-1550525811-e5869dd03032?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
           alt=""/>
    </div>
    <div class="min-w-0 flex-1">
      <form action="#" class="relative">
        <div
          class="overflow-hidden rounded-lg shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-indigo-600">
          <label for="comment" class="sr-only">Add your comment</label>
          <textarea rows="3" name="comment" id="comment"
                    class="block w-full resize-none border-0 bg-transparent py-1.5 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm sm:leading-6"
                    placeholder="Add your comment..."/>

          <!-- Spacer element to match the height of the toolbar -->
          <div class="py-2" aria-hidden="true">
            <!-- Matches height of button in toolbar (1px border + 36px content height) -->
            <div class="py-px">
              <div class="h-9"/>
            </div>
          </div>
        </div>

        <div class="absolute inset-x-0 bottom-0 flex justify-between py-2 pl-3 pr-2">
          <div class="flex items-center space-x-5">
            <div class="flex items-center">
              <button type="button"
                      class="-m-2.5 flex h-10 w-10 items-center justify-center rounded-full text-gray-400 hover:text-gray-500">
                <Icon name="heroicons:paper-clip" class="h-5 w-5" aria-hidden="true"/>
                <span class="sr-only">Attach a file</span>
              </button>
            </div>
            <div class="flex items-center">
              <HeadlessListbox as="div" v-model="selected">
                <HeadlessListboxLabel class="sr-only">Your mood</HeadlessListboxLabel>
                <div class="relative">
                  <HeadlessListboxButton
                    class="relative -m-2.5 flex h-10 w-10 items-center justify-center rounded-full text-gray-400 hover:text-gray-500">
                    <span class="flex items-center justify-center">
                      <span v-if="selected.value === null">
                        <Icon name="heroicons:face-smile" class="h-5 w-5 flex-shrink-0" aria-hidden="true"/>
                        <span class="sr-only">Add your mood</span>
                      </span>
                      <span v-if="!(selected.value === null)">
                        <span :class="[selected.bgColor, 'flex h-8 w-8 items-center justify-center rounded-full']">
                          <Icon :name="selected.icon" class="h-5 w-5 flex-shrink-0 text-white" aria-hidden="true"/>
                        </span>
                        <span class="sr-only">{{ selected.name }}</span>
                      </span>
                    </span>
                  </HeadlessListboxButton>

                  <transition leave-active-class="transition ease-in duration-100" leave-from-class="opacity-100"
                              leave-to-class="opacity-0">
                    <HeadlessListboxOptions
                      class="absolute z-10 -ml-6 mt-1 w-60 rounded-lg bg-white py-3 text-base shadow ring-1 ring-black ring-opacity-5 focus:outline-none sm:ml-auto sm:w-64 sm:text-sm">
                      <HeadlessListboxOption as="template" v-for="mood in moods" :key="mood.value" :value="mood"
                                     v-slot="{ active }">
                        <li
                          :class="[active ? 'bg-gray-100' : 'bg-white', 'relative cursor-default select-none px-3 py-2']">
                          <div class="flex items-center">
                            <div :class="[mood.bgColor, 'flex h-8 w-8 items-center justify-center rounded-full']">
                              <Icon :name="mood.icon" :class="[mood.iconColor, 'h-5 w-5 flex-shrink-0']"
                                         aria-hidden="true"/>
                            </div>
                            <span class="ml-3 block truncate font-medium">{{ mood.name }}</span>
                          </div>
                        </li>
                      </HeadlessListboxOption>
                    </HeadlessListboxOptions>
                  </transition>
                </div>
              </HeadlessListbox>
            </div>
          </div>
          <div class="flex-shrink-0">
            <button type="submit"
                    class="inline-flex items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
              Post
            </button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const moods = [
  { name: 'Excited', value: 'excited', icon: 'heroicons:fire-20-solid', iconColor: 'text-white', bgColor: 'bg-red-500' },
  { name: 'Loved', value: 'loved', icon: 'heroicons:heart-20-solid', iconColor: 'text-white', bgColor: 'bg-pink-400' },
  { name: 'Happy', value: 'happy', icon: 'heroicons:face-smile', iconColor: 'text-white', bgColor: 'bg-green-400' },
  { name: 'Sad', value: 'sad', icon: 'heroicons:face-frown', iconColor: 'text-white', bgColor: 'bg-yellow-400' },
  { name: 'Thumbsy', value: 'thumbsy', icon: 'heroicons:hand-thumb-up', iconColor: 'text-white', bgColor: 'bg-blue-500' },
  { name: 'I feel nothing', value: null, icon: 'heroicons:x-mark', iconColor: 'text-gray-400', bgColor: 'bg-transparent' },
]

const selected = ref(moods[5])
</script>
