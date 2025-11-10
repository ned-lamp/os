# Page Replacement Algorithm Simulation
# FIFO, LRU, and Optimal

def fifo(pages, capacity):
    frame = []
    page_faults = 0

    for page in pages:
        if page not in frame:
            if len(frame) < capacity:
                frame.append(page)
            else:
                frame.pop(0)
                frame.append(page)
            page_faults += 1
        print(f"Page {page} -> Frames: {frame}")
    return page_faults

def lru(pages, capacity):
    frame = []
    page_faults = 0
    recent = []

    for page in pages:
        if page not in frame:
            if len(frame) < capacity:
                frame.append(page)
            else:
                # Remove least recently used page
                lru_page = recent.pop(0)
                frame.remove(lru_page)
                frame.append(page)
            page_faults += 1
        else:
            recent.remove(page)
        recent.append(page)
        print(f"Page {page} -> Frames: {frame}")
    return page_faults

def optimal(pages, capacity):
    frame = []
    page_faults = 0

    for i in range(len(pages)):
        page = pages[i]
        if page not in frame:
            if len(frame) < capacity:
                frame.append(page)
            else:
                # Predict which page won’t be used for the longest time
                farthest_index = -1
                page_to_remove = None
                for f in frame:
                    if f not in pages[i+1:]:
                        page_to_remove = f
                        break
                    else:
                        next_use = pages[i+1:].index(f)
                        if next_use > farthest_index:
                            farthest_index = next_use
                            page_to_remove = f
                frame.remove(page_to_remove)
                frame.append(page)
            page_faults += 1
        print(f"Page {page} -> Frames: {frame}")
    return page_faults

def main():
    pages = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2]
    capacity = 3

    print("Page Reference String:", pages)
    print("Frame Capacity:", capacity)

    print("\n--- FIFO Page Replacement ---")
    faults = fifo(pages, capacity)
    print(f"Total Page Faults (FIFO): {faults}\n")

    print("--- LRU Page Replacement ---")
    faults = lru(pages, capacity)
    print(f"Total Page Faults (LRU): {faults}\n")

    print("--- Optimal Page Replacement ---")
    faults = optimal(pages, capacity)
    print(f"Total Page Faults (Optimal): {faults}\n")

if __name__ == "__main__":
    main()
