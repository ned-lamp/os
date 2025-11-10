#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

// FIFO
int fifo(const vector<int>& pages, int capacity) {
    vector<int> frame;
    int faults = 0;

    for (int page : pages) {
        if (find(frame.begin(), frame.end(), page) == frame.end()) {
            if (frame.size() < capacity)
                frame.push_back(page);
            else {
                frame.erase(frame.begin()); // remove oldest
                frame.push_back(page);
            }
            faults++;
        }
        cout << "Page " << page << " -> ";
        for (int f : frame) cout << f << " ";
        cout << endl;
    }
    return faults;
}

// LRU
int lru(const vector<int>& pages, int capacity) {
    vector<int> frame, recent;
    int faults = 0;

    for (int page : pages) {
        auto it = find(frame.begin(), frame.end(), page);
        if (it == frame.end()) { // not found
            if (frame.size() < capacity)
                frame.push_back(page);
            else {
                int lru_page = recent.front();
                recent.erase(recent.begin());
                frame.erase(remove(frame.begin(), frame.end(), lru_page), frame.end());
                frame.push_back(page);
            }
            faults++;
        } else {
            // page already in frame → move it to most recent
            recent.erase(remove(recent.begin(), recent.end(), page), recent.end());
        }
        recent.push_back(page);

        cout << "Page " << page << " -> ";
        for (int f : frame) cout << f << " ";
        cout << endl;
    }
    return faults;
}

// Optimal
int optimal(const vector<int>& pages, int capacity) {
    vector<int> frame;
    int faults = 0;

    for (size_t i = 0; i < pages.size(); ++i) {
        int page = pages[i];
        if (find(frame.begin(), frame.end(), page) == frame.end()) {
            if (frame.size() < capacity)
                frame.push_back(page);
            else {
                int farthest = -1, replace_idx = -1;
                for (size_t j = 0; j < frame.size(); ++j) {
                    auto it = find(pages.begin() + i + 1, pages.end(), frame[j]);
                    int next_use = (it == pages.end()) ? pages.size() : distance(pages.begin(), it);
                    if (next_use > farthest) {
                        farthest = next_use;
                        replace_idx = j;
                    }
                }
                frame[replace_idx] = page;
            }
            faults++;
        }
        cout << "Page " << page << " -> ";
        for (int f : frame) cout << f << "";
        cout << endl;
    }
    return faults;
}

// Main
int main() {
    vector<int> pages = {7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2};
    int capacity = 3;

    cout << "Page Reference String: ";
    for (int p : pages) cout << p << " ";
    cout << "\nFrame Capacity: " << capacity << "\n\n";

    cout << "--- FIFO Page Replacement ---\n";
    cout << "Total Page Faults: " << fifo(pages, capacity) << "\n\n";

    cout << "--- LRU Page Replacement ---\n";
    cout << "Total Page Faults: " << lru(pages, capacity) << "\n\n";

    cout << "--- Optimal Page Replacement ---\n";
    cout << "Total Page Faults: " << optimal(pages, capacity) << "\n";

    return 0;
}
