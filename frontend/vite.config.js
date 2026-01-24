import { fileURLToPath, URL } from 'node:url'
import path from 'path';
import { createRequire } from 'node:module';

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import createSvgSpritePlugin from 'vite-plugin-svg-spriter'
import svgLoader from 'vite-svg-loader';

const require = createRequire(import.meta.url);
const SVG_FOLDER_PATH = path.resolve(path.resolve(__dirname, 'src'), 'assets', 'icons')

// https://vite.dev/config/
export default defineConfig(({ command }) => {
  const plugins = [
    vue(),
    createSvgSpritePlugin({svgFolder: SVG_FOLDER_PATH}),
    svgLoader(),
  ];

  // Only import and enable Vue DevTools in development mode (serve command)
  // This prevents the module from being loaded during build, avoiding localStorage errors
  if (command === 'serve') {
    try {
      const vueDevTools = require('vite-plugin-vue-devtools').default;
      plugins.push(vueDevTools());
    } catch (e) {
      // Plugin not available, ignore
    }
  }

  return {
    server: {
      hmr: true
    },
    plugins,
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      },
    },
  };
})
