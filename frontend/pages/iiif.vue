<template>
  <div id="iiif-viewer" class="h-screen w-screen" />
</template>
<script setup>
import "tify";
import "tify/dist/tify.css";
import { isNull } from "lodash-es";

const tify = ref(null);
const route = useRoute();

function constructManifestURL(imageURL) {
  return imageURL.replace(/\/files\/.*/, "/pages/1/manifest/");
}

function openViewer() {
  tify.value = new window.Tify({
    container: "#iiif-viewer",
    manifestUrl: constructManifestURL(route.query.manifestURL),
  });
}

function destroyViewer() {
  if (isNull(toValue(tify))) {
    return;
  }
  toValue(tify).destroy();
}

onMounted(() => {
  openViewer();
});

onBeforeUnmount(() => {
  destroyViewer();
});
</script>
