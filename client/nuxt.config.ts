// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  colorMode: {
    preference: 'light',
    classSuffix: '',
    fallback: 'light'
  },
  devServer: {
    port: 3000,
    url: 'http://localhost:8088'
  },
  devtools: {
    enabled: true
  },
  headlessui: {
    prefix: 'Headless'
  },
  modules: [
    '@nuxt/devtools',
    '@nuxtjs/color-mode',
    '@nuxtjs/tailwindcss',
    '@nuxtjs/robots',
    '@pinia/nuxt',
    'nuxt-headlessui',
    'nuxt-icon',
    'nuxt-svgo'
  ],
  robots: {
    rules: [
      { UserAgent: '*' },
      { Disallow: '/' }
    ]
  },
  tailwindcss: {
    viewer: false
  }
})
