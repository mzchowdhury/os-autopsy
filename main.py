import time
from process import ProcessManager
from scheduler import Scheduler
from memory import MemoryManager
from resources import ResourceManager
from crash_detector import CrashDetector
from autopsy import Autopsy
from ui import render_dashboard, render_crash, render_autopsy
from rich.console import Console
from rich.prompt import Prompt, IntPrompt

console = Console()

def setup():
    console.clear()
    console.print("\n[bold cyan]  Welcome to OS AUTOPSY SIMULATOR[/]")
    console.print("  [dim]Break the OS. Find out why it died.[/]\n")

    algo = Prompt.ask(
        "  Choose scheduling algorithm",
        choices=["FCFS", "SJF", "PRIORITY", "RR"],
        default="RR"
    )

    scheduler = Scheduler(algorithm=algo, quantum=3)
    memory = MemoryManager(total=512)
    resource_manager = ResourceManager()
    process_manager = ProcessManager()
    crash_detector = CrashDetector(starvation_threshold=10)

    console.print("\n  [bold]Creating initial processes...[/]\n")

    names = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon"]
    priorities = [3, 1, 4, 2, 5]
    bursts = [10, 6, 8, 12, 5]
    memory_req = [80, 120, 60, 150, 90]

    for i in range(5):
        p = process_manager.create_process(names[i], priorities[i], bursts[i], memory_req[i], cycle=0)
        ok, msg = memory.allocate(p, cycle=0)
        if not ok:
            console.print(f"  [red]Memory full! Could not load {names[i]}[/]")

    return scheduler, memory, resource_manager, process_manager, crash_detector

def main():
    scheduler, memory, resource_manager, process_manager, crash_detector = setup()

    cycle = 0
    console.print("\n  [bold green]System booting...[/]")
    time.sleep(1.5)

    while True:
        cycle += 1
        processes = process_manager.get_active()

        if not processes:
            console.print("\n  [bold yellow]All processes terminated. No crash.[/]")
            break

        # check crash FIRST before anything else
        crashed, crash_info = crash_detector.check(
            process_manager.get_active(), memory, resource_manager, cycle
        )

        if crashed:
            render_dashboard(processes, memory, cycle, crash_detector.warnings, scheduler)
            time.sleep(0.5)
            render_crash()
            report = Autopsy(
                crash_info,
                crash_detector.warnings,
                memory,
                scheduler,
                process_manager.processes + process_manager.terminated
            ).generate()
            render_autopsy(report)
            break

        # schedule
        current = scheduler.schedule(processes, cycle)
        if current:
            terminated = scheduler.tick(current)
            if terminated:
                memory.free(current, cycle)
                process_manager.kill_process(current.pid)

        # render
        render_dashboard(processes, memory, cycle, crash_detector.warnings, scheduler)

        # user action every 5 cycles
        if cycle % 5 == 0:
            console.print("\n  [bold]YOUR TURN — What do you want to do?[/]")
            console.print("  [dim]1. Assign resource to process[/]")
            console.print("  [dim]2. Release resource from process[/]")
            console.print("  [dim]3. Allocate more memory to process[/]")
            console.print("  [dim]4. Do nothing[/]")

            choice = Prompt.ask("  Choice", choices=["1", "2", "3", "4"], default="4")

            if choice == "1":
                pid = IntPrompt.ask("  PID")
                res = Prompt.ask("  Resource", choices=["R1", "R2", "R3"])
                p = process_manager.get_by_pid(pid)
                if p:
                    granted, msg = resource_manager.request(p, res)
                    console.print(f"  [cyan]{msg}[/]")
                    time.sleep(0.8)

            elif choice == "2":
                pid = IntPrompt.ask("  PID")
                res = Prompt.ask("  Resource", choices=["R1", "R2", "R3"])
                p = process_manager.get_by_pid(pid)
                if p:
                    resource_manager.release(p, res)
                    console.print("  [green]Released[/]")
                    time.sleep(0.8)

            elif choice == "3":
                pid = IntPrompt.ask("  PID")
                p = process_manager.get_by_pid(pid)
                if p:
                    p.memory_required = 100
                    ok, msg = memory.allocate(p, cycle)
                    console.print(f"  [cyan]{msg}[/]")
                    time.sleep(0.8)

    time.sleep(0.6)

if __name__ == "__main__":
    main()