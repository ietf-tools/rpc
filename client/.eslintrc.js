module.exports = {
  root: true,
  env: {
    browser: true,
    es2021: true,
    jquery: true,
    node: true,
    'vue/setup-compiler-macros': true
  },
  extends: [
    'standard',
    'plugin:nuxt/recommended',
    // 'plugin:vue/vue3-essential', // Priority A: Essential (Error Prevention)
    // 'plugin:vue/vue3-strongly-recommended' // Priority B: Strongly Recommended (Improving Readability)
    'plugin:@typescript-eslint/recommended',
    'plugin:@typescript-eslint/stylistic'
  ],
  globals: {
    d3: true
  },
  parser: 'vue-eslint-parser',
  parserOptions: {
    parser: '@typescript-eslint/parser',
    ecmaVersion: 'latest',
    sourceType: 'module'
  },
  plugins: [
    'vue'
  ],
  rules: {
    'vue/script-setup-uses-vars': 'error',
    'vue/multi-word-component-names': 'off',
    'vue/max-attributes-per-line': 'off',
    'vue/singleline-html-element-content-newline': 'off',
    'no-undef': 'off',
    '@typescript-eslint/consistent-type-definitions': 'off',
    '@typescript-eslint/no-explicit-any': 'off' // Reenable after types improve
  }
}
