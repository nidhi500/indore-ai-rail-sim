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

yaml
Copy code

---

## ⚙️ Backend Setup (FastAPI + Python)

1. Open terminal in `backend/`
2. Create virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate    # PowerShell
Install dependencies:

powershell
Copy code
pip install -r requirements.txt
If requirements.txt is missing, install manually:

powershell
Copy code
pip install fastapi uvicorn simpy ortools pandas pytest
Run backend:

powershell
Copy code
uvicorn main:app --reload --port 8000
Test:

Open http://localhost:8000/ping → should return {"msg":"Backend alive"}

🎨 Frontend Setup (React + Vite + TailwindCSS)
Open terminal in frontend/

Install dependencies:

powershell
Copy code
npm install
Install UI libraries (already in package.json but run if missing):

powershell
Copy code
npm install react-router-dom chart.js react-chartjs-2 leaflet
npm install -D tailwindcss@3.4.10 postcss autoprefixer
Create/verify postcss.config.js:

js
Copy code
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
Create/verify tailwind.config.js:

js
Copy code
/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: { extend: {} },
  plugins: [],
}
In src/index.css add:

css
Copy code
@tailwind base;
@tailwind components;
@tailwind utilities;
Run frontend:

powershell
Copy code
npm run dev
Test:

Open http://localhost:5173 → should show “Indore Rail AI Dashboard”

📊 Data
CSV files are inside /backend/data/:

stations.csv

sections.csv (includes mainline + loop sections)

platforms.csv

loops.csv

trains.csv

timetable.csv

These define the Indore corridor network, trains, timetables, and loops.

✅ Verification Checklist
 Backend /ping works on port 8000

 Frontend dashboard runs on port 5173

 Tailwind classes apply (blue heading test works)

 CSV data is loadable by backend

🚀 Next Steps
Implement simulation loop (SimPy) in backend

Send live train states via WebSocket/REST

Render trains on Leaflet map in frontend

Add Optimize button → OR-Tools backend call → update UI with conflict resolution

Show KPIs (Passenger-minutes saved, delays reduced, energy proxy)

👥 Contributors
Team SIH 2025 – Indore Corridor Project

pgsql
Copy code

---

This file is already in Markdown format (`.md`), so just copy it into **`README.md`** and push it to your repo.  

Do you want me to also prepare a **ready-to-use `requirements.txt`** and `package.json` snippet with pinned versions so nobody pulls unstable Tailwind 4.x again?





Ask ChatGPT
