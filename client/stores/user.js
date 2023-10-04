import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    id: null,
    authenticated: false,
    name: 'Guest',
    email: '',
    avatar: ''
  }),
  getters: { },
  actions: {
    async refreshAuth () {
      console.debug('Refreshing auth...')
      // TODO: do stuff
    }
  }
})
