<template>
  <div
    v-for="(radarPoint, index) in radarPoints"
    :key="index"
    class="absolute z-10 size-4 origin-center rounded-full bg-blue-400 opacity-80"
    :style="radarPoint"
  />
  <div class="flex h-screen flex-col items-center justify-center">
    <span class="mb-10 font-bold text-white"
      >{{ pointsInProximityCount }} pictures nearby</span
    >
    <div class="flex w-full snap-x snap-mandatory items-center overflow-x-auto">
      <nuxt-link
        v-for="photoInProximity in photosInProximity"
        :key="photoInProximity.id"
        :to="{
          name: 'iiif',
          query: { manifestURL: photoInProximity.iiif_url },
        }"
        class="flex shrink-0 snap-center flex-col"
        style="max-width: 100%; height: auto"
      >
        <img :src="photoInProximity.image_url" class="object-contain" />
        <span class="px-2 text-white">{{ photoInProximity.title }}</span>
      </nuxt-link>
    </div>
  </div>
  <Navigation />
</template>
<script setup>
import {
  useGeolocation,
  useDeviceOrientation,
  useWindowSize,
} from "@vueuse/core";
import { size } from "lodash-es";

const { coords } = useGeolocation();
const { alpha } = useDeviceOrientation();
const { data } = useFetchPhotos(coords, 1000);
const { width, height } = useWindowSize();

const orientation = computed(() => toValue(alpha) * (Math.PI / 180));
const windowCenter = computed(() => ({
  x: toValue(width) / 2,
  y: toValue(height) / 2,
}));
const radius = computed(() => toValue(width) / 2 - 16);

const radarPoints = computed(() => {
  return (toValue(data) || []).map(({ coordinates: { lat, lon } }) => {
    const beta = Math.tanh(
      (lat - toValue(coords).latitude) / (lon - toValue(coords).longitude),
    );
    const tangentPoint = {
      x:
        toValue(windowCenter).x +
        toValue(radius) *
          Math.cos(toValue(beta) + toValue(orientation) - Math.PI / 2),
      y:
        toValue(windowCenter).y +
        toValue(radius) *
          Math.sin(toValue(beta) + toValue(orientation) - Math.PI / 2),
    };
    return {
      transform: `translate(${tangentPoint.x - 16}px, ${tangentPoint.y - 16}px) scale(1.2)`,
    };
  });
});

const photosInProximity = computed(() => {
  return (toValue(data) || []).filter((o) => o.distance <= 400);
});
const pointsInProximityCount = computed(() => size(toValue(photosInProximity)));
</script>
