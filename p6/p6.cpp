#include <iostream>
#include <vector>
#include <iomanip>
using namespace std;

// ---------- First Fit ----------
vector<int> first_fit(vector<int> blocks, const vector<int>& processes) {
    vector<int> allocation(processes.size(), -1);
    for (size_t i = 0; i < processes.size(); ++i) {
        for (size_t j = 0; j < blocks.size(); ++j) {
            if (blocks[j] >= processes[i]) {
                allocation[i] = j;
                blocks[j] -= processes[i];
                break;
            }
        }
    }
    return allocation;
}

// ---------- Next Fit ----------
vector<int> next_fit(vector<int> blocks, const vector<int>& processes) {
    vector<int> allocation(processes.size(), -1);
    size_t j = 0;
    for (size_t i = 0; i < processes.size(); ++i) {
        size_t count = 0;
        while (count < blocks.size()) {
            if (blocks[j] >= processes[i]) {
                allocation[i] = j;
                blocks[j] -= processes[i];
                break;
            }
            j = (j + 1) % blocks.size();
            count++;
        }
    }
    return allocation;
}

// ---------- Best Fit ----------
vector<int> best_fit(vector<int> blocks, const vector<int>& processes) {
    vector<int> allocation(processes.size(), -1);
    for (size_t i = 0; i < processes.size(); ++i) {
        int best_idx = -1;
        for (size_t j = 0; j < blocks.size(); ++j) {
            if (blocks[j] >= processes[i]) {
                if (best_idx == -1 || blocks[j] < blocks[best_idx])
                    best_idx = j;
            }
        }
        if (best_idx != -1) {
            allocation[i] = best_idx;
            blocks[best_idx] -= processes[i];
        }
    }
    return allocation;
}

// ---------- Worst Fit ----------
vector<int> worst_fit(vector<int> blocks, const vector<int>& processes) {
    vector<int> allocation(processes.size(), -1);
    for (size_t i = 0; i < processes.size(); ++i) {
        int worst_idx = -1;
        for (size_t j = 0; j < blocks.size(); ++j) {
            if (blocks[j] >= processes[i]) {
                if (worst_idx == -1 || blocks[j] > blocks[worst_idx])
                    worst_idx = j;
            }
        }
        if (worst_idx != -1) {
            allocation[i] = worst_idx;
            blocks[worst_idx] -= processes[i];
        }
    }
    return allocation;
}

// ---------- Display Function ----------
void display_allocation(const vector<int>& processes, const vector<int>& allocation) {
    cout << left << setw(12) << "Process No."
         << setw(15) << "Process Size"
         << "Block No." << endl;

    for (size_t i = 0; i < processes.size(); ++i) {
        cout << setw(12) << i + 1
             << setw(15) << processes[i];
        if (allocation[i] != -1)
            cout << allocation[i] + 1 << endl;
        else
            cout << "Not Allocated" << endl;
    }
}

int main() {
    vector<int> memory_blocks = {100, 500, 200, 300, 600};
    vector<int> process_sizes = {212, 417, 112, 426};

    cout << "Memory Blocks: ";
    for (int b : memory_blocks) cout << b << " ";
    cout << "\nProcesses: ";
    for (int p : process_sizes) cout << p << " ";
    cout << "\n";

    // First Fit
    cout << "\n--- First Fit Allocation ---\n";
    auto alloc = first_fit(memory_blocks, process_sizes);
    display_allocation(process_sizes, alloc);

    // Next Fit
    cout << "\n--- Next Fit Allocation ---\n";
    alloc = next_fit(memory_blocks, process_sizes);
    display_allocation(process_sizes, alloc);

    // Best Fit
    cout << "\n--- Best Fit Allocation ---\n";
    alloc = best_fit(memory_blocks, process_sizes);
    display_allocation(process_sizes, alloc);

    // Worst Fit
    cout << "\n--- Worst Fit Allocation ---\n";
    alloc = worst_fit(memory_blocks, process_sizes);
    display_allocation(process_sizes, alloc);

    return 0;
}
