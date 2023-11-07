<script setup>
definePageMeta({
  middleware: [
    function (to, from) {
      return navigateTo('/auth48/inprogress')
    }
  ]
})
</script>
