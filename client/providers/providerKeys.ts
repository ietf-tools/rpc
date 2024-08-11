import type { InjectionKey, VNode } from 'vue'

export const overlayModalKey = Symbol() as InjectionKey<{
   /**
   * Open an overlay modal
   */
    openOverlayModal: (opts: { component: VNode | string, componentProps: unknown, mode: string}) => Promise<void>
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