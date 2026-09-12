# Automatic Block Planning - Data Dictionary

Generated 2026-09-11 | seed 20260911 | planning horizon 92 days | history 2024-09-01 to 2026-09-10

Six source-system databases plus one integrated database (`abp_integrated.db`, which also holds the reconciliation view `v_unified_block_request`).

## Databases

| File | Represents | Tables | Rows |
|---|---|---|---|
| `coa_asset_register.db` | Asset register / COA asset availability master | 7 | 28,903 |
| `tms_track_mgmt.db` | Track Management System (Engineering) | 1 | 180 |
| `smms_signalling.db` | Signalling Maintenance & Management System (S&T) | 1 | 165 |
| `tdms_traction.db` | Traction Distribution Management System (TRD) | 1 | 140 |
| `coa_control_office.db` | Control Office Application (timetable, corridors, traffic) | 7 | 28,125 |
| `bdms_legacy.db` | BDMS legacy archive, resources, policy, coordination rules | 5 | 10,585 |
| `abp_integrated.db` | All of the above + `v_unified_block_request` | 22 + 1 view | 68,098 |

## coa_asset_register.db

*Asset register / COA asset availability master*

### `division_master`

Administrative division master.  **1 rows, 8 columns.**

| Column | Type | Example |
|---|---|---|
| `division_id` | TEXT | SUR |
| `division_name` | TEXT | Solapur |
| `zone_code` | TEXT | CR |
| `zone_name` | TEXT | Central Railway |
| `hq_station_code` | TEXT | SUR |
| `route_km` | REAL | 1020.5 |
| `electrified_pct` | REAL | 98.4 |
| `dy_cme_office` | TEXT | Solapur |

### `section_master`

Traffic sections; route class and GMT drive block priority.  **6 rows, 16 columns.**

| Column | Type | Example |
|---|---|---|
| `section_id` | TEXT | SEC-DD-KWV |
| `section_name` | TEXT | Daund - Kurduvadi |
| `division_id` | TEXT | SUR |
| `from_station_code` | TEXT | DD |
| `to_station_code` | TEXT | KWV |
| `route_class` | TEXT | A |
| `line_config` | TEXT | DOUBLE |
| `is_electrified` | INTEGER | 1 |
| `traction_type` | TEXT | 25 kV AC |
| `length_km` | REAL | 108.0 |
| `sanctioned_speed_kmph` | INTEGER | 130 |
| `traffic_density_gmt` | REAL | 42.5 |
| `daily_passenger_trains` | INTEGER | 34 |
| `daily_goods_trains` | INTEGER | 28 |
| `block_section_count` | INTEGER | 14 |
| `is_trunk_route` | INTEGER | 1 |

### `station_master`

Stations with crossing capability (limits where blocks can terminate).  **36 rows, 11 columns.**

| Column | Type | Example |
|---|---|---|
| `station_code` | TEXT | DD |
| `station_name` | TEXT | Daund Jn |
| `section_id` | TEXT | SEC-DD-KWV |
| `seq_in_section` | INTEGER | 1 |
| `station_category` | TEXT | NSG-2 |
| `is_junction` | INTEGER | 1 |
| `interlocking_type` | TEXT | PI |
| `num_loop_lines` | INTEGER | 4 |
| `has_crossing_facility` | INTEGER | 1 |
| `has_goods_shed` | INTEGER | 1 |
| `km_from_division_hq` | REAL | 0.0 |

### `block_section_master`

Block section = atomic unit a block/disconnection is granted on.  **60 rows, 18 columns.**

| Column | Type | Example |
|---|---|---|
| `block_section_id` | TEXT | BS-DD-KWV-01-UP |
| `section_id` | TEXT | SEC-DD-KWV |
| `from_station_code` | TEXT | DD |
| `to_station_code` | TEXT | KDG |
| `line_designation` | TEXT | UP |
| `length_km` | REAL | 14.34 |
| `ruling_gradient` | TEXT | 1 in 200 |
| `max_curvature_deg` | REAL | 0.25 |
| `has_major_bridge` | INTEGER | 1 |
| `has_tunnel` | INTEGER | 0 |
| `num_level_crossings` | INTEGER | 4 |
| `num_turnouts` | INTEGER | 3 |
| `is_ghat_section` | INTEGER | 0 |
| `permitted_speed_kmph` | INTEGER | 130 |
| `single_line_working_possible` | INTEGER | 1 |
| `road_access_rating` | TEXT | MODERATE |
| `ohe_elementary_section_id` | TEXT | ES-DD-KWV-01 |
| `signalling_type` | TEXT | Absolute Block - MACLS |

### `asset_master`

Fixed infrastructure asset register across all three departments.  **900 rows, 19 columns.**

| Column | Type | Example |
|---|---|---|
| `asset_id` | TEXT | AST-ENGG-RAIL-0001 |
| `asset_type` | TEXT | RAIL_PANEL |
| `asset_subtype` | TEXT | 60 kg 90 UTS LWR |
| `owning_dept` | TEXT | ENGG |
| `source_system` | TEXT | TMS |
| `block_section_id` | TEXT | BS-DD-KWV-05-DN |
| `section_id` | TEXT | SEC-DD-KWV |
| `km_location` | REAL | 5.41 |
| `nearest_station_code` | TEXT | BLNI |
| `make_manufacturer` | TEXT | SAIL Bhilai |
| `commissioned_date` | TEXT | 1998-01-30 |
| `design_life_years` | INTEGER | 25 |
| `last_overhaul_date` | TEXT | 2019-06-04 |
| `criticality_class` | TEXT | A |
| `criticality_score` | INTEGER | 99 |
| `redundancy_available` | INTEGER | 1 |
| `failure_consequence` | TEXT | LINE_BLOCKAGE_OR_SAFETY |
| `maintenance_schedule_code` | TEXT | USFD-SCH-1 |
| `schedule_periodicity_days` | INTEGER | 180 |

### `asset_availability_status`

CURRENT operational status of each asset. Decoupled from requests - this is COA/asset-register truth.  **900 rows, 22 columns.**

> Asset-register truth, independent of whether any department has raised a request. Use health_index, days_overdue, predicted_failure_prob_30d and availability_pct_30d as the 'cost of NOT doing the work' side of the objective function.

| Column | Type | Example |
|---|---|---|
| `asset_id` | TEXT | AST-ENGG-RAIL-0001 |
| `as_of_date` | TEXT | 2026-09-11 |
| `operational_status` | TEXT | NORMAL |
| `health_index` | REAL | 44.7 |
| `residual_life_pct` | REAL | 0 |
| `condition_grade` | TEXT | POOR |
| `restriction_in_force` | TEXT | PSR |
| `restriction_speed_kmph` | INTEGER | 45 |
| `restriction_imposed_date` | TEXT | 2026-07-27 |
| `is_isolated` | INTEGER | 0 |
| `failures_last_90d` | INTEGER | 4 |
| `mtbf_days` | REAL | 22.5 |
| `mttr_minutes` | REAL | 230.4 |
| `availability_pct_30d` | REAL | 98.8 |
| `availability_pct_365d` | REAL | 98.88 |
| `downtime_minutes_30d` | INTEGER | 518 |
| `last_inspection_date` | TEXT | 2025-11-05 |
| `next_schedule_due_date` | TEXT | 2026-05-04 |
| `days_overdue` | INTEGER | 130 |
| `open_defect_count` | INTEGER | 1 |
| `monitoring_source` | TEXT | RECORDING_CAR |
| `predicted_failure_prob_30d` | REAL | 0.623 |

### `asset_availability_history`

Daily availability history (trailing 30 days) - trend features for the ML model.  **27,000 rows, 9 columns.**

| Column | Type | Example |
|---|---|---|
| `record_id` | TEXT | AAH-AST-ENGG-RAIL-0001-0812 |
| `asset_id` | TEXT | AST-ENGG-RAIL-0001 |
| `record_date` | TEXT | 2026-08-12 |
| `operational_status` | TEXT | NORMAL |
| `health_index` | REAL | 48.9 |
| `restriction_speed_kmph` | INTEGER |  |
| `downtime_minutes` | INTEGER | 0 |
| `availability_pct` | REAL | 100.0 |
| `failure_event` | INTEGER | 0 |

## tms_track_mgmt.db

*Track Management System (Engineering)*

### `tms_maintenance_request`

Engineering / P.Way requests from Track Management System. Vocabulary: USFD classes, TGI, GMT, track machines.  **180 rows, 62 columns.**

> Engineering vocabulary: USFD defect classes (IMR/REM/OBS/DFWR), TGI, CTR rating, GMT, track machines (BCM/CSM/UTV/T-28/RGM), gang strength, caution orders. Duration is a single `requested_duration_min`. Priority is P1-P4.

| Column | Type | Example |
|---|---|---|
| `tms_req_id` | TEXT | TMS/SUR/2026/1001 |
| `tms_work_order_no` | TEXT | WO-PW-51376 |
| `raised_on_date` | TEXT | 2026-07-28 |
| `raised_by_desig` | TEXT | AEN |
| `pway_section_incharge` | TEXT | SSE/PW/LUR |
| `asset_id` | TEXT | AST-ENGG-RAIL-0036 |
| `block_section_id` | TEXT | BS-KWV-SUR-04-DN |
| `section_id` | TEXT | SEC-KWV-SUR |
| `km_from` | REAL | 4.87 |
| `km_to` | REAL | 6.13 |
| `line_designation` | TEXT | DN |
| `pway_activity_code` | TEXT | RR-TRR |
| `pway_activity_desc` | TEXT | Through rail renewal |
| `work_nature` | TEXT | RENEWAL |
| `defect_source` | TEXT | TMS_AUTO_FLAG |
| `usfd_defect_class` | TEXT | NIL |
| `usfd_defect_code` | TEXT | IMR-135 |
| `rail_flaw_location` | TEXT | WELD_COLLAR |
| `tgi_value` | REAL | 50.0 |
| `ctr_rating` | TEXT | C |
| `unevenness_mm` | REAL | 7.7 |
| `twist_mm` | REAL | 7.4 |
| `gauge_variation_mm` | REAL | -0.6 |
| `alignment_defect_mm` | REAL | 6.9 |
| `rail_wear_mm` | REAL | 10.4 |
| `weld_failures_last_year` | INTEGER | 0 |
| `cumulative_gmt` | REAL | 972.0 |
| `gmt_since_last_renewal` | REAL | 269.3 |
| `sr_in_force_kmph` | INTEGER | 75 |
| `tsr_or_psr` | TEXT | TSR |
| `schedule_due_date` | TEXT | 2026-08-05 |
| `days_overdue` | INTEGER | 37 |
| `statutory_deadline_date` | TEXT | 2026-09-13 |
| `dept_priority_code` | TEXT | P3 |
| `safety_critical_flag` | INTEGER | 0 |
| `accident_prone_location` | INTEGER | 0 |
| `requested_block_type` | TEXT | TRAFFIC_BLOCK |
| `requested_duration_min` | INTEGER | 317 |
| `min_viable_duration_min` | INTEGER | 138 |
| `is_splittable` | INTEGER | 1 |
| `max_splits` | INTEGER | 4 |
| `preferred_window_start` | TEXT | 02:00 |
| `preferred_window_end` | TEXT | 07:17 |
| `earliest_start_date` | TEXT | 2026-09-15 |
| `latest_finish_date` | TEXT | 2026-10-28 |
| `track_machine_required` | TEXT | UTV |
| `machine_resource_id` | TEXT | RES-ENGG-UTV-02 |
| `machine_available_from` | TEXT | 2026-09-25 |
| `gang_strength_required` | INTEGER | 17 |
| `gang_resource_id` | TEXT | RES-ENGG-PWAY_G-05 |
| `material_readiness_pct` | REAL | 64.4 |
| `material_at_site` | INTEGER | 0 |
| `caution_order_required` | INTEGER | 1 |
| `post_work_speed_restriction_kmph` | INTEGER | 45 |
| `post_work_sr_duration_hrs` | INTEGER | 12 |
| `joint_dept_required` | TEXT | SNT,TRD |
| `linked_smms_req_id` | TEXT | SMMS/SUR/2026/2101 |
| `linked_tdms_req_id` | TEXT | TDMS/SUR/2026/3007 |
| `expected_asset_life_gain_years` | REAL | 0.6 |
| `deferral_risk_score` | REAL | 0.212 |
| `request_status` | TEXT | SUBMITTED_TO_BDMS |
| `remarks` | TEXT | Combined with adjacent km work |

## smms_signalling.db

*Signalling Maintenance & Management System (S&T)*

### `smms_maintenance_request`

S&T requests from Signalling M&M System. Vocabulary: disconnections, SEM schedules, interlocking, CRS sanction.  **165 rows, 60 columns.**

> S&T vocabulary: DISCONNECTIONS (not 'blocks'), disconnection memo numbers, SEM schedule codes, megger/relay pickup/drop-shunt readings, interlocking and route counts, CRS sanction, NI working. Duration arrives SPLIT as disconnection_duration_min + reconnection_testing_min. Priority is A1/A2/B1/B2.

| Column | Type | Example |
|---|---|---|
| `smms_req_id` | TEXT | SMMS/SUR/2026/2001 |
| `disconnection_memo_no` | TEXT | DM/MO/278/2026 |
| `raised_on_date` | TEXT | 2026-09-03 |
| `raised_by_desig` | TEXT | Sr.DSTE |
| `sse_signal_incharge` | TEXT | SSE/Tele/SUR |
| `asset_id` | TEXT | AST-SNT-SIG_-0014 |
| `block_section_id` | TEXT | BS-KWV-SUR-05-UP |
| `section_id` | TEXT | SEC-KWV-SUR |
| `station_code` | TEXT | TLT |
| `work_category` | TEXT | CABLE_WORK |
| `sig_activity_code` | TEXT | CBL-LAY |
| `sig_activity_desc` | TEXT | Signalling cable laying / megger recti |
| `sem_schedule_code` | TEXT | SEM-HY |
| `schedule_periodicity` | TEXT | HALF_YEARLY |
| `gear_type` | TEXT | SIG_CABLE |
| `gear_id` | TEXT | AST-SNT-SIG_-0014 |
| `failure_mode` | TEXT | EVALUATOR_CARD_FAULT |
| `failure_symptom` | TEXT | LOAD_DEPENDENT |
| `megger_value_mohm` | REAL | 7.36 |
| `relay_pickup_voltage` | REAL | 8.91 |
| `track_circuit_drop_shunt_ohm` | REAL | 0.323 |
| `point_operation_time_sec` | REAL | 8.5 |
| `axle_counter_reset_count` | INTEGER | 5 |
| `failures_last_30d` | INTEGER | 0 |
| `failures_last_90d` | INTEGER | 5 |
| `cumulative_failure_minutes` | INTEGER | 635 |
| `disconnection_type` | TEXT | PARTIAL |
| `interlocking_affected` | INTEGER | 0 |
| `routes_affected_count` | INTEGER | 0 |
| `points_affected_count` | INTEGER | 2 |
| `signals_affected_count` | INTEGER | 3 |
| `affects_level_crossing` | INTEGER | 0 |
| `affects_block_working` | INTEGER | 0 |
| `alternate_working_mode` | TEXT | MANUAL_POINT_CLAMPING |
| `requires_crs_sanction` | INTEGER | 0 |
| `requires_ni_working` | INTEGER | 0 |
| `tester_grade_required` | TEXT | JE_SIGNAL |
| `tester_resource_id` | TEXT | RES-SNT-SSE_SI-02 |
| `safety_category` | TEXT | DETENTION_RISK |
| `spad_risk_flag` | INTEGER | 0 |
| `schedule_due_date` | TEXT | 2026-10-30 |
| `overdue_days` | INTEGER | 0 |
| `dept_priority` | TEXT | B2 |
| `disconnection_duration_min` | INTEGER | 236 |
| `reconnection_testing_min` | INTEGER | 62 |
| `total_requested_min` | INTEGER | 298 |
| `min_viable_duration_min` | INTEGER | 223 |
| `is_splittable` | INTEGER | 1 |
| `preferred_window_start` | TEXT | 14:00 |
| `preferred_window_end` | TEXT | 18:58 |
| `earliest_start_date` | TEXT | 2026-09-15 |
| `latest_finish_date` | TEXT | 2026-10-30 |
| `spares_available` | INTEGER | 1 |
| `spare_part_eta_date` | TEXT | 2026-09-23 |
| `joint_dept_required` | TEXT | ENGG |
| `linked_tms_req_id` | TEXT | TMS/SUR/2026/1152 |
| `linked_tdms_req_id` | TEXT |  |
| `detention_risk_per_hour_min` | REAL | 18.1 |
| `request_status` | TEXT | PENDING_SUBMISSION |
| `remarks` | TEXT | To be clubbed with P.Way block |

## tdms_traction.db

*Traction Distribution Management System (TRD)*

### `tdms_maintenance_request`

TRD/OHE requests from Traction Distribution M System. Vocabulary: power blocks, PTW, elementary sections, wear.  **140 rows, 63 columns.**

> TRD vocabulary: POWER BLOCKS and permits-to-work, elementary sections, TSS/SP/SSP, contact wire wear in mm and residual area %, stagger, tension lengths, dead-and-earthed, tower wagons. Duration arrives as THREE parts: requested + setup_time_min + restoration_time_min. Priority is A/B/C.

| Column | Type | Example |
|---|---|---|
| `tdms_req_id` | TEXT | TDMS/SUR/2026/3001 |
| `ptw_reference_no` | TEXT | PTW/ES-SUR-GR-03/49/26 |
| `raised_on_date` | TEXT | 2026-09-03 |
| `raised_by_desig` | TEXT | JE/TRD |
| `sse_trd_incharge` | TEXT | SSE/TRD/DD |
| `asset_id` | TEXT | AST-TRD-NEUT-0013 |
| `block_section_id` | TEXT | BS-SUR-GR-06-UP |
| `section_id` | TEXT | SEC-SUR-GR |
| `elementary_section_id` | TEXT | ES-SUR-GR-03 |
| `tss_id` | TEXT | TSS-DD |
| `feeding_post` | TEXT | FP-DN |
| `sp_ssp_id` | TEXT | SP-GDGN |
| `ohe_activity_code` | TEXT | NS-ATTN |
| `ohe_activity_desc` | TEXT | Neutral section attention (PTFE) |
| `ohe_structure_id` | TEXT | OHE/761/22 |
| `tension_length_no` | TEXT | TL-38 |
| `km_from` | REAL | 15.19 |
| `km_to` | REAL | 16.02 |
| `contact_wire_wear_mm` | REAL | 1.92 |
| `residual_cw_area_pct` | REAL | 58.0 |
| `contact_wire_height_mm` | INTEGER | 4800 |
| `stagger_mm` | INTEGER | -100 |
| `deviation_from_norm_mm` | INTEGER | 130 |
| `insulator_leakage_current_ma` | REAL | 3.82 |
| `dropper_slack_count` | INTEGER | 11 |
| `breakdown_count_last_year` | INTEGER | 0 |
| `pantograph_entanglement_history` | INTEGER | 0 |
| `inspection_source` | TEXT | TOWER_WAGON_PATROL |
| `last_ohe_recording_date` | TEXT | 2025-11-20 |
| `defect_grade` | TEXT | G2_EARLY |
| `block_type_required` | TEXT | POWER_BLOCK |
| `power_block_type` | TEXT | DEAD_AND_EARTHED |
| `requires_dead_and_earthed` | INTEGER | 1 |
| `earthing_points_count` | INTEGER | 4 |
| `traction_lines_affected` | TEXT | DN_ONLY |
| `alt_feed_available` | INTEGER | 1 |
| `can_work_under_isolation` | INTEGER | 1 |
| `rolling_block_possible` | INTEGER | 0 |
| `tower_wagon_required` | INTEGER | 1 |
| `tower_wagon_resource_id` | TEXT | RES-TRD-8W_DET-01 |
| `road_vehicle_access` | TEXT | MODERATE |
| `ladder_trolley_required` | INTEGER | 1 |
| `crew_strength_required` | INTEGER | 8 |
| `crew_resource_id` | TEXT | RES-TRD-TRD_MA-06 |
| `schedule_due_date` | TEXT | 2026-10-09 |
| `overdue_days` | INTEGER | 0 |
| `priority_code` | TEXT | C |
| `safety_critical_flag` | INTEGER | 1 |
| `requested_duration_min` | INTEGER | 162 |
| `min_power_block_min` | INTEGER | 90 |
| `setup_time_min` | INTEGER | 19 |
| `restoration_time_min` | INTEGER | 28 |
| `is_splittable` | INTEGER | 1 |
| `preferred_window_start` | TEXT | 01:00 |
| `preferred_window_end` | TEXT | 04:29 |
| `earliest_start_date` | TEXT | 2026-09-16 |
| `latest_finish_date` | TEXT | 2026-10-14 |
| `material_readiness_pct` | REAL | 91.6 |
| `joint_dept_required` | TEXT | ENGG |
| `linked_tms_req_id` | TEXT | TMS/SUR/2026/1154 |
| `linked_smms_req_id` | TEXT |  |
| `request_status` | TEXT | PENDING_SUBMISSION |
| `remarks` | TEXT | Repeated pantograph damage location |

## coa_control_office.db

*Control Office Application (timetable, corridors, traffic)*

### `passenger_timetable`

Working timetable - FIXED paths. Not reschedulable; drives hard blackout windows.  **678 rows, 27 columns.**

> FIXED. is_reschedulable = 0 for priority_class 1-2 and max_permissible_detention_min is 0-15. Treat occupied minutes as hard blackout for the block section.

| Column | Type | Example |
|---|---|---|
| `tt_row_id` | TEXT | TT-21079-BS-DD-KWV-07-DN |
| `train_no` | TEXT | 21079 |
| `train_name` | TEXT | Vijayawada Mail |
| `train_type` | TEXT | MAIL_EXPRESS |
| `priority_class` | INTEGER | 2 |
| `section_id` | TEXT | SEC-DD-KWV |
| `block_section_id` | TEXT | BS-DD-KWV-07-DN |
| `direction` | TEXT | DN |
| `seq_no` | INTEGER | 1 |
| `entry_time` | TEXT | 16:47 |
| `exit_time` | TEXT | 17:01 |
| `occupancy_min` | INTEGER | 14 |
| `days_of_run` | TEXT | MTWTFSS |
| `runs_mon` | INTEGER | 1 |
| `runs_tue` | INTEGER | 1 |
| `runs_wed` | INTEGER | 1 |
| `runs_thu` | INTEGER | 1 |
| `runs_fri` | INTEGER | 1 |
| `runs_sat` | INTEGER | 1 |
| `runs_sun` | INTEGER | 1 |
| `is_reschedulable` | INTEGER | 0 |
| `max_permissible_detention_min` | INTEGER | 15 |
| `punctuality_pct_l30d` | REAL | 81.4 |
| `avg_delay_min` | REAL | 16.7 |
| `halt_or_pass` | TEXT | HALT |
| `coaching_link_critical` | INTEGER | 0 |
| `diversion_route_available` | INTEGER | 1 |

### `goods_train_forecast`

Control Office goods forecast - RESCHEDULABLE paths with regulation cost. Optimizer routes around these first.  **5,159 rows, 27 columns.**

> RESCHEDULABLE. Every row has is_reschedulable = 1, max_regulation_hours and regulation_cost_per_hour. These are the paths the optimizer should regulate around a block, priced by freight revenue rather than forbidden outright.

| Column | Type | Example |
|---|---|---|
| `forecast_id` | TEXT | GF-20260911-DD-KWV-01 |
| `forecast_date` | TEXT | 2026-09-11 |
| `generated_on_date` | TEXT | 2026-09-11 |
| `path_id` | TEXT | PATH-DD-KWV-UP-21 |
| `rake_id` | TEXT | RK-84014 |
| `section_id` | TEXT | SEC-DD-KWV |
| `block_section_id` | TEXT | BS-DD-KWV-07-UP |
| `direction` | TEXT | UP |
| `commodity` | TEXT | FERTILIZER |
| `load_status` | TEXT | LOADED |
| `rake_type` | TEXT | BCN |
| `tonnage_gross` | REAL | 2984.0 |
| `origin_station` | TEXT | BELLARY |
| `destination_station` | TEXT | MUMBAI |
| `expected_entry_time` | TEXT | 21:20 |
| `expected_exit_time` | TEXT | 21:53 |
| `occupancy_min` | INTEGER | 33 |
| `path_priority` | TEXT | LOW |
| `priority_class` | INTEGER | 3 |
| `is_reschedulable` | INTEGER | 1 |
| `max_regulation_hours` | REAL | 5.1 |
| `regulation_cost_per_hour` | REAL | 1389.1 |
| `freight_revenue_estimate` | REAL | 41000.0 |
| `is_premium_committed` | INTEGER | 0 |
| `alternate_paths_available` | INTEGER | 2 |
| `forecast_confidence_pct` | REAL | 90.2 |
| `crew_link_constraint` | INTEGER | 0 |

### `corridor_block_master`

Pre-notified maintenance corridors per section (the supply side of block capacity).  **40 rows, 16 columns.**

| Column | Type | Example |
|---|---|---|
| `corridor_id` | TEXT | COR-DD-KWV-001 |
| `section_id` | TEXT | SEC-DD-KWV |
| `corridor_name` | TEXT | Night Engineering Corridor (UP) |
| `corridor_type` | TEXT | PRE_NOTIFIED_CORRIDOR |
| `block_kind` | TEXT | TRAFFIC_BLOCK |
| `nominal_start_time` | TEXT | 01:30 |
| `nominal_end_time` | TEXT | 05:00 |
| `nominal_duration_min` | INTEGER | 210 |
| `days_applicable` | TEXT | DAILY |
| `is_mega_block` | INTEGER | 0 |
| `line_designation` | TEXT | UP |
| `max_parallel_departments` | INTEGER | 2 |
| `max_parallel_activities` | INTEGER | 4 |
| `sanctioned_by` | TEXT | Sr.DOM/SUR |
| `notified_in_wtt` | INTEGER | 1 |
| `min_notice_days` | INTEGER | 3 |

### `block_availability_calendar`

Date-expanded corridor instances per block section - the CP-SAT capacity windows.  **17,340 rows, 22 columns.**

> The supply side. One row per (corridor, block section, date). net_available_min and remaining_capacity_dept_slots are the CP-SAT capacity; status = CANCELLED rows must be excluded.

| Column | Type | Example |
|---|---|---|
| `availability_id` | TEXT | AVL-000001 |
| `corridor_id` | TEXT | COR-DD-KWV-001 |
| `block_section_id` | TEXT | BS-DD-KWV-01-UP |
| `section_id` | TEXT | SEC-DD-KWV |
| `calendar_date` | TEXT | 2026-09-11 |
| `day_of_week` | TEXT | Fri |
| `available_from` | TEXT | 01:30 |
| `available_to` | TEXT | 05:00 |
| `gross_window_min` | INTEGER | 210 |
| `net_available_min` | INTEGER | 198 |
| `setup_deduction_min` | INTEGER | 12 |
| `status` | TEXT | OPEN |
| `unavailable_reason` | TEXT | PRIOR_SANCTIONED_WORK |
| `passenger_trains_in_window` | INTEGER | 0 |
| `goods_trains_in_window` | INTEGER | 0 |
| `trains_to_be_regulated` | INTEGER | 0 |
| `estimated_detention_min` | INTEGER | 0 |
| `single_line_working_required` | INTEGER | 1 |
| `monsoon_flag` | INTEGER | 1 |
| `event_embargo_flag` | INTEGER | 0 |
| `weather_risk_score` | REAL | 0.235 |
| `remaining_capacity_dept_slots` | INTEGER | 2 |

### `section_traffic_load_profile`

Typical hourly traffic load by day-type - lets the optimizer pick genuinely low-traffic hours.  **4,320 rows, 11 columns.**

| Column | Type | Example |
|---|---|---|
| `profile_id` | TEXT | TLP-BS-DD-KWV-01-UP-WE-00 |
| `block_section_id` | TEXT | BS-DD-KWV-01-UP |
| `section_id` | TEXT | SEC-DD-KWV |
| `day_type` | TEXT | WEEKDAY |
| `hour_of_day` | INTEGER | 0 |
| `passenger_trains` | INTEGER | 0 |
| `goods_trains` | INTEGER | 0 |
| `total_occupancy_min` | INTEGER | 1 |
| `line_capacity_utilisation_pct` | REAL | 1.7 |
| `is_lean_period` | INTEGER | 1 |
| `cumulative_detention_risk_min` | REAL | 0.0 |

### `weather_forecast`

Weather by section-date; gates monsoon-sensitive P.Way and OHE work.  **552 rows, 13 columns.**

| Column | Type | Example |
|---|---|---|
| `weather_id` | TEXT | WX-DD-KWV-20260911 |
| `section_id` | TEXT | SEC-DD-KWV |
| `forecast_date` | TEXT | 2026-09-11 |
| `rainfall_mm` | REAL | 19.0 |
| `max_temp_c` | REAL | 34.4 |
| `min_temp_c` | REAL | 20.8 |
| `rail_temp_max_c` | REAL | 44.8 |
| `wind_speed_kmph` | REAL | 16.5 |
| `visibility_m` | INTEGER | 3000 |
| `monsoon_flag` | INTEGER | 1 |
| `lwr_destressing_permissible` | INTEGER | 0 |
| `ohe_work_permissible` | INTEGER | 1 |
| `weather_risk_score` | REAL | 0.235 |

### `special_events_calendar`

Festival rush / VIP movement / embargo dates that suppress block grants.  **36 rows, 10 columns.**

| Column | Type | Example |
|---|---|---|
| `event_id` | TEXT | EVT-0001 |
| `event_date` | TEXT | 2026-10-17 |
| `event_name` | TEXT | Dussehra |
| `event_type` | TEXT | FESTIVAL_RUSH |
| `scope` | TEXT | DIVISION |
| `section_id` | TEXT | SEC-SUR-GR |
| `traffic_multiplier` | REAL | 1.12 |
| `block_embargo_flag` | INTEGER | 0 |
| `max_block_duration_min` | INTEGER | 150 |
| `issued_by` | TEXT | Sr.DOM/SUR |

## bdms_legacy.db

*BDMS legacy archive, resources, policy, coordination rules*

### `resource_master`

Machines, gangs, tower wagons, testers - shared scarce resources across depts.  **65 rows, 15 columns.**

| Column | Type | Example |
|---|---|---|
| `resource_id` | TEXT | RES-ENGG-BCM-01 |
| `resource_name` | TEXT | BCM #1 (ENGG) |
| `resource_type` | TEXT | TRACK_MACHINE |
| `resource_class` | TEXT | BCM |
| `owning_dept` | TEXT | ENGG |
| `home_depot_station` | TEXT | LUR |
| `division_id` | TEXT | SUR |
| `capacity_units` | INTEGER | 1 |
| `output_rate_per_hour` | REAL | 150.0 |
| `max_working_hours_per_day` | REAL | 7.8 |
| `mobilisation_lead_time_hrs` | REAL | 24.0 |
| `requires_own_block` | INTEGER | 1 |
| `is_shared_across_sections` | INTEGER | 1 |
| `hire_cost_per_hour` | REAL | 18500.0 |
| `current_status` | TEXT | DEPLOYED |

### `resource_availability`

Daily resource availability - CP-SAT cumulative resource constraint input.  **5,980 rows, 10 columns.**

| Column | Type | Example |
|---|---|---|
| `avail_id` | TEXT | RAV-RES-ENGG-BCM-01-0911 |
| `resource_id` | TEXT | RES-ENGG-BCM-01 |
| `calendar_date` | TEXT | 2026-09-11 |
| `available_from` | TEXT | 08:00 |
| `available_to` | TEXT | 15:48 |
| `available_hours` | REAL | 7.8 |
| `allocated_hours` | REAL | 0.8 |
| `allocated_to_req_id` | TEXT |  |
| `stabled_at_station` | TEXT | LUR |
| `status` | TEXT | AVAILABLE |

### `dept_activity_compatibility`

Cross-department rules: which activities MUST be jointly blocked, can run parallel, or must be sequenced.  **18 rows, 11 columns.**

> The coordination brain expressed as data: MANDATORY_JOINT, COMPATIBLE_PARALLEL, COMPATIBLE_SEQUENCED and MUTUALLY_EXCLUSIVE pairs with min_gap_minutes and shared_block_saving_min. Drives clubbing decisions and no-overlap constraints.

| Column | Type | Example |
|---|---|---|
| `rule_id` | TEXT | CMP-001 |
| `dept_a` | TEXT | ENGG |
| `activity_code_a` | TEXT | PC-REN |
| `dept_b` | TEXT | SNT |
| `activity_code_b` | TEXT | PT-DET |
| `compatibility` | TEXT | MANDATORY_JOINT |
| `min_gap_minutes` | INTEGER | 0 |
| `sequence_order` | TEXT | B_AFTER_A |
| `shared_block_saving_min` | INTEGER | 150 |
| `rationale` | TEXT | Point & crossing renewal invalidates p |
| `authority_reference` | TEXT | IRPWM Para 237 |

### `policy_constraint_master`

Hard/soft rules the optimizer must respect, expressed as data not code.  **22 rows, 13 columns.**

> Rules as rows, not as code. is_hard_constraint = 1 -> CP-SAT constraint; 0 -> objective term weighted by penalty_weight.

| Column | Type | Example |
|---|---|---|
| `constraint_id` | TEXT | POL-001 |
| `constraint_name` | TEXT | Max concurrent blocks per section |
| `constraint_type` | TEXT | CAPACITY |
| `applies_to` | TEXT | SECTION |
| `scope_value` | TEXT | ALL |
| `parameter_name` | TEXT | max_concurrent_blocks |
| `parameter_value` | TEXT | 2 |
| `unit` | TEXT | count |
| `is_hard_constraint` | INTEGER | 1 |
| `penalty_weight` | REAL | 0.0 |
| `authority_reference` | TEXT | Sr.DOM circular 14/2026 |
| `effective_from` | TEXT | 2026-04-01 |
| `remarks` | TEXT |  |

### `historical_block_grant`

Closed BDMS records, denormalised with engineered features + 6 labels. Primary ML training table.  **4,500 rows, 55 columns.**

> Primary ML table, 24 months, denormalised on purpose. Features are everything known BEFORE the decision; labels are granted_flag (classification) plus granted_duration_min, actual_duration_min, block_utilisation_pct, overrun_min, work_completion_status and total_detention_min (regression). Do not feed the label columns back in as features.

| Column | Type | Example |
|---|---|---|
| `grant_id` | TEXT | BDMS/GRT/2025/000001 |
| `source_system` | TEXT | TMS |
| `source_req_id` | TEXT | TMS/SUR/2025/4876 |
| `dept` | TEXT | ENGG |
| `activity_code` | TEXT | SEJ-OVH |
| `activity_group` | TEXT | SCHEDULED |
| `asset_id` | TEXT | AST-ENGG-WELD-0001 |
| `block_section_id` | TEXT | BS-DD-KWV-07-DN |
| `section_id` | TEXT | SEC-DD-KWV |
| `route_class` | TEXT | A |
| `line_config` | TEXT | DOUBLE |
| `traffic_density_gmt` | REAL | 42.5 |
| `request_date` | TEXT | 2025-01-06 |
| `requested_block_date` | TEXT | 2025-01-21 |
| `notice_days` | INTEGER | 15 |
| `requested_duration_min` | INTEGER | 132 |
| `min_viable_duration_min` | INTEGER | 84 |
| `is_splittable` | INTEGER | 0 |
| `block_kind` | TEXT | TRAFFIC_BLOCK |
| `dept_priority_code` | TEXT | P4 |
| `dept_priority_rank` | INTEGER | 4 |
| `asset_criticality_score` | INTEGER | 78 |
| `asset_health_index` | REAL | 37.5 |
| `days_overdue` | INTEGER | 2 |
| `safety_critical_flag` | INTEGER | 0 |
| `sr_in_force_kmph` | INTEGER | 45 |
| `failures_last_90d` | INTEGER | 3 |
| `material_readiness_pct` | REAL | 77.6 |
| `resource_required` | TEXT | NONE |
| `resource_confirmed_flag` | INTEGER | 1 |
| `joint_dept_flag` | INTEGER | 1 |
| `window_start_hour` | INTEGER | 11 |
| `is_night_block` | INTEGER | 0 |
| `day_of_week` | TEXT | Tue |
| `month_num` | INTEGER | 1 |
| `monsoon_flag` | INTEGER | 0 |
| `event_embargo_flag` | INTEGER | 0 |
| `passenger_trains_in_window` | INTEGER | 0 |
| `goods_trains_in_window` | INTEGER | 0 |
| `section_utilisation_pct` | REAL | 3.1 |
| `competing_requests_same_window` | INTEGER | 4 |
| `corridor_notified_flag` | INTEGER | 0 |
| `approval_authority` | TEXT | Dy.CoM/HQ |
| `granted_flag` | INTEGER | 1 |
| `rejection_or_cancellation_reason` | TEXT | SANCTION_NOT_RECEIVED |
| `granted_duration_min` | INTEGER | 131 |
| `actual_start_delay_min` | INTEGER | 21 |
| `actual_duration_min` | INTEGER | 106 |
| `block_utilisation_pct` | REAL | 80.9 |
| `overrun_min` | INTEGER | 0 |
| `work_completion_status` | TEXT | FULLY_COMPLETED |
| `trains_detained` | INTEGER | 0 |
| `total_detention_min` | INTEGER | 0 |
| `asset_downtime_avoided_min` | INTEGER | 332 |
| `post_block_defect_cleared` | INTEGER | 1 |
