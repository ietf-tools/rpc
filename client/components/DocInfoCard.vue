<template>
  <BaseCard>
    <template #header>
      <h3 class="text-base font-semibold">Document Info</h3>
    </template>
    <div class="lg:col-span-2 lg:row-span-2 lg:row-start-1 grid place-items-stretch">
      <div v-if="draft">
        <div class="mx-4 pb-3 text-sm font-medium">
          <dl>
            <div class="px-4 pt-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt>Title</dt>
              <dd class="mt-1 leading-6 sm:col-span-2 sm:mt-0">
                {{ draft.title }}
              </dd>
            </div>
            <div class="px-4 pt-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt>Authors</dt>
              <dd class="mt-1 leading-6 sm:col-span-2 sm:mt-0">
                J. Doe (mocked)
              </dd>
            </div>
            <div class="px-4 pt-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt>Submitted Pages</dt>
              <dd class="mt-1 leading-6 sm:col-span-2 sm:mt-0">
                {{ draft.pages }}
              </dd>
            </div>
            <div class="px-4 pt-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt>Document Shepherd</dt>
              <dd class="mt-1 leading-6 sm:col-span-2 sm:mt-0">
                Dolly Shepherd (mocked)
              </dd>
            </div>
            <div class="px-4 pt-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt>Stream</dt>
              <dd class="mt-1 leading-6 sm:col-span-2 sm:mt-0">
                {{ draft.stream }}
                <span v-if="draft.submittedStream !== draft.stream">
                        (submitted as {{ draft.submittedStream }})
                      </span>
              </dd>
            </div>
            <div class="px-4 pt-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt>Stream Manager</dt>
              <dd class="mt-1 leading-6 sm:col-span-2 sm:mt-0">
                Ari Drecker (mocked)
              </dd>
            </div>
            <div class="px-4 pt-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt>Submitted Format</dt>
              <dd class="mt-1 leading-6 sm:col-span-2 sm:mt-0">
                {{ draft.submittedFormat }}
              </dd>
            </div>
            <div class="px-4 pt-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt>Submitted Boilerplate</dt>
              <dd class="mt-1 leading-6 sm:col-span-2 sm:mt-0">
                {{ draft.intendedBoilerplate }}
                <span v-if="draft.submittedBoilerplate !== draft.intendedBoilerplate">
                        (submitted as {{ draft.submittedBoilerplate }})
                      </span>
              </dd>
            </div>
            <div class="px-4 pt-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt>Standard Level</dt>
              <dd class="mt-1 leading-6 sm:col-span-2 sm:mt-0">
                {{ draft.intendedStdLevel }}
                <span v-if="draft.submittedStdLevel !== draft.intendedStdLevel">
                        (submitted as {{ draft.submittedStdLevel }})
                      </span>
              </dd>
            </div>
            <div class="px-4 pt-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt>Disposition</dt>
              <dd class="mt-1 leading-6 sm:col-span-2 sm:mt-0">
                {{ draft.disposition }}
              </dd>
            </div>
          </dl>
        </div>
      </div>
    </div>
  </BaseCard>
</template>

<script setup lang="ts">

import type { RfcToBe } from '~/rpctracker_client'

type Props = {
  draft: RfcToBe | null
}

defineProps<Props>()

</script>
