from enum import Enum
import random

class ProcessState(Enum):
    NEW = "New"
    READY = "Ready"
    RUNNING = "Running"
    WAITING = "Waiting"
    TERMINATED = "Terminated"

class Process:
    def __init__(self, pid, name, priority, burst_time, memory_required):
        self.pid = pid
        self.name = name
        self.priority = priority
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.memory_required = memory_required
        self.state = ProcessState.READY
        self.waiting_cycles = 0
        self.held_resources = []
        self.requested_resources = []
        self.creation_cycle = 0

    def __repr__(self):
        return f"Process({self.pid}, {self.name}, {self.state.value})"


class ProcessManager:
    def __init__(self):
        self.processes = []
        self.next_pid = 1
        self.terminated = []

    def create_process(self, name, priority, burst_time, memory_required, cycle):
        p = Process(self.next_pid, name, priority, burst_time, memory_required)
        p.creation_cycle = cycle
        self.processes.append(p)
        self.next_pid += 1
        return p

    def kill_process(self, pid):
        for p in self.processes:
            if p.pid == pid:
                p.state = ProcessState.TERMINATED
                self.terminated.append(p)
                self.processes.remove(p)
                return p
        return None

    def get_active(self):
        return [p for p in self.processes if p.state != ProcessState.TERMINATED]

    def get_by_pid(self, pid):
        for p in self.processes:
            if p.pid == pid:
                return p
        return None