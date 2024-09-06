import { defineStore } from 'pinia'

export type ProfileData = {
  authenticated: boolean
  id: string | null
  name: string | null
  email: string | null
  avatar: string | null
  rpcPersonId: number | null
  isManager: boolean
}

type PretendingToBe = {
  pretendingToBe: number | null
}

export const useUserStore = defineStore('user', {
  state: () => {
    const defaultState: ProfileData & PretendingToBe = {
      authenticated: false,
      id: null,
      name: 'Guest',
      email: '',
      avatar: '',
      rpcPersonId: null,
      isManager: false,
      pretendingToBe: null // demo/debug only!
    }
    return defaultState
  },
  getters: {},
  actions: {
    async refreshAuth () {
      const profileData = await $fetch<ProfileData>(
        this.pretendingToBe
          ? `/api/rpc/profile/${this.pretendingToBe}`
          : '/api/rpc/profile/'
      )
      this.authenticated = profileData.authenticated
      if (profileData.authenticated) {
        this.id = profileData.id
        this.name = profileData.name
        this.email = profileData.email
        this.avatar = profileData.avatar
        this.rpcPersonId = profileData.rpcPersonId
        this.isManager = profileData.isManager
      }
    },
    async pretendToBe (rpcPersonId: number | null) {
      this.pretendingToBe = rpcPersonId
      return await this.refreshAuth()
    }
  }
})
