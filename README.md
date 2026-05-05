# OS Autopsy

> *Break the OS. Find out why it died.*

**OS Autopsy** is an interactive operating system simulator built in Python where you are given direct control over a live OS environment. You manage processes, allocate memory, and assign resources. Make the wrong decisions — create a deadlock, overflow memory, starve a process — and the system crashes. A forensic **autopsy report** then generates, telling you exactly what killed it, when the warning signs first appeared, and what the correct fix would have been.

This project was built as a course project for Operating Systems. It covers CPU scheduling, memory management, process lifecycle management, and deadlock detection — all in one cohesive, interactive system.

---

## Table of Contents

- [Concept](#concept)
- [Demo](#demo)
- [Features](#features)
- [OS Concepts Covered](#os-concepts-covered)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [How to Use](#how-to-use)
- [Crash Types](#crash-types)
- [Deadlock Demo Sequence](#deadlock-demo-sequence)
- [Autopsy Report](#autopsy-report)
- [Tech Stack](#tech-stack)
- [Author](#author)

---

## Concept

Most OS projects build systems that work correctly and demonstrate normal operation. OS Autopsy takes the opposite approach.

The premise is simple: the best way to understand how an operating system works is to watch one fail. The user is not a passive observer — they are the one making decisions that degrade the system. Every resource assignment, every memory allocation, every scheduling choice has a consequence. When the system finally crashes, it does not just stop — it generates a detailed forensic report explaining the exact chain of events that led to failure.

This makes abstract OS concepts tangible. Deadlock is not just a definition on a slide. It is something you caused, watched form cycle by cycle, and then read about in a post-mortem.

---

## Demo

Watch the full demo here: **[Demo Video Link]**

The demo shows:
- System booting with 5 active processes
- Live process table updating every cycle
- A deadlock being deliberately triggered through resource assignment
- The SYSTEM CRASH screen firing the moment circular wait is detected
- The autopsy report generating with cause of death, processes involved, and recommended fix

If you prefer to read rather than watch, everything you need to understand and run the project is documented below.

---

## Features

| Feature | Description |
|---|---|
| **4 Scheduling Algorithms** | Choose between FCFS, SJF, Priority, and Round Robin at startup |
| **Live Process Table** | Real-time view of all processes — state, priority, burst time, waiting cycles, held resources |
| **Memory Manager** | Visual memory bar showing pool usage. Allocate memory, watch it fill, trigger overflow |
| **Resource Allocation** | Assign and release R1, R2, R3 across processes every 5 cycles |
| **Deadlock Detection** | Wait-for graph with DFS cycle detection. Fires the moment circular wait forms |
| **3 Crash Types** | Deadlock, Memory Overflow, and Starvation — each with a unique autopsy |
| **Early Warning System** | Dashboard flags starvation warnings before the fatal crash occurs |
| **Forensic Autopsy Report** | Post-mortem showing time of death, cause, involved processes, and the fix |
| **Interactive Control** | Every 5 cycles you choose what happens next — or do nothing and watch it degrade |

---

## OS Concepts Covered

**CPU Scheduling**
Implements four classic scheduling algorithms. FCFS runs processes in arrival order. SJF selects the shortest remaining burst time. Priority scheduling favours higher-priority processes, which can cause starvation of low-priority ones. Round Robin distributes CPU time in fixed time quantum slices. The user selects the algorithm at startup, and their choice directly affects how quickly starvation can occur.

**Process Management**
Each process moves through a full lifecycle: New → Ready → Running → Waiting → Terminated. The process manager tracks all active processes, their current state, remaining burst time, and how long they have been waiting. When a process terminates, its memory is freed automatically.

**Memory Management**
A fixed memory pool of 512 units is allocated across all processes at creation. The user can manually allocate additional memory to any process during the simulation. The memory manager tracks all allocations, calculates usage percentage, and detects overflow the moment total usage reaches capacity.

**Deadlock**
Resources R1, R2, and R3 each have a single unit. Processes can hold resources and request additional ones. When a requested resource is unavailable, the process enters a waiting state and an edge is added to the wait-for graph pointing from the waiting process to the holding process. A Depth First Search runs on this graph every cycle. If a cycle is detected — meaning two or more processes are waiting on each other in a circle — deadlock is confirmed and the system crashes immediately.

---

## Project Structure

```
os_autopsy/
│
├── main.py              # Entry point. Main simulation loop and user interaction.
├── process.py           # Process class, ProcessState enum, ProcessManager.
├── scheduler.py         # FCFS, SJF, Priority, and Round Robin scheduling logic.
├── memory.py            # Memory pool allocation, deallocation, overflow detection.
├── resources.py         # Resource assignment, wait-for graph, deadlock detection via DFS.
├── crash_detector.py    # Monitors every cycle for deadlock, overflow, and starvation.
├── autopsy.py           # Generates the forensic post-mortem crash report.
└── ui.py                # Rich terminal dashboard, process table, memory bar, crash screen.
```

Each module handles exactly one OS concept. This separation mirrors how a real OS kernel separates concerns and made testing and debugging significantly more manageable.

---

## Installation

### Requirements

- Python 3.8 or higher
- pip

### Steps

**1. Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/os-autopsy.git
cd os-autopsy
```

**2. Install the only dependency**

```bash
pip install rich
```

**3. Run the simulator**

```bash
python main.py
```

No other setup required.

---

## How to Use

### Step 1 — Choose a scheduling algorithm

When the simulator starts, you will be prompted to choose:

```
Choose scheduling algorithm [FCFS/SJF/PRIORITY/RR]:
```

- **FCFS** — safe, unlikely to cause starvation
- **SJF** — can starve long processes
- **PRIORITY** — high risk of starving low-priority processes
- **RR** — balanced, good for demonstrating deadlock

### Step 2 — Watch the system run

The dashboard updates every cycle showing:

- All active processes with their current state, priority, remaining burst time, waiting cycles, and held resources
- A memory usage bar showing how full the pool is
- Any active warning messages in the lower section

### Step 3 — Take control every 5 cycles

Every 5 cycles the simulation pauses and presents:

```
YOUR TURN — What do you want to do?
  1. Assign resource to process
  2. Release resource from process
  3. Allocate more memory to process
  4. Do nothing
```

Your choices directly affect the system. Assigning resources can create deadlock. Allocating memory can cause overflow. Doing nothing repeatedly with a bad scheduling algorithm will cause starvation.

### Step 4 — Cause a crash

The goal is to crash the system. Each crash type requires a different approach. The system will display warnings before it finally dies.

### Step 5 — Read the autopsy

When the system crashes, a forensic report generates automatically showing exactly what happened and how it could have been prevented.

---

## Crash Types

### Deadlock

Occurs when two or more processes are each waiting on a resource held by the other. Neither can proceed. Neither will release. The system detects this using a cycle in the wait-for graph and crashes immediately.

**Triggered by:** Assigning resources in a circular pattern across processes.

**Autopsy shows:** Processes involved, cycle number of death, the circular dependency, and the fix.

---

### Memory Overflow

Occurs when total memory allocated across all processes reaches or exceeds the 512-unit pool.

**Triggered by:** Repeatedly allocating extra memory to processes using option 3.

**Autopsy shows:** Memory usage at time of death and which allocations pushed it over.

---

### Starvation

Occurs when a process is continually passed over by the scheduler and never gets CPU time. The system warns at 10 waiting cycles and crashes at 20.

**Triggered by:** Choosing PRIORITY or SJF scheduling with a low-priority or long process in the queue.

**Autopsy shows:** Which process was starved, how long it waited, and which scheduling algorithm caused it.

---

## Deadlock Demo Sequence

This sequence reliably triggers a deadlock crash and is suitable for demonstration purposes.

**At startup:** Choose `RR` (Round Robin).

| Cycle | Choice | PID | Resource | Response |
|---|---|---|---|---|
| 5 | 1 — Assign resource | 1 | R1 | GRANTED |
| 10 | 1 — Assign resource | 2 | R2 | GRANTED |
| 15 | 1 — Assign resource | 1 | R2 | WAITING |
| 20 | 1 — Assign resource | 2 | R1 | WAITING |
| 21 | — | — | — | **SYSTEM CRASH** |

**What is happening:**
- After cycle 15: P1 holds R1, wants R2. P2 holds R2. Graph: `{1: [2]}`
- After cycle 20: P2 holds R2, wants R1. P1 holds R1. Graph: `{1: [2], 2: [1]}`
- Cycle 21: DFS detects cycle in graph → deadlock confirmed → crash fires

---

## Autopsy Report

Every crash generates a report in this format:

```
=============================================
         OS AUTOPSY REPORT
=============================================
  TIME OF DEATH        : Cycle 21
  CAUSE OF DEATH       : DEADLOCK
  DETAILS              : Processes involved: [1, 2]
  MEMORY AT DEATH      : 500/512 units
  SCHEDULING ALGORITHM : RR
  TOTAL PROCESSES      : 5
---------------------------------------------
  EARLY WARNING SIGNS  : None detected
---------------------------------------------
  VERDICT: Circular resource waiting detected.
  FIX    : Release resources before requesting new ones.
=============================================
```

The report always includes:
- Exact cycle of death
- Cause of death and processes involved
- Memory state at time of crash
- Any early warnings that appeared before the crash
- A plain-language verdict and recommended fix

---

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.8+ |
| Terminal UI | [Rich](https://github.com/Textualize/rich) |
| Deadlock Detection | Depth First Search on adjacency list wait-for graph |
| Scheduling | Custom implementations of FCFS, SJF, Priority, Round Robin |
| Architecture | Modular — one Python file per OS concept |

---