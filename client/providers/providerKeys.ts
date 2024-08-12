import type { InjectionKey, VNode, Component } from 'vue'

export const overlayModalKey = Symbol() as InjectionKey<{
   /**
   * Open an overlay modal
   */
    openOverlayModal: (opts: {
        component: null | VNode | Component,
        componentProps?: null | Record<string, unknown>,
        mode?: "overlay" | "side"
    }) => Promise<void>
    closeOverlayModal: () => void
}>

export const overlayModalMethodsKey = Symbol() as InjectionKey<{
    ok: (val?: string) => void,
    cancel: () => void,
}>

export const assignEditorKey = Symbol() as InjectionKey<
    (doc: unknown, editor: unknown) => void
>

export const deleteAssignmentKey = Symbol() as InjectionKey<
    (assignment: unknown) => void
>