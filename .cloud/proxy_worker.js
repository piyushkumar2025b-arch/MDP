export default {
  async fetch(request, env) {
    const { pathname } = new URL(request.url);

    if (pathname === "/api/log-molecule") {
      const { cid, smiles, lead_score, grade } = await request.json();
      await env.DB.prepare(
        "INSERT INTO molecules (cid, smiles, lead_score, grade) VALUES (?, ?, ?, ?)"
      ).bind(cid, smiles, lead_score, grade).run();
      return new Response("Logged to D1 Edge", { status: 200 });
    }

    if (pathname === "/api/get-discovery-stats") {
      const stats = await env.DB.prepare(
        "SELECT COUNT(*) as total, AVG(lead_score) as avg_score FROM molecules"
      ).first();
      return new Response(JSON.stringify(stats), {
        headers: { "Content-Type": "application/json" },
      });
    }

    return new Response("ChemoFilter v1M Edge API Online", { status: 200 });
  },
};
