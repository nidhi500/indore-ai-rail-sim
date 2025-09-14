"""
simulator/engine.py
Phase 2.1: Time-space simulator core (with real travel times)

- Loads canonical JSONs
- Simulates trains moving across sections with dwell times
- Respects section length & train speed
- Logs events to outputs/logs/
"""

import json
import uuid
from pathlib import Path
import pandas as pd
from datetime import timedelta, datetime

# --- Directories ---
CANONICAL = Path("data/canonical")
LOGS = Path("outputs/logs")
LOGS.mkdir(parents=True, exist_ok=True)

class Simulator:
    def __init__(self, tick_seconds: int = 60):
        self.tick = timedelta(seconds=tick_seconds)
        self.time = datetime.strptime("00:00", "%H:%M")  # simulation clock
        self.events = []
        self.trains = {}
        self.stations = {}
        self.sections = {}
        self.timetable = {}
        self.run_id = str(uuid.uuid4())[:8]

    # --- Load canonical JSONs ---
    def load_data(self):
        stations = pd.read_json(CANONICAL / "stations.json")
        sections = pd.read_json(CANONICAL / "sections.json")
        trains = pd.read_json(CANONICAL / "trains.json")
        timetable = pd.read_json(CANONICAL / "timetable.json")

        # normalize to dicts
        self.stations = stations.set_index("station_code").to_dict(orient="index")
        self.sections = sections.set_index("section_id").to_dict(orient="index")

        # build timetable as dict: train_id -> list of stops
        self.timetable = {
            k: g.to_dict("records")
            for k, g in timetable.groupby("train_id", group_keys=False)
        }

        # init train states
        for _, row in trains.iterrows():
            self.trains[row["train_id"]] = {
                "train_id": row["train_id"],
                "name": row.get("train_name", row["train_id"]),
                "priority": row.get("priority", 0),
                "speed_class_kmph": row["speed_class_kmph"],
                "length_m": row["length_m"],
                "schedule": self.timetable.get(row["train_id"], []),
                "current_index": 0,
                "status": "waiting",
                "next_event_time": None,
                "current_section": None,
            }

    # --- Utility: log event ---
    def log_event(self, train_id, event_type, station=None, section=None):
        evt = {
            "time": self.time.strftime("%H:%M"),
            "train_id": train_id,
            "event": event_type
        }
        if station:
            evt["station_code"] = station
        if section:
            evt["section_id"] = section
        self.events.append(evt)

    # --- Estimate travel time on section (minutes) ---
    def estimate_travel_time(self, train, from_station, to_station):
        # find section connecting from_station -> to_station
        section = None
        for sid, s in self.sections.items():
            if s["from_station"] == from_station and s["to_station"] == to_station:
                section = s
                break
            if s["to_station"] == from_station and s["from_station"] == to_station:
                section = s
                break

        if not section:
            # fallback if no section found
            return 5, "UNKNOWN"

        train_speed = train["speed_class_kmph"]
        sec_speed = section["max_speed_kmph"]
        sec_length = section["length_km"]

        effective_speed = min(train_speed, sec_speed)
        travel_hours = sec_length / effective_speed
        travel_min = travel_hours * 60

        return max(1, int(round(travel_min))), section.get("section_id", "UNKNOWN")

    # --- Step simulation ---
    def step(self):
        for tid, train in self.trains.items():
            sched = train["schedule"]
            idx = train["current_index"]

            if idx >= len(sched):
                continue  # finished

            current_stop = sched[idx]
            stn = current_stop["station_code"]

            # if waiting, log arrival
            if train["status"] == "waiting":
                self.log_event(tid, "arrive_station", station=stn)
                dwell = current_stop.get("dwell_min", 0)
                train["status"] = "dwelling"
                train["next_event_time"] = self.time + timedelta(minutes=dwell)

            # if dwelling and time reached, depart
            elif train["status"] == "dwelling" and self.time >= train["next_event_time"]:
                self.log_event(tid, "depart_station", station=stn)
                if idx + 1 < len(sched):
                    next_stop = sched[idx + 1]["station_code"]
                    travel_min, sec_id = self.estimate_travel_time(train, stn, next_stop)
                    train["status"] = "enroute"
                    train["current_section"] = sec_id
                    train["next_event_time"] = self.time + timedelta(minutes=travel_min)
                    self.log_event(tid, "enter_section", section=sec_id)
                else:
                    train["status"] = "done"

            # if enroute and time reached, exit section
            elif train["status"] == "enroute" and self.time >= train["next_event_time"]:
                sec_id = train["current_section"]
                self.log_event(tid, "exit_section", section=sec_id)
                train["status"] = "waiting"
                train["current_index"] += 1

        # advance clock
        self.time += self.tick

    # --- Run until given sim minutes ---
    def run_until(self, minutes: int):
        steps = int(minutes * 60 / self.tick.total_seconds())
        for _ in range(steps):
            self.step()

    # --- Save events log ---
    def save_logs(self):
        out_path = LOGS / f"{self.run_id}_events.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(self.events, f, indent=2)
        print(f"Saved events log to {out_path}")

if __name__ == "__main__":
    sim = Simulator(tick_seconds=60)
    sim.load_data()
    sim.run_until(60)  # run 60 minutes
    sim.save_logs()
