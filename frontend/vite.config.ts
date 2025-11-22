import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  publicDir: 'static',
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        cookieDomainRewrite: 'localhost'
      }
    }
  },
  plugins: [
    vue(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['favicon.svg'],
      manifest: {
        name: 'BlackCat AI',
        short_name: 'BlackCat',
        theme_color: '#121212',
        display: 'standalone'
      },
      workbox: {
        runtimeCaching: [
          {
            urlPattern: ({url}) => url.pathname.startsWith('/api/records'),
            handler: 'NetworkFirst',
            options: {
              cacheName: 'records-cache',
              expiration: { maxEntries: 50, maxAgeSeconds: 7 * 24 * 3600 }
            }
          }
        ]
      }
    })
  ]
})