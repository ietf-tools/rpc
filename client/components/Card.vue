<template>
  <div class="overflow-hidden rounded-lg bg-white shadow">
    <div v-if="$slots.header" class="px-4 py-5 sm:px-6">
      <slot name="header"/>
    </div>
    <div class="px-4 py-5 sm:p-6">
      <slot/>
    </div>
    <div v-if="$slots.footer" class="px-4 py-5 sm:px-6">
      <slot name="footer"/>
    </div>
  </div>
</template>

<script setup lang="ts">

</script>
