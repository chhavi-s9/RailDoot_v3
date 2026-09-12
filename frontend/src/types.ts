export type Department = "Engineering" | "S&T" | "TRD";

export interface RequestItem {
  req_uid: string;
  dept: Department | string;
  asset_id: string;
  block_section_id: string;
  section_id: string;
  activity_code: string;
  activity_desc: string;
  dept_priority_code: string;
  dept_priority_rank: number;
  days_overdue: number;
  safety_critical_flag: number;
  requested_duration_min: number;
  min_viable_duration_min: number;
  earliest_start_date: string;
  latest_finish_date: string;
  request_status: string;
  joint_dept_required: string | null;
}

export interface PlanBlock {
  id: string;
  section: string;
  block_section: string;
  department: string;
  activity: string;
  start: string;
  end: string;
  duration: number;
  status: string;
  score?: number;
  resource?: string;
}

export interface Conflict {
  id: string;
  type: string;
  severity: "HIGH" | "MEDIUM" | "LOW";
  task: string;
  section: string;
  detail: string;
  status: "OPEN" | "RESOLVED";
}

export interface DashboardSummary {
  total_requests: number;
  critical_requests: number;
  overdue_requests: number;
  active_conflicts: number;
  planned_blocks: number;
  high_risk_assets: number;
  asset_availability_pct: number;
  block_utilization_pct: number;
}
