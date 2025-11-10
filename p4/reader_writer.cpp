#include <iostream>
#include <thread>
#include <mutex>
#include <semaphore.h>
#include <chrono>

using namespace std;

int readCount = 0;
mutex mtx;
sem_t wrt;
int sharedData = 0;

void reader(int id) {
    while (true) {
        mtx.lock();
        readCount++;
        if (readCount == 1)
            sem_wait(&wrt); // first reader locks writer
        mtx.unlock();

        cout << "Reader " << id << " reads data = " << sharedData << endl;
        this_thread::sleep_for(chrono::milliseconds(200));

        mtx.lock();
        readCount--;
        if (readCount == 0)
            sem_post(&wrt); // last reader unlocks writer
        mtx.unlock();

        this_thread::sleep_for(chrono::milliseconds(400));
    }
}

void writer(int id) {
    while (true) {
        sem_wait(&wrt);
        sharedData++;
        cout << "Writer " << id << " writes data = " << sharedData << endl;
        sem_post(&wrt);
        this_thread::sleep_for(chrono::milliseconds(500));
    }
}

int main() {
    sem_init(&wrt, 0, 1);

    thread r1(reader, 1);
    thread r2(reader, 2);
    thread w1(writer, 1);

    this_thread::sleep_for(chrono::seconds(3));

    cout << "Stopping simulation." << endl;
    return 0;
}
