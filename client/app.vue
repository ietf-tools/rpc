<template>
  <div>
    <SidebarNav />
    <main class="lg:pl-72">
      <HeaderNav />
      <NuxtLayout>
        <NuxtPage />
      </NuxtLayout>
    </main>
    <NuxtSnackbar />
  </div>
</template>

<script setup>
// const colorMode = useColorMode()

useHead({
  link: [
    { rel: 'preconnect', href: 'https://rsms.me' },
    { rel: 'stylesheet', href: 'https://rsms.me/inter/inter.css' }
  ],
  bodyAttrs: {
    class: 'h-full'
  },
  htmlAttrs: {
    class: 'h-full'
  },
  titleTemplate: (titleChunk) => {
    return titleChunk ? `${titleChunk} - RPC Production Center` : 'RPC Production Center'
  }
})
</script>

<style lang="scss">
:root { font-family: 'Inter', sans-serif; }
@supports (font-variation-settings: normal) {
  :root { font-family: 'Inter var', sans-serif; }
}

body {
  background-color: #f9fafb;
}
.dark body {
  background-color: #0a0a0a;
}
</style>
