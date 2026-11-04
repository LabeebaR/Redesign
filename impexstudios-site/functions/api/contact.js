// Cloudflare Pages Function: POST /api/contact
// Forwards form submissions to your automation webhook (n8n, Make, GoHighLevel, Zapier...).
// Set it in Cloudflare: Pages project > Settings > Variables and Secrets > add WEBHOOK_URL.
export async function onRequestPost({ request, env }) {
  const wantsJson = (request.headers.get("Accept") || "").includes("application/json");
  const reply = (ok, error, status) => wantsJson
    ? Response.json(ok ? { ok: true } : { ok: false, error }, { status })
    : Response.redirect(new URL(ok ? "/thanks/" : "/contact/?error=1", request.url), 303);

  let data = {};
  try {
    const type = request.headers.get("Content-Type") || "";
    if (type.includes("application/json")) data = await request.json();
    else { const fd = await request.formData(); for (const [k, v] of fd) data[k] = data[k] ? `${data[k]}, ${v}` : v; }
  } catch { return reply(false, "We couldn't read the form.", 400); }

  // Honeypot: bots fill hidden fields. Pretend success, send nothing.
  if (data.company_url) return reply(true, null, 200);

  const email = String(data.email || "").trim();
  if (!data.name || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || !data.message)
    return reply(false, "Please add your name, a valid email and a message.", 422);

  if (!env.WEBHOOK_URL) return reply(false, "The form isn't connected yet.", 500);

  const payload = {
    ...Object.fromEntries(Object.entries(data).map(([k, v]) => [k, String(v).slice(0, 5000)])),
    submitted_at: new Date().toISOString(),
    country_detected: request.cf?.country || null,
    region_detected: request.cf?.region || null,
  };
  delete payload.company_url;

  try {
    const r = await fetch(env.WEBHOOK_URL, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) });
    if (!r.ok) throw new Error(String(r.status));
  } catch { return reply(false, "Our system didn't accept the message.", 502); }

  return reply(true, null, 200);
}
