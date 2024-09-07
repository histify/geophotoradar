<template>
  <div id="map" class="h-screen w-screen" />
</template>
<script setup>
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import { useGeolocation } from "@vueuse/core";

const { coords } = useGeolocation();
const router = useRouter();

const initialZoom = 20;
const layer = {
  url: "https://wmts.geo.admin.ch/1.0.0/ch.swisstopo.pixelkarte-farbe/default/current/3857/{z}/{x}/{y}.jpeg",
  attribution: "© swisstopo",
};

let map = null;
const me = L.marker();
const { data } = useFetchPhotos(coords, 1000);
const photosLayer = L.layerGroup();

onMounted(() => {
  map = L.map("map", { zoomControl: false, dragging: false, tap: false });
  map.dragging.disable();
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
