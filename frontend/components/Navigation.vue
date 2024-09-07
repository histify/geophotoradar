<template>
  <div class="fixed bottom-0 flex h-16 w-screen bg-white" style="z-index: 9999">
    <nuxt-link
      active-class="bg-blue-200"
      class="flex grow items-center justify-center"
      :to="{ name: 'index' }"
      ><Icon size="40" name="icon-park:radar-two"
    /></nuxt-link>
    <nuxt-link
      active-class="bg-blue-200"
      class="flex grow items-center justify-center"
      :to="{ name: 'map' }"
      ><Icon size="40" name="icon-park:map-draw"
    /></nuxt-link>
  </div>
</template>
