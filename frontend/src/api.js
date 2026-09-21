/**
 * ClaimLens Nexus — API Client
 * Centralized API calls to the FastAPI backend.
 */

const API_BASE = '/api';

async function fetchJSON(url, options = {}) {
  const response = await fetch(`${API_BASE}${url}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  });
  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`);
  }
  return response.json();
}

export const api = {
  // Trends (FR-002)
  getOverview: () => fetchJSON('/trends/overview'),
  getMonthlyTrends: (params = {}) => {
    const qs = new URLSearchParams(params).toString();
    return fetchJSON(`/trends/monthly${qs ? '?' + qs : ''}`);
  },
  getTrendsByLOB: () => fetchJSON('/trends/by-lob'),
  getTrendsByState: () => fetchJSON('/trends/by-state'),

  // Anomalies (FR-003)
  getAnomalyQueue: (params = {}) => {
    const qs = new URLSearchParams(params).toString();
    return fetchJSON(`/anomalies/queue${qs ? '?' + qs : ''}`);
  },
  getAnomalyStats: () => fetchJSON('/anomalies/stats'),
  getAnomalyDetail: (claimId) => fetchJSON(`/anomalies/${claimId}`),

  // Ask ClaimLens (FR-004)
  askQuestion: (question) =>
    fetchJSON('/ask', {
      method: 'POST',
      body: JSON.stringify({ question }),
    }),

  // Decisions (FR-006)
  getDecisions: (params = {}) => {
    const qs = new URLSearchParams(params).toString();
    return fetchJSON(`/decisions/${qs ? '?' + qs : ''}`);
  },
  createDecision: (decision) =>
    fetchJSON('/decisions/', {
      method: 'POST',
      body: JSON.stringify(decision),
    }),
  getDecisionStats: () => fetchJSON('/decisions/stats'),

  // Morning Brief (FR-005)
  getMorningBrief: () => fetchJSON('/brief/morning'),

  // External Data (FR-009)
  getIRDAI: () => fetchJSON('/external/irdai'),
  getPMFBY: () => fetchJSON('/external/pmfby'),

  // Health
  getHealth: () => fetchJSON('/health'),
};
