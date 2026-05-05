from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import BarColumn, Progress
from rich import box
from rich.text import Text
import time

console = Console()

def render_dashboard(processes, memory, cycle, warnings, scheduler):
    console.clear()

    console.print(f"\n[bold cyan]  ██████  ███████      ██████  ███████[/]\n  [bold cyan]██    ██ ██          ██    ██ ██[/]\n  [bold cyan]██    ██ ███████     ███████  ███████[/]\n  [bold cyan]██    ██      ██     ██            ██[/]\n  [bold cyan] ██████  ███████     ██       ███████[/]\n")
    console.print(f"[bold white]  AUTOPSY SIMULATOR[/]  [dim]Cycle: {cycle}  |  Algorithm: {scheduler.algorithm}[/]\n")

    # process table
    table = Table(box=box.SIMPLE_HEAVY, show_header=True, header_style="bold cyan")
    table.add_column("PID", style="dim", width=5)
    table.add_column("Name", width=12)
    table.add_column("State", width=12)
    table.add_column("Priority", width=9)
    table.add_column("Remaining", width=10)
    table.add_column("Waiting", width=8)
    table.add_column("Holds", width=12)

    for p in processes:
        state_color = {
            "Running": "bold green",
            "Ready": "yellow",
            "Waiting": "red",
            "Terminated": "dim",
            "New": "cyan"
        }.get(p.state.value, "white")

        table.add_row(
            str(p.pid),
            p.name,
            f"[{state_color}]{p.state.value}[/]",
            str(p.priority),
            str(p.remaining_time),
            str(p.waiting_cycles),
            ", ".join(p.held_resources) or "-"
        )

    console.print(table)

    # memory bar
    pct = memory.usage_percent()
    bar_filled = int(pct / 5)
    bar = "█" * bar_filled + "░" * (20 - bar_filled)
    color = "green" if pct < 60 else "yellow" if pct < 85 else "red"
    console.print(f"  [bold]MEMORY[/]  [{color}]{bar}[/] {memory.used}/{memory.total} units ({pct:.1f}%)\n")

    # warnings
    if warnings:
        for w in warnings[-2:]:
            console.print(f"  [bold yellow]⚠  {w}[/]")

def render_crash():
    console.clear()
    time.sleep(0.3)
    console.print("\n\n")
    console.print("[bold red]" + "█" * 45 + "[/]")
    console.print("[bold red]" + " " * 12 + "SYSTEM CRASH 💀" + " " * 12 + "[/]")
    console.print("[bold red]" + "█" * 45 + "[/]")
    console.print("\n  [dim red]Collecting crash data...[/]")
    time.sleep(2)

def render_autopsy(report):
    console.print("\n")
    for line in report:
        if "CAUSE OF DEATH" in line or "CRASH" in line:
            console.print(f"[bold red]{line}[/]")
        elif "===" in line or "---" in line:
            console.print(f"[bold cyan]{line}[/]")
        elif "FIX" in line:
            console.print(f"[bold green]{line}[/]")
        elif "WARNING" in line:
            console.print(f"[bold yellow]{line}[/]")
        else:
            console.print(f"[white]{line}[/]")
        time.sleep(0.08)