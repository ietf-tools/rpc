import vue from 'eslint-plugin-vue'
import globals from 'globals'
import parser from 'vue-eslint-parser'
import eslint from '@eslint/js'
import neostandard from 'neostandard'
import withNuxt from './.nuxt/eslint.config.mjs'

export default withNuxt(
  ...neostandard(),
  eslint.configs.recommended, {
    plugins: {
      vue
    },

    languageOptions: {
      globals: {
        ...globals.browser,
        ...globals.node,
        ...vue.environments['setup-compiler-macros']['setup-compiler-macros'],
        d3: true
      },

      parser,
      ecmaVersion: 'latest',
      sourceType: 'module',

      parserOptions: {
        parser: '@typescript-eslint/parser'
      }
    },

    rules: {
      'vue/script-setup-uses-vars': 'error',
      'vue/multi-word-component-names': 'off',
      'vue/max-attributes-per-line': 'off',
      'vue/singleline-html-element-content-newline': 'off',
      'no-undef': 'off',
      '@typescript-eslint/consistent-type-definitions': 'off',
      '@typescript-eslint/no-explicit-any': 'off',
      '@typescript-eslint/ban-ts-comment': 'off',
      '@typescript-eslint/no-unused-vars': 'off'
    }
  }, {
    ignores: [
      '.nuxt/',
      '.output/',
      'rpctracker_client/'
    ]
  }
)
