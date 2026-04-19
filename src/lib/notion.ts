import { Client } from '@notionhq/client';

export type SubscriberSource = 'footer' | 'homepage' | 'other';

export async function addSubscriber({
  email,
  source,
}: {
  email: string;
  source: SubscriberSource;
}): Promise<{ ok: true } | { ok: false; error: string }> {
  const token = import.meta.env.NOTION_TOKEN;
  const databaseId = import.meta.env.NOTION_SUBSCRIBERS_DB_ID;

  if (!token || !databaseId) {
    return { ok: false, error: 'Notion env vars missing' };
  }

  const notion = new Client({ auth: token });

  try {
    await notion.pages.create({
      parent: { database_id: databaseId },
      properties: {
        Email: { title: [{ text: { content: email } }] },
        'Subscribed Date': { date: { start: new Date().toISOString() } },
        Source: { select: { name: source } },
        Status: { select: { name: 'Active' } },
      },
    });
    return { ok: true };
  } catch (err) {
    const message = err instanceof Error ? err.message : 'unknown error';
    return { ok: false, error: message };
  }
}
