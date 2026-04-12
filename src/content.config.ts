import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const products = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/products' }),
  schema: z.object({
    title: z.string(),
    collection: z.string(),
    description: z.string(),
    image: z.string(),
    price: z.string().optional(),
    specs: z.object({
      width: z.string(),
      height: z.string(),
      depth: z.string(),
      weight: z.string(),
      shelfCapacity: z.string(),
      material: z.string(),
      shelves: z.number().optional(),
      drawers: z.number().optional(),
    }),
    features: z.array(z.string()),
    retailers: z.array(z.object({
      name: z.string(),
      url: z.string(),
    })).optional(),
    order: z.number().default(0),
  }),
});

const cabinetCollections = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/collections' }),
  schema: z.object({
    title: z.string(),
    slug: z.string(),
    description: z.string(),
    image: z.string(),
    order: z.number().default(0),
  }),
});

const blog = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.coerce.date(),
    image: z.string().optional(),
    author: z.string().default('Klovo Team'),
  }),
});

export const collections = { products, cabinetCollections, blog };
