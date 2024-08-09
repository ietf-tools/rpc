import type { InjectionKey } from 'vue'

export const overlayModalMethodsKey = Symbol() as InjectionKey<{
    ok: (val?: string) => void,
    cancel: () => void,
}>