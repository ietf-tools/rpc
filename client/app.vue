<template>
  <div>
    <SidebarNav />
    <main class="lg:pl-72">
      <HeaderNav />
      <NuxtLayout>
        <NuxtPage />
      </NuxtLayout>
    </main>
    <OverlayModal
      v-model:isShown="overlayModalState.isShown"
      :opts="overlayModalState.opts"
      @closeOk="overlayModalState.promiseResolve"
      @closeCancel="overlayModalState.promiseReject"
    />
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

// OVERLAY MODAL

const overlayModalState = shallowReactive({
  isShown: false,
  opts: {
    component: null,
    componentProps: {}
  },
  promiseResolve: null,
  promiseReject: null
})

provide('overlayModal', {
  /**
   * Open an overlay modal
   *
   * @param {Object} opts - Modal options
   * @param {Component|string} opts.component - Component to display
   * @param {Object} opts.componentProps - Properties to bind to the component
   * @returns {Promise} Promise that resolves when the user closes the modal with a value
   */
  openOverlayModal: (opts) => {
    overlayModalState.opts = {
      component: opts.component,
      componentProps: opts.componentProps ?? {},
      mode: opts.mode ?? 'overlay'
    }
    return new Promise((resolve, reject) => {
      overlayModalState.promiseResolve = resolve
      overlayModalState.promiseReject = reject
      overlayModalState.isShown = true
    })
  },
  /**
   * Close the active overlay modal
   */
  closeOverlayModal: () => {
    if (overlayModalState.promiseReject) {
      overlayModalState.isShown = false
      overlayModalState.promiseReject()
    }
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
