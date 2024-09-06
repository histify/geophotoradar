import { useFetch } from "@vueuse/core";

function constructURL(coordinates, radius) {
  const { latitude, longitude } = toValue(coordinates);
  const url = new URL(window.location.origin);
  url.pathname = "/api/photos";
  url.searchParams.set("latitude", latitude);
  url.searchParams.set("longitude", longitude);
  url.searchParams.set("radius", toValue(radius));
  return url.toString();
}

export default function (coordinates, radius) {
  const url = computed(() => constructURL(coordinates, radius));
  return useFetch(url, { refetch: true }).get().json();
}
