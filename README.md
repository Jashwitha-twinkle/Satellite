# 🛰️ DEBRIX ORBITAL — Satellite Collision Avoidance System

> Built by Spacekitties✨

A real-time orbital simulation and autonomous collision avoidance system. Given a constellation of satellites and a debris cloud, it continuously predicts conjunction threats, plans fuel-efficient evasion maneuvers, and visualizes everything on a live mission control dashboard.

---

## 📸 Dashboard

> <img width="1897" height="859" alt="image" src="https://github.com/user-attachments/assets/65e52786-5c46-4185-9322-ab25daa0ac49" />
> <img width="1870" height="879" alt="image" src="https://github.com/user-attachments/assets/3c7ac2ee-62ea-43f7-baf7-b77152fae057" />
> <img width="1859" height="846" alt="image" src="https://github.com/user-attachments/assets/0144980e-b068-4e5d-aa07-d34ff634f483" />
> <img width="1897" height="860" alt="image" src="https://github.com/user-attachments/assets/c3a787ad-f00f-466b-88ff-af148ce83e6c" />




| Ground Track | Bullseye Plot | Gantt Timeline |
|---|---|---|
| Real-time Mercator map with terminator line | Polar conjunction view with TCA & risk indexing | Maneuver scheduler with conflict detection |

---

## 🚀 Features

### Visualization Modules (Frontend)
- **Ground Track Map** — Live Mercator projection with historical trails (90 min), dashed predicted trajectories (90 min), day/night terminator overlay, and full debris cloud
- **Conjunction Bullseye Plot** — Polar chart centered on selected satellite. Radial distance = Time to Closest Approach (TCA), angle = approach vector. Debris color-coded Green/Yellow/Red by miss distance
- **Telemetry & Resource Heatmaps** — Circular SVG fuel gauges (m_fuel) per satellite + ΔV cost analysis graph (Fuel Consumed vs Collisions Avoided)
- **Maneuver Timeline (Gantt)** — Chronological Burn Start / Burn End / mandatory 600s thruster cooldown blocks with conflict and blackout zone flagging

### Backend Capabilities
- **Physics Engine** — Keplerian orbital propagation using 6-element state vectors (position + velocity in km/km·s⁻¹)
- **Conjunction Detection** — K-D tree spatial indexing for O(log n) proximity queries across the entire debris field
- **ACM (Autonomous Collision Management)** — Rule-based maneuver planner that schedules minimum-ΔV evasion burns respecting cooldown windows
- **Fuel Modeling** — Tsiolkovsky rocket equation for burn cost estimation; satellites tracked with mass and remaining propellant
- **REST API** — FastAPI with auto-generated Swagger docs at `/docs`

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│              Mission Control UI              │
│     React 18 + D3-geo + Canvas API (Vite)   │
└──────────────────┬──────────────────────────┘
                   │ HTTP polling every 2s
┌──────────────────▼──────────────────────────┐
│            FastAPI Backend (port 8000)       │
│  ┌─────────┐ ┌──────────┐ ┌─────────────┐  │
│  │ Physics │ │Conjunction│ │     ACM     │  │
│  │ Engine  │ │ K-D Tree  │ │  Planner    │  │
│  └─────────┘ └──────────┘ └─────────────┘  │
│           In-memory State Store              │
│         (loaded from objects.json)           │
└─────────────────────────────────────────────┘
```

---

## ⚙️ How the Backend Works

### 1. State Initialization
On startup, `objects.json` is loaded into an in-memory store. Each object (satellite or debris) has a 6-element state vector `[x, y, z, vx, vy, vz]` in km and km/s, plus fuel mass and object type.

### 2. Simulation Step (`POST /api/simulate/step`)
Each step advances the simulation by N seconds (default 60s). The physics engine applies simplified Keplerian propagation — positions are updated using velocity vectors, with gravitational acceleration computed from Earth's GM constant. No atmospheric drag is modeled (LEO approximation).

### 3. Conjunction Detection (`GET /api/visualization/conjunctions`)
A K-D tree is built over all object positions at each step. For every satellite, the tree is queried for all objects within a configurable threshold radius. Relative velocity is used to compute Time to Closest Approach (TCA) and miss distance analytically. Results are sorted by risk level.

### 4. Autonomous Collision Management (ACM)
When miss distance drops below the critical threshold (1 km), ACM schedules an evasion burn. The planner:
- Computes minimum ΔV needed to increase miss distance above safe threshold
- Checks thruster cooldown (600s between burns)
- Deducts fuel using the rocket equation: `Δm = m(1 - e^(-ΔV/Isp·g₀))`
- Flags satellites as `LOW_FUEL` (<20%) or `EOL_PENDING` (<5%)

### 5. Telemetry Ingestion (`POST /api/telemetry`)
External state vectors can be pushed in real time (e.g. from a ground station simulator or TLE propagator). The backend merges incoming data with the current state and re-runs conjunction detection immediately.

---

## ⚙️ How the Frontend Works

### Rendering Pipeline
The Ground Track map uses an HTML5 Canvas with a D3 equirectangular projection. Every frame (via `requestAnimationFrame`):
1. World topology is drawn from TopoJSON (cached after first load)
2. Terminator line is overlaid as a pixel-step shadow based on current UTC sun position
3. Each satellite's historical trail (last 90 min) and predicted path (next 90 min, dashed) are drawn
4. Debris cloud and satellites are drawn with status-coded colors

### Data Flow
The frontend polls `/api/visualization/snapshot` every 2 seconds and simultaneously triggers `/api/simulate/step` every second when simulation is running. All four panels share the same state and re-render reactively.

### Bullseye Plot
Built on Canvas with polar coordinate math. Each conjunction alert maps `tca_seconds → radial distance` and `approach_angle → polar angle`. Miss distance determines the color ring zone (Green > 5km, Yellow < 5km, Red < 1km).

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite, D3-geo, Canvas API, Lucide Icons |
| Backend | Python 3.11, FastAPI, Uvicorn |
| Physics | NumPy, scikit-learn (K-D tree) |
| Containerization | Docker, Docker Compose, Nginx |

---

## ⚡ Quick Start

### Option 1 — Docker Compose (Recommended)

```bash
git clone https://github.com/sragssmonkey/Satellite.git
cd Satellite
docker-compose up --build
```

Then open:
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs (Swagger):** http://localhost:8000/docs

### Option 2 — Run Manually

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
# opens at http://localhost:5173
```

---

## 🔌 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/visualization/snapshot` | Current positions of all satellites + debris |
| `GET` | `/api/visualization/conjunctions` | Active conjunction alerts with TCA + miss distance |
| `GET` | `/api/visualization/maneuvers` | Full maneuver history log |
| `GET` | `/api/visualization/efficiency` | ΔV cost log (fuel consumed vs collisions avoided) |
| `POST` | `/api/simulate/step` | Advance simulation (`{ "step_seconds": 60 }`) |
| `POST` | `/api/telemetry` | Push new state vectors for objects |
| `GET` | `/docs` | Interactive Swagger UI |

---

## 📁 Project Structure

```
Satellite/
├── Dockerfile              # Root multi-stage build (Node → Python + Nginx)
├── docker-compose.yml      # Service orchestration
├── nginx.conf              # Reverse proxy: / → frontend, /api → backend
├── start.sh                # Container startup (nginx + uvicorn)
├── backend/
│   ├── main.py             # FastAPI entry point + startup data loader
│   ├── requirements.txt
│   ├── api/                # Route handlers
│   │   ├── visualization.py  # Snapshot, conjunctions, maneuvers, efficiency
│   │   ├── simulate.py       # Step simulation
│   │   ├── telemetry.py      # Ingest state vectors
│   │   └── maneuver.py       # Trigger and log maneuvers
│   ├── physics/            # Orbital propagation engine
│   ├── conjuction/         # K-D tree conjunction detection
│   ├── acm/                # Autonomous collision management
│   ├── state/              # In-memory object store
│   └── data/               # objects.json — initial constellation
└── frontend/
    ├── src/
    │   ├── App.jsx          # All 4 dashboard modules
    │   └── index.css
    ├── index.html
    ├── package.json
    └── vite.config.js
```

---

## 🎮 How to Use

1. **Start the simulation** — click **START SIMULATION** in the sidebar
2. **Watch the Ground Track** — satellites move in real time with trails, predicted paths, and terminator shadow
3. **Click any satellite** — jumps to **Bullseye Plot** showing all conjunction threats for that satellite
4. **Check Telemetry** — view per-satellite fuel gauges and the ΔV efficiency graph
5. **Open Gantt** — see the full maneuver schedule with cooldown windows and conflict flags

---

## 👥 Team [Spacekitties]

| Name | Role |
|---|---|
| [Jashwitha Bhnadary] | Frontend, Visualization, Docker |
| [Sragvi Chavan] | Backend, Physics Engine, ACM |

---

## 📄 License

MIT
