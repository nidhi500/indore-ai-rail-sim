# Indore Conflict-Resolution DSS — 5 Phase Development Plan

---

## Phase 1 — Data Setup & Validation
**Goal:** Clean and connect the network data so the simulator has a foundation.  

**Tasks:**
- Load CSVs (`stations`, `sections`, `trains`, `timetable`, `platforms`, `loops`).
- Validate invariants:
  - Platform length ≥ train length.
  - Sections connect valid stations.
  - Single/double track flags consistent.
  - Dwell times ≥ 0.
- Build a **graph structure** (`networkx`): stations = nodes, sections = edges with attributes (length_km, max_speed, track_type).
- Export:
  - `canonical_data.json` (unified schema).
  - `data_quality_report.md`.

**Output:** Clean dataset + schematic graph ready for simulation.

---

## Phase 2 — Core Simulator (Time-Space Engine)
**Goal:** Move trains realistically and generate event logs.  

**Tasks:**
- **Time discretization:** 30s–60s tick.
- **Movement model:** average cruise speed = min(train class, section limit).
- **Block occupancy tracking:**
  - Single track = one critical block.
  - Double track = split by direction.
- **Station/platform handling:**
  - Assign trains to platforms.
  - Apply dwell times.
  - Allow loop use for overtakes.
- **Event logger:** log `enter_section`, `exit_section`, `arrive_platform`, `depart_platform`, `hold_start`, `hold_end`.

**Output:** Run-able simulation producing JSON/CSV event logs.

---

## Phase 3 — Conflict Detection
**Goal:** Identify and prioritize conflicts in simulation output.  

**Tasks:**
- Sliding lookahead window (15–30 min).
- Conflict types:
  - Section overlap (same section, overlapping time).
  - Platform overlap.
  - Junction route clash.
- Severity scoring:
  - Priority weight (train class).
  - Estimated downstream delay.
  - Number of trains affected.
- API endpoint: `GET /conflicts` → structured JSON with ranked conflicts.

**Output:** Conflict summary table + JSON payloads.

---

## Phase 4 — Resolution Recommender
**Goal:** Suggest safe, explainable fixes to conflicts.  

**Tasks:**
- Define primitives:
  - Hold (X min at station).
  - Divert to loop.
  - Platform swap.
  - Expedite departure (cut dwell).
- Feasibility checks: platform length, loop availability, interlocking.
- Heuristic rules:
  - Higher priority goes first.
  - Hold lower priority at nearest suitable stop.
  - Minimize passenger impact.
- Impact estimation: simulate next 30 min with candidate → compute Δdelay.
- Explainability: short factual reason  
  *Example:* “Hold Goods at DWX for 6 min so Express clears junction.”

**Output:** JSON with Top-2 recommended actions + impact metrics + explanation.

---

## Phase 5 — UI + API Integration
**Goal:** Judge-usable interface showing trains, conflicts, and fixes.  

**Tasks:**
- **Backend (FastAPI):**
  - `GET /status` → current sim time, active trains.
  - `POST /simulate/step` → advance tick.
  - `GET /conflicts` → list of active conflicts.
  - `POST /actions` → apply recommendation.
  - `GET /export/logs` → full run log.
- **Frontend (Streamlit/Dash/React+Plotly):**
  - Map/network view (schematic Indore region).
  - Time-space diagram (train lines, conflicts marked).
  - Conflict panel (ranked list).
  - Action panel (apply/override recommendation).
  - Metrics HUD (avg delay, total delay saved).
- **Interactivity:**
  - Click conflict → highlight on diagram.
  - Apply recommendation → show before/after overlay.

**Output:** Working demo system (local or hosted) with conflict detection, recommendations, and visualization.

---
