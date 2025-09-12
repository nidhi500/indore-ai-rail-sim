# 🚆 Indore AI Rail Simulation (Prototype)

AI-assisted decision support system for the Indore railway corridor.  
Simulates trains, detects conflicts, optimizes schedules, and shows results on a live dashboard.  
Built for SIH 2025.

---

## 📂 Project Structure

indore-ai-rail-sim/
│
├── backend/ # FastAPI backend (simulation + optimization)
│ ├── api/ # API endpoints
│ ├── sim/ # simulation engine (SimPy / custom)
│ ├── opt/ # optimization models (OR-Tools/PuLP)
│ ├── rules/ # Indian Railways protocol/priority rules
│ ├── data/ # CSVs (stations, sections, trains, timetable, etc.)
│ └── main.py # FastAPI entrypoint
│
├── frontend/ # React + Tailwind dashboard
│ ├── public/
│ ├── src/
│ │ ├── components/ # UI components (KPI tiles, map, alerts)
│ │ ├── views/ # Pages (Dashboard)
│ │ └── App.tsx # Root React component
│ ├── index.html
│ └── package.json
│
├── scripts/ # Helpers (data seeding, generators)
│
├── .gitignore
├── README.md
└── requirements.txt

## ⚙️ Backend Setup (FastAPI + Python)

1. Open terminal in `backend/`
2. Create virtual environment:
   python -m venv venv
   .\venv\Scripts\activate    # PowerShell
Install dependencies:

pip install -r requirements.txt
pip install fastapi uvicorn simpy ortools pandas pytest

Run backend:
uvicorn main:app --reload --port 8000

Test:

Open http://localhost:8000/ping → should return {"msg":"Backend alive"}

🎨 Frontend Setup (React + Vite + TailwindCSS)
Open terminal in frontend/

Install dependencies:

powershell
Copy code
npm install

Run frontend:
npm run dev

Test:

Open http://localhost:5173 → should show “Indore Rail AI Dashboard”

📊 Data
CSV files are inside /backend/data/:

1.stations.csv
2.sections.csv (includes mainline + loop sections)
3.platforms.csv
4.loops.csv
5.trains.csv
6.timetable.csv

These define the Indore corridor network, trains, timetables, and loops.

✅ Verification Checklist
 1.Backend /ping works on port 8000

 2.Frontend dashboard runs on port 5173

 3.Tailwind classes apply (blue heading test works)

 4.CSV data is loadable by backend

👥 Contributors
Team SIH 2025 – Indore Corridor Project

This file is already in Markdown format (`.md`), so just copy it into **`README.md`** and push it to your repo.  

Do you want me to also prepare a **ready-to-use `requirements.txt`** and `package.json` snippet with pinned versions so nobody pulls unstable Tailwind 4.x again?
