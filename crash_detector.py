class CrashDetector:
    def __init__(self, starvation_threshold=10):
        self.starvation_threshold = starvation_threshold
        self.warnings = []
        self.crash = None

    def check(self, processes, memory, resource_manager, cycle):
        # check memory overflow
        if memory.is_overflowed():
            self.crash = {
                "type": "MEMORY OVERFLOW",
                "cycle": cycle,
                "details": f"Memory reached {memory.used}/{memory.total} units"
            }
            return True, self.crash

        # check deadlock
        deadlocked, involved = resource_manager.detect_deadlock()
        if deadlocked:
            self.crash = {
                "type": "DEADLOCK",
                "cycle": cycle,
                "details": f"Processes involved: {involved}"
            }
            return True, self.crash

        # check starvation
        for p in processes:
            if p.waiting_cycles >= self.starvation_threshold:
                warning = f"[Cycle {cycle}] WARNING: Process {p.name} (PID {p.pid}) waiting {p.waiting_cycles} cycles"
                if warning not in self.warnings:
                    self.warnings.append(warning)
                if p.waiting_cycles >= self.starvation_threshold * 2:
                    self.crash = {
                        "type": "STARVATION",
                        "cycle": cycle,
                        "details": f"Process {p.name} (PID {p.pid}) starved after {p.waiting_cycles} cycles"
                    }
                    return True, self.crash

        return False, None
        