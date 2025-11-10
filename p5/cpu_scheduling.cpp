#include <iostream>
#include <vector>
#include <algorithm>
#include <queue>
using namespace std;

struct Process {
    int pid;
    int arrival;
    int burst;
    int priority;
    int remaining;
    int waiting;
    int turnaround;
};

// ---------- FCFS ----------
void fcfs(vector<Process> p) {
    cout << "\n=== FCFS Scheduling ===\n";
    int time = 0;
    for (auto &pr : p) {
        if (time < pr.arrival) time = pr.arrival;
        pr.waiting = time - pr.arrival;
        time += pr.burst;
        pr.turnaround = pr.waiting + pr.burst;
        cout << "P" << pr.pid << " ";
    }

    double avgWait = 0, avgTurn = 0;
    for (auto &pr : p) {
        avgWait += pr.waiting;
        avgTurn += pr.turnaround;
    }

    cout << "\nAverage Waiting Time: " << avgWait / p.size();
    cout << "\nAverage Turnaround Time: " << avgTurn / p.size() << "\n";
}

// ---------- SJF (Preemptive) ----------
void sjfPreemptive(vector<Process> p) {
    cout << "\n=== SJF (Preemptive) Scheduling ===\n";
    int completed = 0, time = 0, n = p.size();
    int shortest = -1, minBurst = 1e9;
    for (auto &pr : p) pr.remaining = pr.burst;

    while (completed < n) {
        shortest = -1;
        minBurst = 1e9;

        for (int i = 0; i < n; i++) {
            if (p[i].arrival <= time && p[i].remaining > 0 && p[i].remaining < minBurst) {
                minBurst = p[i].remaining;
                shortest = i;
            }
        }

        if (shortest == -1) { time++; continue; }

        p[shortest].remaining--;
        cout << "P" << p[shortest].pid << " ";
        time++;

        if (p[shortest].remaining == 0) {
            completed++;
            p[shortest].turnaround = time - p[shortest].arrival;
            p[shortest].waiting = p[shortest].turnaround - p[shortest].burst;
        }
    }

    double avgWait = 0, avgTurn = 0;
    for (auto &pr : p) {
        avgWait += pr.waiting;
        avgTurn += pr.turnaround;
    }

    cout << "\nAverage Waiting Time: " << avgWait / n;
    cout << "\nAverage Turnaround Time: " << avgTurn / n << "\n";
}

// ---------- Priority (Non-Preemptive) ----------
void priorityScheduling(vector<Process> p) {
    cout << "\n=== Priority (Non-Preemptive) Scheduling ===\n";
    int time = 0, completed = 0;
    int n = p.size();
    vector<int> done(n, 0);

    while (completed < n) {
        int idx = -1, bestPri = 1e9;
        for (int i = 0; i < n; i++) {
            if (p[i].arrival <= time && !done[i] && p[i].priority < bestPri) {
                bestPri = p[i].priority;
                idx = i;
            }
        }

        if (idx == -1) { time++; continue; }

        p[idx].waiting = time - p[idx].arrival;
        time += p[idx].burst;
        p[idx].turnaround = p[idx].waiting + p[idx].burst;
        done[idx] = 1;
        completed++;
        cout << "P" << p[idx].pid << " ";
    }

    double avgWait = 0, avgTurn = 0;
    for (auto &pr : p) {
        avgWait += pr.waiting;
        avgTurn += pr.turnaround;
    }

    cout << "\nAverage Waiting Time: " << avgWait / n;
    cout << "\nAverage Turnaround Time: " << avgTurn / n << "\n";
}

// ---------- Round Robin ----------
void roundRobin(vector<Process> p, int quantum) {
    cout << "\n=== Round Robin Scheduling ===\n";
    queue<int> q;
    int time = 0, n = p.size(), completed = 0;

    for (auto &pr : p) pr.remaining = pr.burst;
    vector<int> inQueue(n, 0);

    while (completed < n) {
        for (int i = 0; i < n; i++)
            if (p[i].arrival <= time && !inQueue[i] && p[i].remaining > 0) {
                q.push(i);
                inQueue[i] = 1;
            }

        if (q.empty()) { time++; continue; }

        int idx = q.front(); q.pop();
        inQueue[idx] = 0;

        int exec = min(quantum, p[idx].remaining);
        p[idx].remaining -= exec;
        for (int t = 0; t < exec; t++)
            cout << "P" << p[idx].pid << " ";
        time += exec;

        if (p[idx].remaining == 0) {
            completed++;
            p[idx].turnaround = time - p[idx].arrival;
            p[idx].waiting = p[idx].turnaround - p[idx].burst;
        } else {
            for (int i = 0; i < n; i++)
                if (p[i].arrival <= time && !inQueue[i] && p[i].remaining > 0) {
                    q.push(i);
                    inQueue[i] = 1;
                }
            q.push(idx);
            inQueue[idx] = 1;
        }
    }

    double avgWait = 0, avgTurn = 0;
    for (auto &pr : p) {
        avgWait += pr.waiting;
        avgTurn += pr.turnaround;
    }

    cout << "\nAverage Waiting Time: " << avgWait / n;
    cout << "\nAverage Turnaround Time: " << avgTurn / n << "\n";
}

// ---------- MAIN ----------
int main() {
    int n;
    cout << "Enter number of processes: ";
    cin >> n;

    vector<Process> p(n);
    for (int i = 0; i < n; i++) {
        p[i].pid = i + 1;
        cout << "Enter Arrival, Burst, Priority for P" << i + 1 << ": ";
        cin >> p[i].arrival >> p[i].burst >> p[i].priority;
    }

    // Sort by arrival for fair start
    sort(p.begin(), p.end(), [](Process a, Process b) { return a.arrival < b.arrival; });

    fcfs(p);
    sjfPreemptive(p);
    priorityScheduling(p);
    roundRobin(p, 2);  // quantum = 2

    return 0;
}
