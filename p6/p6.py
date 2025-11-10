# Memory Placement Strategies Simulation
# Algorithms: First Fit, Next Fit, Best Fit, Worst Fit

def first_fit(blocks, processes):
    allocation = [-1] * len(processes)
    for i in range(len(processes)):
        for j in range(len(blocks)):
            if blocks[j] >= processes[i]:
                allocation[i] = j
                blocks[j] -= processes[i]
                break
    return allocation

def next_fit(blocks, processes):
    allocation = [-1] * len(processes)
    j = 0
    for i in range(len(processes)):
        count = 0
        while count < len(blocks):
            if blocks[j] >= processes[i]:
                allocation[i] = j
                blocks[j] -= processes[i]
                break
            j = (j + 1) % len(blocks)
            count += 1
    return allocation

def best_fit(blocks, processes):
    allocation = [-1] * len(processes)
    for i in range(len(processes)):
        best_idx = -1
        for j in range(len(blocks)):
            if blocks[j] >= processes[i]:
                if best_idx == -1 or blocks[j] < blocks[best_idx]:
                    best_idx = j
        if best_idx != -1:
            allocation[i] = best_idx
            blocks[best_idx] -= processes[i]
    return allocation

def worst_fit(blocks, processes):
    allocation = [-1] * len(processes)
    for i in range(len(processes)):
        worst_idx = -1
        for j in range(len(blocks)):
            if blocks[j] >= processes[i]:
                if worst_idx == -1 or blocks[j] > blocks[worst_idx]:
                    worst_idx = j
        if worst_idx != -1:
            allocation[i] = worst_idx
            blocks[worst_idx] -= processes[i]
    return allocation

def display_allocation(processes, allocation):
    print("Process No.\tProcess Size\tBlock No.")
    for i in range(len(processes)):
        if allocation[i] != -1:
            print(f"{i+1}\t\t{processes[i]}\t\t{allocation[i]+1}")
        else:
            print(f"{i+1}\t\t{processes[i]}\t\tNot Allocated")

if __name__ == "__main__":
    # Example input
    memory_blocks = [100, 500, 200, 300, 600]
    process_sizes = [212, 417, 112, 426]

    print("Memory Blocks:", memory_blocks)
    print("Processes:", process_sizes)

    # First Fit
    allocation = first_fit(memory_blocks.copy(), process_sizes)
    print("\n--- First Fit Allocation ---")
    display_allocation(process_sizes, allocation)

    # Next Fit
    allocation = next_fit(memory_blocks.copy(), process_sizes)
    print("\n--- Next Fit Allocation ---")
    display_allocation(process_sizes, allocation)

    # Best Fit
    allocation = best_fit(memory_blocks.copy(), process_sizes)
    print("\n--- Best Fit Allocation ---")
    display_allocation(process_sizes, allocation)

    # Worst Fit
    allocation = worst_fit(memory_blocks.copy(), process_sizes)
    print("\n--- Worst Fit Allocation ---")
    display_allocation(process_sizes, allocation)
