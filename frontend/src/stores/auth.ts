import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthed: localStorage.getItem('isAuthed') === 'true',
    csrfToken: localStorage.getItem('csrfToken') || ''
  }),
  actions: {
    setAuthed(v: boolean) {
      this.isAuthed = v
      localStorage.setItem('isAuthed', String(v))
    },
    setCsrf(token: string) {
      this.csrfToken = token
      localStorage.setItem('csrfToken', token)
    }
  }
})