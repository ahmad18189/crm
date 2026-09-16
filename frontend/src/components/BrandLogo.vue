<template>
  <div
    v-if="brand?.logo"
    class="flex items-center justify-center overflow-hidden rounded-md bg-white p-0.5"
  >
    <img :src="brand.logo" class="h-full w-full object-cover" />
  </div>
  <CRMLogo v-else class="size-8 shrink-0 rounded-md bg-white p-0.5" />
</template>

<script setup>
import CRMLogo from '@/components/Icons/CRMLogo.vue'

const brand = defineModel({ type: Object, default: () => ({}) })
</script>
