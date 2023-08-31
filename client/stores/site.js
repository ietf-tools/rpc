import { defineStore } from 'pinia'

export const useSiteStore = defineStore('site', {
  state: () => ({
    sidebarIsOpen: false
  }),
  getters: { },
  actions: { },
})
