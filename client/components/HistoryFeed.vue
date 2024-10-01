<!--
History feed component
Based on https://tailwindui.com/components/application-ui/lists/feeds#component-81e5ec57a92ddcadaa913e7bb68336fe
-->
<template>
  <ul role="list" class="space-y-6">
    <li v-for="(activityItem, activityItemIdx) in orderedActivity" :key="activityItem.id" class="relative flex gap-x-4">
      <div
        :class="[activityItemIdx === activity.length - 1 ? 'h-6' : '-bottom-6', 'absolute left-0 top-0 flex w-6 justify-center']">
        <div class="w-px bg-gray-200"/>
      </div>
      <template v-if="activityItem.type === 'commented'">
        <img :src="activityItem.person.imageUrl" alt=""
             class="relative mt-3 h-6 w-6 flex-none rounded-full bg-gray-50"/>
        <div class="flex-auto rounded-md p-3 ring-1 ring-inset ring-gray-200">
          <div class="flex justify-between gap-x-4">
            <div class="py-0.5 text-xs leading-5 text-gray-500">
              <span class="font-medium text-gray-900">{{ activityItem.person.name }}</span> commented
            </div>
            <time :datetime="activityItem.dateTime" class="flex-none py-0.5 text-xs leading-5 text-gray-500">
              {{ activityItem.date }}
            </time>
          </div>
          <p class="text-sm leading-6 text-gray-500">{{ activityItem.comment }}</p>
        </div>
      </template>
      <template v-else>
        <div class="relative flex h-6 w-6 flex-none items-center justify-center bg-white">
          <Icon name="heroicons:check-circle" v-if="activityItem.type === 'paid'" class="h-6 w-6 text-indigo-600"
                aria-hidden="true"/>
          <div v-else class="h-1.5 w-1.5 rounded-full bg-gray-100 ring-1 ring-gray-300"/>
        </div>
        <p class="flex-auto py-0.5 text-xs leading-5 text-gray-500">
          <span class="font-medium text-gray-900">{{ activityItem.person.name }}</span> {{ activityItem.type }} the
          invoice.
        </p>
        <time :datetime="activityItem.dateTime" class="flex-none py-0.5 text-xs leading-5 text-gray-500">
          {{ activityItem.date }}
        </time>
      </template>
    </li>
  </ul>
</template>

<script setup lang="ts">
import { orderBy } from 'lodash-es'

const activity = [
  { id: 1, type: 'created', person: { name: 'Chelsea Hagon' }, date: '7d ago', dateTime: '2023-01-23T10:32' },
  { id: 2, type: 'edited', person: { name: 'Chelsea Hagon' }, date: '6d ago', dateTime: '2023-01-23T11:03' },
  { id: 3, type: 'sent', person: { name: 'Chelsea Hagon' }, date: '6d ago', dateTime: '2023-01-23T11:24' },
  {
    id: 4,
    type: 'commented',
    person: {
      name: 'Chelsea Hagon',
      imageUrl:
        'https://images.unsplash.com/photo-1550525811-e5869dd03032?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
    },
    comment: 'Called client, they reassured me the invoice would be paid by the 25th.',
    date: '3d ago',
    dateTime: '2023-01-23T15:56',
  },
  { id: 5, type: 'viewed', person: { name: 'Alex Curren' }, date: '2d ago', dateTime: '2023-01-24T09:12' },
  { id: 6, type: 'paid', person: { name: 'Alex Curren' }, date: '1d ago', dateTime: '2023-01-24T09:20' },
]

const orderedActivity = computed(() => orderBy(activity, ['dateTime'], ['desc']))

</script>
