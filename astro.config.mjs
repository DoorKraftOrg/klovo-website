// @ts-check
import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';
import vercel from '@astrojs/vercel';

export default defineConfig({
  site: 'https://www.klovo.com',
  output: 'static',
  adapter: vercel(),
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
    // Shopify legacy /pages/* URLs — preserve SEO equity with 301s to existing Astro pages
    '/pages/about': '/about',
    '/pages/contact': '/contact',
    '/pages/warranty': '/warranty',
    '/pages/assembly': '/assembly',
    '/pages/where-to-buy': '/where-to-buy',
    '/pages/frequently-asked-questions': '/faq',
    '/pages/retailers': '/for-retailers',
    '/pages/how-it-works': '/assembly',
    '/pages/pro': '/for-retailers',
    '/pages/dealers': '/where-to-buy',
    '/pages/builders': '/for-retailers',
    '/pages/trade': '/contact',
    '/pages/plan': '/',
    '/pages/rendering': '/',
    '/pages/configurator': '/sets/',
    // Shopify /blog alias → canonical blog index
    '/blog': '/blogs/news',
    '/blog/': '/blogs/news',
    '/blogs': '/blogs/news',
    // Shopify /collections/* → Astro sets hub (safety catches for old inbound links)
    '/collections/all': '/sets/',
    '/collections/kits-bundles': '/sets/',
    '/collections/garage-cabinet-sets': '/sets/',
  },
  vite: {
    plugins: [tailwindcss()],
  },
});
