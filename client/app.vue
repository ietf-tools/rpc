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

<script setup lang="ts">
import { overlayModalKey } from './providers/providerKeys'
import type { OverlayModal } from './providers/providerKeys'

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
    return titleChunk ? `${titleChunk} - RFC Production Center` : 'RFC Production Center'
  }
})

// OVERLAY MODAL

type OverlayModalState = {
  isShown: boolean
  opts: Parameters<OverlayModal['openOverlayModal']>[0]
  promiseResolve?: (value?: string | PromiseLike<string | undefined>) => void
  promiseReject?: (reason?: any) => void
}

const overlayModalState = shallowReactive<OverlayModalState>({
  isShown: false,
  opts: {
    component: undefined,
    componentProps: undefined
  },
  promiseResolve: undefined,
  promiseReject: undefined
})

provide(overlayModalKey, {
  openOverlayModal: (opts) => {
    overlayModalState.opts = {
      component: opts.component,
      componentProps: opts.componentProps ?? {},
      mode: opts.mode ?? 'overlay'
    }
    return new Promise<string | undefined>((resolve, reject) => {
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
