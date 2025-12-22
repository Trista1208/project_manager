# src/core/scheduler.py
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from pathlib import Path
import json


class Scheduler:
    def __init__(
            self,
            start_time: datetime | None = None,
            work_morning_start: int = 8,
            work_morning_end: int = 12,
            work_afternoon_start: int = 14,
            work_afternoon_end: int = 17,
            state_file: Optional[Path] = None,
    ):
        self.start_time = start_time
        self.work_morning_start = work_morning_start
        self.work_morning_end = work_morning_end
        self.work_afternoon_start = work_afternoon_start
        self.work_afternoon_end = work_afternoon_end

        # Load state file path
        if state_file is None:
            project_root = Path(__file__).parent.parent.parent
            state_file = project_root / "state" / "project_state.json"
        self.state_file = state_file

    def _load_busy_periods(self) -> List[Dict[str, datetime]]:
        """Load already scheduled tasks - always read fresh from file."""
        busy_periods = []

        project_root = Path(__file__).parent.parent.parent
        state_file = project_root / "state" / "project_state.json"

        print(f"[SCHEDULER] Loading busy periods from {state_file}")

        if not state_file.exists():
            print(f"[SCHEDULER] State file doesn't exist")
            return busy_periods

        try:
            with open(state_file, "r") as f:
                content = f.read()
                if not content or not content.strip():
                    print(f"[SCHEDULER] State file is empty")
                    return busy_periods
                state = json.loads(content)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"[SCHEDULER] Error reading state: {e}")
            return busy_periods

        scheduled_tasks = state.get("scheduled_tasks", {})
        print(f"[SCHEDULER] Found {len(scheduled_tasks)} existing tasks")

        for task_key, task in scheduled_tasks.items():
            try:
                start = datetime.fromisoformat(task["start"])
                end = datetime.fromisoformat(task["end"])
                busy_periods.append({"start": start, "end": end, "task": task_key})
                print(f"[SCHEDULER]   Busy: {start} → {end}")
            except (KeyError, ValueError) as e:
                print(f"[SCHEDULER]   Skipping invalid task: {e}")
                continue

        busy_periods.sort(key=lambda x: x["start"])
        return busy_periods

    def _is_time_free(self, start: datetime, end: datetime, busy_periods: List[Dict]) -> bool:
        """Check if a time period is free (no overlap with busy periods)."""
        for busy in busy_periods:
            # Check for overlap
            if start < busy["end"] and end > busy["start"]:
                return False
        return True

    def _find_next_free_slot(
            self,
            desired_start: datetime,
            duration_hours: float,
            busy_periods: List[Dict],
            now: datetime
    ) -> datetime:
        """Find the next available start time that doesn't conflict with busy periods."""
        current = self._align_to_business(desired_start)

        max_iterations = 100  # Prevent infinite loops
        iteration = 0

        while iteration < max_iterations:
            iteration += 1

            # Get the blocks needed for this duration
            blocks = self._get_work_blocks(current, duration_hours)
            if not blocks:
                current = self._align_to_business(current + timedelta(hours=1))
                continue

            # Check if ALL blocks are free
            all_free = True
            for block in blocks:
                if not self._is_time_free(block["start"], block["end"], busy_periods):
                    all_free = False
                    break

            if all_free:
                return current

            # Find the conflicting busy period and skip past it
            for block in blocks:
                for busy in busy_periods:
                    if block["start"] < busy["end"] and block["end"] > busy["start"]:
                        # Move to after this busy period
                        current = self._align_to_business(busy["end"])
                        break
                else:
                    continue
                break

        return current

    def schedule(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Schedule tasks avoiding conflicts with already scheduled tasks.

        tasks: list of dicts:
        {
          "task": "Do X",
          "duration": 2,          # hours (float allowed)
          "depends_on": ["Other task"]
        }
        Returns calendar events with ISO8601 "start" and "end".
        """

        # Load existing busy periods
        busy_periods = self._load_busy_periods()
        print(f"[SCHEDULER] Loaded {len(busy_periods)} existing scheduled tasks")

        # --- Topological order by depends_on ---
        lookup = {t["task"]: t for t in tasks}
        completed = set()
        ordered: List[Dict[str, Any]] = []

        def visit(name: str):
            if name in completed:
                return
            deps = lookup[name].get("depends_on", []) or []
            for d in deps:
                if d in lookup:
                    visit(d)
            completed.add(name)
            ordered.append(lookup[name])

        for t in tasks:
            visit(t["task"])

        # max 5 tasks per scheduling run
        if len(ordered) > 5:
            ordered = ordered[:5]

        now = datetime.now()
        current = self.start_time or now
        current = self._next_work_start(current, now)

        # Result: list of calendar events
        scheduled_events = []

        for t in ordered:
            duration = float(t.get("duration", 1.0) or 1.0)

            # Find next free slot that doesn't conflict
            start = self._find_next_free_slot(current, duration, busy_periods, now)
            blocks = self._get_work_blocks(start, duration)

            for i, block in enumerate(blocks):
                block_start = block["start"]
                block_end = block["end"]

                # Create event name (add part number if split)
                if len(blocks) > 1:
                    event_name = f"{t['task']} (Part {i + 1}/{len(blocks)})"
                else:
                    event_name = t["task"]

                event = {
                    "task": event_name,
                    "original_task": t["task"],
                    "start": block_start.isoformat(),
                    "end": block_end.isoformat(),
                    "duration": (block_end - block_start).total_seconds() / 3600,
                    "depends_on": t.get("depends_on", []),
                }

                scheduled_events.append(event)

                # Add to busy_periods so subsequent tasks don't overlap
                busy_periods.append({"start": block_start, "end": block_end, "task": event_name})

            # Next task starts after this one ends
            current = blocks[-1]["end"]

        # Re-sort busy periods after adding new ones
        busy_periods.sort(key=lambda x: x["start"])

        return scheduled_events

    # ---- helpers ----

    def _next_work_start(self, dt: datetime, now: datetime) -> datetime:
        """Move to the next valid work time (>= now, inside 8–12 or 14–17)."""
        if dt < now:
            dt = now

        if dt.minute or dt.second or dt.microsecond:
            dt = dt.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)

        return self._align_to_business(dt)

    def _align_to_business(self, dt: datetime) -> datetime:
        """Snap dt forward into a valid work block (08–12 or 14–17)."""
        dt = dt.replace(minute=0, second=0, microsecond=0)

        iterations = 0
        while True:
            iterations += 1
            if iterations > 10:
                break

            hour = dt.hour

            if self.work_morning_start <= hour < self.work_morning_end:
                return dt

            if self.work_afternoon_start <= hour < self.work_afternoon_end:
                return dt

            if hour < self.work_morning_start:
                return dt.replace(hour=self.work_morning_start)

            if self.work_morning_end <= hour < self.work_afternoon_start:
                return dt.replace(hour=self.work_afternoon_start)

            dt = (dt + timedelta(days=1)).replace(
                hour=self.work_morning_start, minute=0, second=0, microsecond=0
            )

        return dt

    def _get_work_blocks(self, start: datetime, hours: float) -> List[Dict[str, datetime]]:
        """Split work hours into individual calendar blocks."""
        blocks = []
        current = self._align_to_business(start)
        remaining = float(hours)

        iterations = 0
        while remaining > 0:
            iterations += 1
            if iterations > 20:
                break

            hour = current.hour

            if self.work_morning_start <= hour < self.work_morning_end:
                end_block = current.replace(
                    hour=self.work_morning_end, minute=0, second=0, microsecond=0
                )
            elif self.work_afternoon_start <= hour < self.work_afternoon_end:
                end_block = current.replace(
                    hour=self.work_afternoon_end, minute=0, second=0, microsecond=0
                )
            else:
                current = self._align_to_business(current)
                continue

            available = (end_block - current).total_seconds() / 3600.0

            if remaining <= available:
                block_end = current + timedelta(hours=remaining)
                blocks.append({"start": current, "end": block_end})
                break
            else:
                blocks.append({"start": current, "end": end_block})
                remaining -= available

                if end_block.hour == self.work_morning_end:
                    current = end_block.replace(
                        hour=self.work_afternoon_start, minute=0, second=0, microsecond=0
                    )
                else:
                    current = (end_block + timedelta(days=1)).replace(
                        hour=self.work_morning_start, minute=0, second=0, microsecond=0
                    )

        return blocks