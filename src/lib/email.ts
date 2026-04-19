import { Resend } from 'resend';

export async function sendWelcomeEmail(
  email: string
): Promise<{ sent: true } | { sent: false; skipped: true } | { sent: false; error: string }> {
  const apiKey = import.meta.env.RESEND_API_KEY;
  const fromEmail = import.meta.env.FROM_EMAIL || 'hello@klovo.com';

  if (!apiKey) {
    return { sent: false, skipped: true };
  }

  const resend = new Resend(apiKey);

  try {
    await resend.emails.send({
      from: `Klovo <${fromEmail}>`,
      to: email,
      subject: "You're on the Klovo list",
      text: welcomeText(),
      html: welcomeHtml(),
    });
    return { sent: true };
  } catch (err) {
    const message = err instanceof Error ? err.message : 'unknown error';
    return { sent: false, error: message };
  }
}

function welcomeText(): string {
  return `Hey —

You're on the Klovo newsletter list. Expect garage tips, new products, and the occasional dad joke. No spam, ever.

If you're here to build your setup, our full collection is at https://www.klovo.com/sets/.

— The Klovo team
`;
}

function welcomeHtml(): string {
  return `<!doctype html>
<html>
  <body style="margin:0;padding:0;background:#F8F5F0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;color:#272727;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#F8F5F0;padding:48px 16px;">
      <tr>
        <td align="center">
          <table role="presentation" width="560" cellpadding="0" cellspacing="0" style="max-width:560px;background:#FFFFFF;border-radius:12px;padding:40px;">
            <tr>
              <td>
                <p style="margin:0 0 8px;font-size:13px;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:#F7C948;">You're in.</p>
                <h1 style="margin:0 0 20px;font-size:28px;line-height:1.2;color:#272727;">Welcome to the Klovo list.</h1>
                <p style="margin:0 0 16px;font-size:16px;line-height:1.6;color:#272727;">Hey —</p>
                <p style="margin:0 0 16px;font-size:16px;line-height:1.6;color:#272727;">You're on the list. Expect garage tips, new products, and the occasional dad joke. No spam, ever.</p>
                <p style="margin:0 0 32px;font-size:16px;line-height:1.6;color:#272727;">If you're here to build your setup, start with the preset collection:</p>
                <p style="margin:0 0 32px;">
                  <a href="https://www.klovo.com/sets/" style="display:inline-block;padding:14px 24px;background:#0E4C8B;color:#FFFFFF;text-decoration:none;border-radius:6px;font-weight:600;font-size:15px;">See our sets</a>
                </p>
                <p style="margin:0;font-size:14px;line-height:1.6;color:#858485;">— The Klovo team</p>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>`;
}
