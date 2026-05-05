class Autopsy:
    def __init__(self, crash, warnings, memory, scheduler, processes):
        self.crash = crash
        self.warnings = warnings
        self.memory = memory
        self.scheduler = scheduler
        self.processes = processes

    def generate(self):
        report = []
        report.append("=" * 45)
        report.append("         OS AUTOPSY REPORT")
        report.append("=" * 45)
        report.append(f"  TIME OF DEATH        : Cycle {self.crash['cycle']}")
        report.append(f"  CAUSE OF DEATH       : {self.crash['type']}")
        report.append(f"  DETAILS              : {self.crash['details']}")
        report.append(f"  MEMORY AT DEATH      : {self.memory.used}/{self.memory.total} units")
        report.append(f"  SCHEDULING ALGORITHM : {self.scheduler.algorithm}")
        report.append(f"  TOTAL PROCESSES      : {len(self.processes)}")
        report.append("-" * 45)

        if self.warnings:
            report.append("  EARLY WARNING SIGNS  :")
            for w in self.warnings[-3:]:
                report.append(f"    {w}")
        else:
            report.append("  EARLY WARNING SIGNS  : None detected")

        report.append("-" * 45)

        if self.crash["type"] == "DEADLOCK":
            report.append("  VERDICT: Circular resource waiting detected.")
            report.append("  FIX    : Release resources before requesting new ones.")
        elif self.crash["type"] == "MEMORY OVERFLOW":
            report.append("  VERDICT: Memory pool exhausted.")
            report.append("  FIX    : Free terminated process memory earlier.")
        elif self.crash["type"] == "STARVATION":
            report.append("  VERDICT: Process was never given CPU time.")
            report.append("  FIX    : Use Round Robin or aging to prevent starvation.")

        report.append("=" * 45)
        return report