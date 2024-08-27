<template>
  <button type="button" class="btn-secondary">
    <span class="sr-only">Refresh</span>
    <Icon name="solar:refresh-line-duotone" size="1.5em" @click="$emit('refresh')"
          :class="[pending ? 'animate-spin text-orange-600' : 'text-gray-500 dark:text-neutral-300']"
          aria-hidden="true"/>
  </button>
</template>

<script setup lang="ts">
type Props = {
  pending?: boolean
}

withDefaults(defineProps<Props>(), {
  pending: false
})

defineEmits(['refresh'])
</script>
