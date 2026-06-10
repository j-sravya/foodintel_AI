const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8787";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail || `Request failed: ${response.status}`);
  }
  return response.json();
}

export const api = {
  categories: () => request("/categories"),
  login: (username, password) =>
    request("/auth/login", {
      method: "POST",
      body: JSON.stringify({ username, password }),
    }),
  areas: () => request("/areas"),
  prospects: (category, area) =>
    request(`/prospects?category=${encodeURIComponent(category)}${area ? `&area=${encodeURIComponent(area)}` : ""}`),
  commandCenter: (category, area) =>
    request(`/command-center?category=${encodeURIComponent(category)}${area ? `&area=${encodeURIComponent(area)}` : ""}`),
  brief: (prospectId, category) =>
    request(`/brief/${encodeURIComponent(prospectId)}?category=${encodeURIComponent(category)}`),
  opportunityRadar: (category) => request(`/opportunity-radar?category=${encodeURIComponent(category)}`),
  crmTimeline: (prospectId, category) =>
    request(`/crm-timeline/${encodeURIComponent(prospectId)}?category=${encodeURIComponent(category)}`),
  followup: (prospectId, category) =>
    request(`/followup/${encodeURIComponent(prospectId)}?category=${encodeURIComponent(category)}`),
  copilot: (question, prospectId, category) =>
    request("/copilot", {
      method: "POST",
      body: JSON.stringify({ question, prospectId, category }),
    }),
  workflow: () => request("/ai-workflow"),
  billingPlans: () => request("/billing/plans"),
  checkout: (plan) =>
    request("/billing/checkout", {
      method: "POST",
      body: JSON.stringify({ plan }),
    }),
  track: (event, properties = {}) =>
    request("/analytics/track", {
      method: "POST",
      body: JSON.stringify({ event, properties }),
    }),
};
