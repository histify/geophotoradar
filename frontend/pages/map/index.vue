<template>
  <div id="map" class="h-screen w-screen"></div>
</template>
<script setup>
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import { useGeolocation } from "@vueuse/core";

const { coords } = useGeolocation();

const initialPosition = [46.801111, 8.226667];
const initialZoom = 20;
const layer = {
  url: "https://wmts.geo.admin.ch/1.0.0/ch.swisstopo.pixelkarte-farbe/default/current/3857/{z}/{x}/{y}.jpeg",
  attribution: "© swisstopo",
};

let map = null;
const me = L.marker(initialPosition);
const { data } = useFetchPhotos(coords, 0);

onMounted(() => {
  map = L.map("map", { zoomControl: false });
  L.tileLayer(layer.url, { attribution: layer.attribution }).addTo(map);
  me.addTo(map);
});

watch(coords, ({ latitude, longitude }) => {
  me.setLatLng([latitude, longitude]);
  map.setView(new L.LatLng(latitude, longitude), initialZoom);
});

function placePhotos(photos) {
  photos.forEach(({ coordinates: { coordinates } }) => {
    L.marker(coordinates).addTo(map);
  });
}
watch(data, placePhotos);
</script>
