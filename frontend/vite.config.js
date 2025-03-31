import { fileURLToPath, URL } from 'node:url'
import path from 'path';

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import createSvgSpritePlugin from 'vite-plugin-svg-spriter'
import svgLoader from 'vite-svg-loader';

const SVG_FOLDER_PATH = path.resolve(path.resolve(__dirname, 'src'), 'assets', 'icons')

// https://vite.dev/config/
export default defineConfig({
  server: {
    hmr: true
  },
  plugins: [
    vue(),
    vueDevTools(),
    createSvgSpritePlugin({svgFolder: SVG_FOLDER_PATH}),
    svgLoader(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
})
