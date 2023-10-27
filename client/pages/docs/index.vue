<template>
  <TitleBlock title="Documents" summary="Beep boop">
    <template #right>
      <RefreshButton class="mr-3"/>
      <NuxtLink
        v-if="userStore.isManager"
        class="max-w-l items-center rounded-md bg-violet-600 px-3 py-2 text-center text-sm font-semibold text-white shadow-sm hover:bg-violet-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
        to="/docs/assignments">
        Manage Assignments
      </NuxtLink>
    </template>
  </TitleBlock>
  <div class="mt-8 flow-root">
  </div>
</template>

<script setup>
const userStore = useUserStore()
</script>
