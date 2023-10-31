import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    id: null,
    authenticated: false,
    name: 'Guest',
    email: '',
    avatar: '',
    isManager: false,
    pretendingToBe: null // demo/debug only!
  }),
  getters: {},
  actions: {
    async refreshAuth () {
      const profileData = await $fetch(
        this.pretendingToBe
          ? `/api/rpc/profile/${this.pretendingToBe}`
          : '/api/rpc/profile/'
      )
      this.authenticated = profileData.authenticated
      if (this.authenticated) {
        this.id = profileData.id
        this.name = profileData.name
        this.email = profileData.email
        this.avatar = profileData.avatar
        this.isManager = profileData.isManager
      }
    },
    async pretendToBe (rpcPersonId) {
      this.pretendingToBe = rpcPersonId
      return await this.refreshAuth()
    }
  }
})
