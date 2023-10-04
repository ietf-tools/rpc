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
      const profileData = await $fetch('/api/rpc/profile')
      this.id = profileData.id
      this.authenticated = profileData.authenticated
      this.name = profileData.name
    }
  }
})
