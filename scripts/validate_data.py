"""
scripts/validate_data.py
Phase 1: Data validation + canonical export
Normalizes raw CSVs into a canonical schema for simulator/backend use.
"""

import pandas as pd
from pathlib import Path

# --- Directories ---
RAW = Path("data/raw")
CANONICAL = Path("data/canonical")
REPORTS = Path("data/reports")

CANONICAL.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

def validate():
    report_lines = []

    # --- Load + normalize stations ---
    stations = pd.read_csv(RAW / "stations.csv")
    stations = stations.rename(columns={
        "station_id": "station_code",
        "name": "station_name",
        "platform_count": "no_of_platforms",
        "track_count": "no_of_tracks"
    })

    # --- Load + normalize sections ---
    sections = pd.read_csv(RAW / "sections.csv")
    sections = sections.rename(columns={
        "single_or_double": "track_type"
    })
    # keep: section_id, from_station, to_station, length_km, max_speed_kmph, electrified, track_type

    # --- Load + normalize trains ---
    trains = pd.read_csv(RAW / "trains.csv")
    trains = trains.rename(columns={
        "name": "train_name",
        "priority_wt": "priority"
    })
    # keep: train_id, train_name, type, priority, length_m, seats_or_tonnage,
    # accel_mps2, decel_mps2, speed_class_kmph, dwell_std_min

    # --- Load + normalize timetable ---
    timetable = pd.read_csv(RAW / "timetable.csv")
    timetable = timetable.rename(columns={
        "station_id": "station_code",
        "sched_arrival": "arr_time",
        "sched_departure": "dep_time"
    })
    # keep: train_id, station_code, arr_time, dep_time, dwell_min

    # --- Load + normalize platforms ---
    platforms = pd.read_csv(RAW / "platforms.csv")
    platforms = platforms.rename(columns={
        "station_id": "station_code"
    })
    # keep: station_code, platform_id, length_m

    # --- Load + normalize loops ---
    loops = pd.read_csv(RAW / "loops.csv")
    loops = loops.rename(columns={
        "station_id": "station_code"
    })
    # keep: station_code, loop_id, length_m

    # --- 1. Section endpoints must exist ---
    missing_nodes = (
        set(sections["from_station"]) | set(sections["to_station"])
    ) - set(stations["station_code"])
    if missing_nodes:
        report_lines.append(f"Invalid section endpoints: {missing_nodes}")

    # --- 2. Platform length >= train length ---
    train_lengths = dict(zip(trains["train_id"], trains["length_m"]))
    for _, row in timetable.iterrows():
        tid = row["train_id"]
        stn = row["station_code"]
        train_len = train_lengths.get(tid, 0)
        fits = platforms[platforms["station_code"] == stn]["length_m"].max()
        if pd.notna(fits) and train_len > fits:
            report_lines.append(f"Train {tid} too long for station {stn}")

    # --- 3. Track type sanity ---
    bad_tracks = sections.loc[~sections["track_type"].isin(["single", "double"])]
    if not bad_tracks.empty:
        report_lines.append(
            f"Invalid track_type rows: {bad_tracks.to_dict('records')}"
        )

    # --- 4. Dwell times must be >= 0 ---
    if "dwell_min" in timetable.columns:
        bad_dwell = timetable.loc[timetable["dwell_min"] < 0]
        if not bad_dwell.empty:
            report_lines.append(
                f"Negative dwell times for trains: {bad_dwell['train_id'].tolist()}"
            )

    # --- 5. Save canonical JSONs ---
    stations.to_json(CANONICAL / "stations.json", orient="records", indent=2)
    sections.to_json(CANONICAL / "sections.json", orient="records", indent=2)
    trains.to_json(CANONICAL / "trains.json", orient="records", indent=2)
    timetable.to_json(CANONICAL / "timetable.json", orient="records", indent=2)
    platforms.to_json(CANONICAL / "platforms.json", orient="records", indent=2)
    loops.to_json(CANONICAL / "loops.json", orient="records", indent=2)

    # --- 6. Report ---
    report_file = REPORTS / "data_quality_report.md"
    with open(report_file, "w", encoding="utf-8") as f:
        if not report_lines:
            f.write("# Data Quality Report\nAll checks passed ✅\n")
        else:
            f.write("# Data Quality Report\n")
            f.write("\n".join([f"- {line}" for line in report_lines]))

    print(f"Validation complete. Report saved to {report_file}")

if __name__ == "__main__":
    validate()
