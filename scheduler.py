from process import ProcessState

class Scheduler:
    def __init__(self, algorithm="RR", quantum=3):
        self.algorithm = algorithm
        self.quantum = quantum
        self.current_quantum = 0
        self.current_process = None
        self.rr_queue = []
        self.history = []

    def schedule(self, processes, cycle):
        ready = [p for p in processes if p.state == ProcessState.READY]

        # increment waiting cycles for non-running processes
        for p in processes:
            if p.state == ProcessState.WAITING or p.state == ProcessState.READY:
                p.waiting_cycles += 1

        if self.algorithm == "FCFS":
            return self._fcfs(ready, cycle)
        elif self.algorithm == "SJF":
            return self._sjf(ready, cycle)
        elif self.algorithm == "PRIORITY":
            return self._priority(ready, cycle)
        elif self.algorithm == "RR":
            return self._round_robin(ready, cycle)

    def _fcfs(self, ready, cycle):
        if not ready:
            return None
        p = sorted(ready, key=lambda x: x.creation_cycle)[0]
        p.state = ProcessState.RUNNING
        self.history.append((cycle, p.pid))
        return p

    def _sjf(self, ready, cycle):
        if not ready:
            return None
        p = sorted(ready, key=lambda x: x.remaining_time)[0]
        p.state = ProcessState.RUNNING
        self.history.append((cycle, p.pid))
        return p

    def _priority(self, ready, cycle):
        if not ready:
            return None
        p = sorted(ready, key=lambda x: x.priority, reverse=True)[0]
        p.state = ProcessState.RUNNING
        self.history.append((cycle, p.pid))
        return p

    def _round_robin(self, ready, cycle):
        if not ready:
            return None

        if self.current_process and self.current_process in ready:
            if self.current_quantum < self.quantum:
                self.current_quantum += 1
                self.current_process.state = ProcessState.RUNNING
                return self.current_process

        if ready:
            if self.current_process in ready:
                idx = ready.index(self.current_process)
                next_p = ready[(idx + 1) % len(ready)]
            else:
                next_p = ready[0]

            self.current_process = next_p
            self.current_quantum = 1
            next_p.state = ProcessState.RUNNING
            self.history.append((cycle, next_p.pid))
            return next_p

    def tick(self, process):
        if process:
            process.remaining_time -= 1
            if process.remaining_time <= 0:
                process.state = ProcessState.TERMINATED
                return True
        return False