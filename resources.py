class ResourceManager:
    def __init__(self):
        self.resources = {
            "R1": {"total": 1, "available": 1, "held_by": []},
            "R2": {"total": 1, "available": 1, "held_by": []},
            "R3": {"total": 1, "available": 1, "held_by": []},
        }
        self.wait_for_graph = {}

    def request(self, process, resource_name):
        r = self.resources.get(resource_name)
        if not r:
            return False, "Resource not found"
        if r["available"] > 0:
            r["available"] -= 1
            r["held_by"].append(process.pid)
            process.held_resources.append(resource_name)
            return True, "GRANTED"
        else:
            process.requested_resources.append(resource_name)
            process.waiting_cycles += 1
            holders = list(r["held_by"])
            if process.pid not in self.wait_for_graph:
                self.wait_for_graph[process.pid] = []
            for holder_pid in holders:
                if holder_pid not in self.wait_for_graph[process.pid]:
                    self.wait_for_graph[process.pid].append(holder_pid)
            return False, "WAITING"

    def release(self, process, resource_name):
        r = self.resources.get(resource_name)
        if not r:
            return False
        if process.pid in r["held_by"]:
            r["held_by"].remove(process.pid)
            r["available"] += 1
            if resource_name in process.held_resources:
                process.held_resources.remove(resource_name)
            if process.pid in self.wait_for_graph:
                del self.wait_for_graph[process.pid]
            return True
        return False

    def detect_deadlock(self):
        graph = self.wait_for_graph
        if not graph:
            return False, []

        visited = set()
        stack = set()

        def has_cycle(node):
            visited.add(node)
            stack.add(node)
            for neighbour in graph.get(node, []):
                if neighbour not in visited:
                    if has_cycle(neighbour):
                        return True
                elif neighbour in stack:
                    return True
            stack.discard(node)
            return False

        for node in list(graph.keys()):
            if node not in visited:
                if has_cycle(node):
                    return True, list(graph.keys())

        return False, []