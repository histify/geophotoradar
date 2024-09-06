import { defineNuxtConfig } from "nuxt/config";

const isProduction = process.env.NODE_ENV === "production";

export default defineNuxtConfig({
  devtools: { enabled: false },
  ssr: false,
  modules: [
    "@nuxtjs/tailwindcss",
    "@nuxt/icon",
    "@nuxt/eslint",
    "@vite-pwa/nuxt",
  ],
  vite: {
    build: {
      target: "esnext",
    },
  },
  pwa: {
    registerType: "autoUpdate",
    manifest: {
      name: "geophotoradar",
      short_name: "geophotoradar",
      description: "geophotoradar",
      theme_color: "#3b82f6",
    },
    pwaAssets: {
      config: true,
    },
    client: {
      periodicSyncForUpdates: 3600,
    },
    devOptions: {
      enabled: !isProduction,
      type: "module",
    },
    workbox: {
      globPatterns: ["**/*.{js,css,html,png,svg,ico}"],
    },
    injectManifest: {
      globPatterns: ["**/*.{js,css,html,png,svg,ico}"],
    },
  },
  compatibilityDate: "2024-09-06",
});
