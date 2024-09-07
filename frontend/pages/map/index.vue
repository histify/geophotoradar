<template>
  <div id="map" class="h-screen w-screen" />
  <Navigation />
</template>
<script setup>
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import { useGeolocation, watchOnce } from "@vueuse/core";
import pinIconPath from "~/assets/icons/twemoji--brain.png";
import meIconPath from "~/assets/icons/fluent-emoji--person-zombie.png";

const { coords } = useGeolocation();
const router = useRouter();

const pinIcon = L.icon({
  iconUrl: pinIconPath,
  iconSize: [38, 38],
  iconAnchor: [0, 38],
  popupAnchor: [19, -38],
});

const meIcon = L.icon({
  iconUrl: meIconPath,
  iconSize: [38, 38],
  iconAnchor: [0, 38],
  popupAnchor: [19, -38],
});

const layer = {
  url: "https://wmts.geo.admin.ch/1.0.0/ch.swisstopo.pixelkarte-farbe/default/current/3857/{z}/{x}/{y}.jpeg",
  attribution: "© swisstopo",
};

let map = null;
const me = L.marker([], { icon: meIcon });
const { data } = useFetchPhotos(coords, 1000);
const photosLayer = L.layerGroup();

onMounted(() => {
  map = L.map("map", { zoomControl: false });
  L.tileLayer(layer.url, { attribution: layer.attribution }).addTo(map);
  photosLayer.addTo(map);
  me.addTo(map);
});

watch(coords, ({ latitude, longitude }) => {
  me.setLatLng([latitude, longitude]);
});

watchOnce(coords, ({ latitude, longitude }) => {
  map.setView(new L.LatLng(latitude, longitude), 30);
});

function placePhotos(photos) {
  photosLayer.clearLayers();
  photos.forEach(({ coordinates: { lat, lon }, image_url, iiif_url }) => {
    const marker = L.marker([lat, lon], { icon: pinIcon }).bindPopup(
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
