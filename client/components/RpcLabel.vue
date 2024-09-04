<template>
  <Badge :color="label?.color">
    <Icon v-if="label?.isException" class="mr-2" name="pajamas:warning"/>
    {{ label?.slug }}
  </Badge>
</template>

<script setup lang="ts">
import type { Label } from '~/rpctracker_client'

type Props = {
  label?: Label
}

const props = defineProps<Props>()

</script>
