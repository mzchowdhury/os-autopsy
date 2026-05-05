class MemoryManager:
    def __init__(self, total=512):
        self.total = total
        self.used = 0
        self.allocations = {}
        self.history = []

    def allocate(self, process, cycle):
        if self.used + process.memory_required > self.total:
            return False, "OVERFLOW"
        self.used += process.memory_required
        self.allocations[process.pid] = process.memory_required
        self.history.append((cycle, process.pid, "ALLOC", self.used))
        return True, "OK"

    def free(self, process, cycle):
        if process.pid in self.allocations:
            self.used -= self.allocations[process.pid]
            del self.allocations[process.pid]
            self.history.append((cycle, process.pid, "FREE", self.used))
            return True
        return False

    def usage_percent(self):
        return (self.used / self.total) * 100

    def is_overflowed(self):
        return self.used >= self.total