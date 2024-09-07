<template>
  <div
    v-for="(radarPoint, index) in radarPoints"
    :key="index"
    class="absolute size-4 origin-center rounded-full bg-blue-400 opacity-80"
    :style="radarPoint"
  />
  <div class="flex h-screen snap-x snap-mandatory overflow-x-auto bg-black">
    <img
      v-for="photoInProximity in photosInProximity"
      :key="photoInProximity.id"
      :src="photoInProximity.image_url"
      class="snap-center object-contain"
    />
  </div>
  <Navigation />
</template>
<script setup>
import {
  useGeolocation,
  useDeviceOrientation,
  useWindowSize,
} from "@vueuse/core";

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
</script>
