<template>
  <div
    v-for="(radarPoint, index) in radarPoints"
    :key="index"
    class="absolute size-4 origin-center rounded-full bg-blue-400"
    :style="radarPoint"
    style="z-index: 9999"
  />
  <div id="map" class="h-screen w-screen" />
</template>
<script setup>
import { map as lodashMap } from "lodash-es";
import {
  useGeolocation,
  useDeviceOrientation,
  useWindowSize,
} from "@vueuse/core";
import { computed, toValue } from "vue";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

const { coords } = useGeolocation();
const { alpha } = useDeviceOrientation();
const { data } = useFetchPhotos(coords, 1000);
const { width, height } = useWindowSize();
const router = useRouter();

const orientation = computed(() => toValue(alpha) * (Math.PI / 180));
const windowCenter = computed(() => ({
  x: toValue(width) / 2,
  y: toValue(height) / 2,
}));
const radius = computed(() => toValue(width) / 2 - 16);

const pointsInProximity = computed(() =>
  lodashMap(toValue(data), "coordinates"),
);
const radarPoints = computed(() => {
  return toValue(pointsInProximity).map((point) => {
    const beta = Math.tanh(
      (point.lat - toValue(coords).latitude) /
        (point.lon - toValue(coords).longitude),
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
      transform: `translate(${tangentPoint.x - 16}px, ${tangentPoint.y - 16}px)`,
    };
  });
});

const initialZoom = 20;
const layer = {
  url: "https://wmts.geo.admin.ch/1.0.0/ch.swisstopo.pixelkarte-farbe/default/current/3857/{z}/{x}/{y}.jpeg",
  attribution: "© swisstopo",
};

let map = null;
const me = L.marker();
const photosLayer = L.layerGroup();

onMounted(() => {
  map = L.map("map", { zoomControl: false });
  L.tileLayer(layer.url, { attribution: layer.attribution }).addTo(map);
  photosLayer.addTo(map);
  me.addTo(map);
});

watch(coords, ({ latitude, longitude }) => {
  me.setLatLng([latitude, longitude]);
  map.setView(new L.LatLng(latitude, longitude), initialZoom);
});

function placePhotos(photos) {
  photosLayer.clearLayers();
  photos.forEach(({ coordinates: { lat, lon }, image_url, iiif_url }) => {
    const marker = L.marker([lat, lon]).bindPopup(
      `<img src="${image_url}" />`,
      {
        maxWidth: 200,
        minWidth: 200,
        maxHeight: 200,
        minHeight: 200,
      },
    );
    marker.on("popupopen", function () {
      const popupContent = document.querySelector(".leaflet-popup-content");
      popupContent.addEventListener("click", () => {
        router.push({ name: "iiif", query: { manifestURL: iiif_url } });
      });
    });
    marker.addTo(photosLayer);
  });
}
watch(data, placePhotos);
</script>
