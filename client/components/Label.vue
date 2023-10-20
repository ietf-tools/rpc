<template>
  <Badge :color="label.color">
    <Icon v-if="label.is_exception" class="mr-2" name="pajamas:warning"/>
    {{ label.slug }}
  </Badge>
</template>

<script setup>
defineProps({
  /**
   * Label to be rendered
   */
  label: {
    type: Object,
    required: true
  }
})
</script>
