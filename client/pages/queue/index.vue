<script setup>
definePageMeta({
  middleware: [
    function (to, from) {
      return navigateTo('/queue/submissions')
    }
  ]
})
</script>
