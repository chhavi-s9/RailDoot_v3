import type { Conflict, DashboardSummary, PlanBlock, RequestItem } from "./types";

const api = async <T,>(path: string, options?: RequestInit): Promise<T> => {
  const response = await fetch(`/api${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!response.ok) throw new Error(`${response.status} ${response.statusText}`);
  return response.json();
};

export const getDashboard = () => api<DashboardSummary>("/dashboard/summary");
export const getRequests = () => api<RequestItem[]>("/requests");
export const getConflicts = () => api<Conflict[]>("/conflicts");
export const getPlan = (startDate?: string, endDate?: string) =>
  api<PlanBlock[]>(`/blocks/plan${startDate ? `?start_date=${startDate}&end_date=${endDate ?? startDate}` : ""}`);

export const generatePlan = (payload: {
  start_date: string;
  end_date: string;
  section?: string;
}) => api<{ plan: PlanBlock[]; conflicts: Conflict[]; metrics: Record<string, number> }>("/planning/generate", {
  method: "POST",
  body: JSON.stringify(payload),
});

export const resolveConflict = (id: string) =>
  api<{ recommendation: unknown }>(`/conflicts/${id}/resolve`, { method: "POST" });

export const applyRecommendation = (id: string) =>
  api<{ status: string }>(`/approvals/${id}/apply`, { method: "POST" });
