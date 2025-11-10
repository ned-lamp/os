# CPU Scheduling Simulator in Python
# Algorithms: FCFS, SJF (Preemptive), Priority (Non-Preemptive), Round Robin (Preemptive)

def find_waiting_time_fcfs(processes):
    wt = [0] * len(processes)
    processes.sort(key=lambda x: x[1])  # Sort by arrival time
    service_time = processes[0][1]
    for i in range(1, len(processes)):
        service_time += processes[i-1][2]
        wt[i] = max(0, service_time - processes[i][1])
    return wt

def find_turnaround_time(processes, wt):
    tat = [processes[i][2] + wt[i] for i in range(len(processes))]
    return tat

def find_avg_time_fcfs(processes):
    wt = find_waiting_time_fcfs(processes)
    tat = find_turnaround_time(processes, wt)
    print("\nFCFS Scheduling:")
    print("PID\tAT\tBT\tWT\tTAT")
    for i in range(len(processes)):
        print(f"{processes[i][0]}\t{processes[i][1]}\t{processes[i][2]}\t{wt[i]}\t{tat[i]}")
    print(f"Average Waiting Time: {sum(wt)/len(wt):.2f}")
    print(f"Average Turnaround Time: {sum(tat)/len(tat):.2f}")

# ---------------- SJF Preemptive ----------------
def sjf_preemptive(processes):
    n = len(processes)
    rt = [p[2] for p in processes]
    complete = 0
    t = 0
    wt = [0]*n
    tat = [0]*n
    minm = 999999999
    short = 0
    check = False

    while complete != n:
        for j in range(n):
            if processes[j][1] <= t and rt[j] < minm and rt[j] > 0:
                minm = rt[j]
                short = j
                check = True
        if not check:
            t += 1
            continue

        rt[short] -= 1
        minm = rt[short] if rt[short] > 0 else 999999999

        if rt[short] == 0:
            complete += 1
            check = False
            fint = t + 1
            wt[short] = (fint - processes[short][2] - processes[short][1])
            if wt[short] < 0:
                wt[short] = 0
        t += 1

    tat = [processes[i][2] + wt[i] for i in range(n)]
    print("\nSJF (Preemptive):")
    print("PID\tAT\tBT\tWT\tTAT")
    for i in range(n):
        print(f"{processes[i][0]}\t{processes[i][1]}\t{processes[i][2]}\t{wt[i]}\t{tat[i]}")
    print(f"Average Waiting Time: {sum(wt)/n:.2f}")
    print(f"Average Turnaround Time: {sum(tat)/n:.2f}")

# ---------------- Priority Non-preemptive ----------------
def priority_non_preemptive(processes):
    processes.sort(key=lambda x: (x[1], x[3]))  # Sort by arrival then priority
    wt = [0]*len(processes)
    total_bt = 0
    for i in range(1, len(processes)):
        total_bt += processes[i-1][2]
        wt[i] = max(0, total_bt - processes[i][1])
    tat = [processes[i][2] + wt[i] for i in range(len(processes))]

    print("\nPriority Scheduling (Non-preemptive):")
    print("PID\tAT\tBT\tPR\tWT\tTAT")
    for i in range(len(processes)):
        print(f"{processes[i][0]}\t{processes[i][1]}\t{processes[i][2]}\t{processes[i][3]}\t{wt[i]}\t{tat[i]}")
    print(f"Average Waiting Time: {sum(wt)/len(wt):.2f}")
    print(f"Average Turnaround Time: {sum(tat)/len(tat):.2f}")

# ---------------- Round Robin Preemptive ----------------
def round_robin(processes, quantum):
    n = len(processes)
    rem_bt = [p[2] for p in processes]
    t = 0
    wt = [0]*n

    while True:
        done = True
        for i in range(n):
            if rem_bt[i] > 0:
                done = False
                if rem_bt[i] > quantum:
                    t += quantum
                    rem_bt[i] -= quantum
                else:
                    t += rem_bt[i]
                    wt[i] = t - processes[i][2] - processes[i][1]
                    rem_bt[i] = 0
        if done:
            break
    tat = [processes[i][2] + wt[i] for i in range(n)]

    print("\nRound Robin (Preemptive):")
    print("PID\tAT\tBT\tWT\tTAT")
    for i in range(n):
        print(f"{processes[i][0]}\t{processes[i][1]}\t{processes[i][2]}\t{wt[i]}\t{tat[i]}")
    print(f"Average Waiting Time: {sum(wt)/n:.2f}")
    print(f"Average Turnaround Time: {sum(tat)/n:.2f}")

# ---------------- Main ----------------
if __name__ == "__main__":
    processes = [
        [1, 0, 5, 2],   # [PID, Arrival Time, Burst Time, Priority]
        [2, 1, 3, 1],
        [3, 2, 8, 3],
        [4, 3, 6, 2]
    ]

    find_avg_time_fcfs(processes.copy())
    sjf_preemptive(processes.copy())
    priority_non_preemptive(processes.copy())
    round_robin(processes.copy(), quantum=2)
