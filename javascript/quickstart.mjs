/**
 * Korea DART Corporate API — Node/browser quickstart.
 *
 * Get a free key (Basic plan, 3,000 requests/month): https://rapidapi.com/krdartapi/api/krdart
 * Docs: https://dart.ryanpp.com/openapi.yaml
 *
 *   RAPIDAPI_KEY=your_key node quickstart.mjs
 */

const BASE = "https://krdart.p.rapidapi.com";
const headers = {
  "X-RapidAPI-Key": process.env.RAPIDAPI_KEY,
  "X-RapidAPI-Host": "krdart.p.rapidapi.com",
};

const get = async (path, params = {}) => {
  const url = new URL(BASE + path);
  for (const [k, v] of Object.entries(params)) if (v !== undefined) url.searchParams.set(k, v);
  const r = await fetch(url, { headers });
  if (!r.ok) throw new Error(`${path} → HTTP ${r.status}`);
  return r.json();
};

const search      = (q, limit = 10) => get("/companies/search", { q, limit });
const company     = (code) => get(`/companies/${code}`);
const financials  = (code, year = 2024, reprt = "11011") => get(`/financials/${code}`, { year, reprt });
const distress    = (code) => get(`/distress/${code}`);
const events      = (days = 7, type, limit = 50) => get("/events/recent", { days, type, limit });

// ── demo
const hits = (await search("samsung", 3)).results;
console.log("SEARCH →", hits.map((h) => [h.corp_code, h.corp_name_eng]));

const code = hits[0].corp_code;
console.log("COMPANY →", await company(code));

const fin = await financials(code, 2024);
console.log(`FINANCIALS → ${fin.count} items`);
for (const item of fin.items.slice(0, 5)) {
  console.log(`  ${item.statement.padEnd(20)} ${item.account_name_en.padEnd(30)} ${item.current_amount?.toLocaleString()}`);
}

console.log("DISTRESS →", await distress(code));

const del = await events(30, "DELISTING_RISK", 10);
console.log(`DELISTING_RISK (30d) → ${del.count} events`);
for (const ev of del.results.slice(0, 5)) {
  console.log(`  ${ev.event_dt}  sev=${ev.severity}  ${ev.corp_name}  ${ev.detail.slice(0, 80)}`);
}
