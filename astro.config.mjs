// @ts-check
import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://www.klovo.com',
  integrations: [react(), sitemap()],
  redirects: {
    '/cabinets/': '/sets/',
    '/cabinets/tall/': '/sets/',
    '/cabinets/base/': '/sets/',
    '/cabinets/wall/': '/sets/',
    '/cabinets/tall/tall-cabinet-36/': '/sets/',
    '/cabinets/tall/tall-cabinet-24/': '/sets/',
    '/cabinets/base/base-cabinet-36/': '/sets/',
    '/cabinets/wall/wall-cabinet-36/': '/sets/',
    '/how-it-works/': '/assembly/',
  },
  vite: {
    plugins: [tailwindcss()],
  },
});
