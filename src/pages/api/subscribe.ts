import type { APIRoute } from 'astro';
import { addSubscriber, type SubscriberSource } from '../../lib/notion';
import { sendWelcomeEmail } from '../../lib/email';

export const prerender = false;

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const ALLOWED_SOURCES: SubscriberSource[] = ['footer', 'homepage', 'other'];

export const POST: APIRoute = async ({ request }) => {
  const form = await request.formData();
  const email = String(form.get('email') || '').trim().toLowerCase();
  const rawSource = String(form.get('source') || 'other');
  const source: SubscriberSource = (ALLOWED_SOURCES as string[]).includes(rawSource)
    ? (rawSource as SubscriberSource)
    : 'other';

  const redirectTo = (path: string) =>
    new Response(null, { status: 303, headers: { Location: path } });

  if (!EMAIL_RE.test(email) || email.length > 254) {
    return redirectTo('/subscribed?error=invalid');
  }

  const notionResult = await addSubscriber({ email, source });
  if (!notionResult.ok) {
    console.error('[subscribe] notion error:', notionResult.error);
  }

  const emailResult = await sendWelcomeEmail(email);
  if ('skipped' in emailResult && emailResult.skipped) {
    console.log('[subscribe] email send skipped (no RESEND_API_KEY)');
  } else if ('error' in emailResult) {
    console.error('[subscribe] resend error:', emailResult.error);
  }

  return redirectTo('/subscribed');
};
