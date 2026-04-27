import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const sets = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/sets' }),
  schema: z.object({
    sku: z.string(),
    upc: z.string().optional(),
    title: z.string(),
    longTitle: z.string(),
    seoTitle: z.string().optional(),
    widthFt: z.number(),
    widthIn: z.number(),
    heightIn: z.number().default(84),
    depthIn: z.number().default(18),
    pieces: z.number(),
    drawers: z.number().default(0),
    msrp: z.number(),
    shortDescription: z.string(),
    includedComponents: z.string(),
    features: z.array(z.string()),
    specialFeatures: z.array(z.string()).optional(),
    keywords: z.string().optional(),
    image: z.string(),
    angleImages: z.array(z.string()).optional(),
    imagesAvailable: z.boolean().default(false),
    useCaseTags: z.array(z.string()).optional(),
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
    imageAlt: z.string().optional(),
    author: z.string().default('Klovo Team'),
    tags: z.array(z.string()).default([]),
    canonical: z.string().optional(),
    draft: z.boolean().default(false),
  }),
});

export const collections = { sets, blog };
