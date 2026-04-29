"""
=============================================================
  Latihan Bab 8 — SEMUA SOAL DALAM SATU FILE
  Soal 1: Kompleksitas waktu (komentar di setiap metode)
  Soal 2: Eksekusi manual queue (enqueue saja)
  Soal 3: Eksekusi manual queue (enqueue + dequeue)
  Soal 4: Implementasi _handleArrival, _handleBeginService,
           _handleEndService
  Soal 5: Versi detik + tabel eksperimen
  Soal 6: Fungsi reverseQueue
=============================================================
"""

import random


# ─────────────────────────────────────────────────────────────
# Struktur data pendukung (Queue, Array, TicketAgent, Passenger)
# ─────────────────────────────────────────────────────────────

class _QueueNode:
    def __init__(self, item):
        self.item = item
        self.next = None


class Queue:
    """Queue berbasis linked list — enqueue/dequeue O(1)."""

    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0

    def isEmpty(self):
        return self._size == 0

    def __len__(self):
        return self._size

    def enqueue(self, item):           # O(1)
        node = _QueueNode(item)
        if self._tail is None:
            self._head = node
            self._tail = node
        else:
            self._tail.next = node
            self._tail = node
        self._size += 1

    def dequeue(self):                 # O(1)
        assert not self.isEmpty(), "Cannot dequeue from empty queue"
        item = self._head.item
        self._head = self._head.next
        if self._head is None:
            self._tail = None
        self._size -= 1
        return item

    def peek(self):
        assert not self.isEmpty(), "Cannot peek empty queue"
        return self._head.item


class Array:
    """Array sederhana berbasis Python list."""

    def __init__(self, size):
        self._data = [None] * size
        self._size = size

    def __getitem__(self, index):
        return self._data[index]

    def __setitem__(self, index, value):
        self._data[index] = value

    def __len__(self):
        return self._size

    def __iter__(self):
        return iter(self._data)


class TicketAgent:
    """Representasi satu loket tiket."""

    def __init__(self, agent_id):
        self._id = agent_id
        self._passenger = None
        self._finish_time = 0

    def isFree(self):
        return self._passenger is None

    def isFinished(self, cur_time):
        return self._passenger is not None and self._finish_time == cur_time

    def startService(self, passenger, finish_time):
        self._passenger = passenger
        self._finish_time = finish_time

    def stopService(self):
        passenger = self._passenger
        self._passenger = None
        return passenger


class Passenger:
    """Representasi satu penumpang."""

    def __init__(self, arrival_time):
        self._arrival_time = arrival_time

    def arrivalTime(self):
        return self._arrival_time


# ─────────────────────────────────────────────────────────────
# SOAL 4 — Implementasi lengkap TicketCounterSimulation (MENIT)
# ─────────────────────────────────────────────────────────────
#
# SOAL 1 — Kompleksitas waktu (worst case):
#
#   __init__         : O(n)     — loop n kali isi array agent
#   run              : O(m * n) — m menit x n agent per handler
#   _handleArrival   : O(1)     — random check + enqueue O(1)
#   _handleBeginService: O(n)   — iterasi semua n agent
#   _handleEndService: O(n)     — iterasi semua n agent
#   printResults     : O(1)     — hitung + cetak saja
#
#   n = numAgents, m = numMinutes
# ─────────────────────────────────────────────────────────────

class TicketCounterSimulation:
    """Simulasi antrian loket tiket (satuan MENIT)."""

    def __init__(self, num_agents, num_minutes, between_time, service_time):
        # O(n) — inisialisasi n agent
        self._arrive_prob  = 1.0 / between_time
        self._service_time = service_time
        self._num_minutes  = num_minutes

        self._passenger_q = Queue()
        self._the_agents  = Array(num_agents)
        for i in range(num_agents):
            self._the_agents[i] = TicketAgent(i + 1)

        self._total_wait_time = 0
        self._num_passengers  = 0

    def run(self):
        # O(m * n)
        for cur_time in range(self._num_minutes + 1):
            self._handleArrival(cur_time)
            self._handleBeginService(cur_time)
            self._handleEndService(cur_time)

    # ── SOAL 4: tiga metode di bawah ini adalah yang diimplementasikan ──

    def _handleArrival(self, cur_time):
        """
        Aturan #1: penumpang tiba secara acak tiap menit.
        Kompleksitas: O(1)
        """
        if random.random() <= self._arrive_prob:
            passenger = Passenger(cur_time)
            self._passenger_q.enqueue(passenger)
            self._num_passengers += 1

    def _handleBeginService(self, cur_time):
        """
        Aturan #2: agent bebas mengambil penumpang dari depan antrian.
        Kompleksitas: O(n) — cek setiap agent
        """
        for agent in self._the_agents:
            if agent.isFree() and not self._passenger_q.isEmpty():
                passenger  = self._passenger_q.dequeue()
                finish_time = cur_time + self._service_time
                agent.startService(passenger, finish_time)
                self._total_wait_time += cur_time - passenger.arrivalTime()

    def _handleEndService(self, cur_time):
        """
        Aturan #3: agent yang selesai melayani kembali bebas.
        Kompleksitas: O(n) — cek setiap agent
        """
        for agent in self._the_agents:
            if agent.isFinished(cur_time):
                agent.stopService()

    def printResults(self):
        # O(1)
        num_served = self._num_passengers - len(self._passenger_q)
        avg_wait   = float(self._total_wait_time) / num_served if num_served else 0.0
        print(f"  Passengers served         : {num_served}")
        print(f"  Passengers remaining      : {len(self._passenger_q)}")
        print(f"  Average wait time (menit) : {avg_wait:.2f}")
        return num_served, len(self._passenger_q), avg_wait


# ─────────────────────────────────────────────────────────────
# SOAL 5 — Modifikasi ke satuan DETIK + tabel eksperimen
# ─────────────────────────────────────────────────────────────

class TicketCounterSimulationSeconds(TicketCounterSimulation):
    """
    Versi detik dari TicketCounterSimulation.
    Parameter between_time dan service_time kini dalam satuan detik.
    Logika identik — hanya unit yang berubah.
    """

    def __init__(self, num_agents, num_seconds, between_sec, service_sec):
        super().__init__(num_agents, num_seconds, between_sec, service_sec)

    def getResults(self):
        num_served = self._num_passengers - len(self._passenger_q)
        avg_wait   = float(self._total_wait_time) / num_served if num_served else 0.0
        return num_served, len(self._passenger_q), avg_wait


def runExperimentTable():
    """Jalankan berbagai kombinasi parameter dan cetak tabel (satuan detik)."""
    random.seed(42)

    # (num_seconds, num_agents, between_sec, service_sec)
    configs = [
        (6000,  2, 120, 180),
        (30000, 2, 120, 180),
        (60000, 2, 120, 180),
        (6000,  2, 120, 240),
        (30000, 2, 120, 240),
        (60000, 2, 120, 240),
        (6000,  3, 120, 240),
        (30000, 3, 120, 240),
        (60000, 3, 120, 240),
    ]

    W = 72
    print("=" * W)
    print("  TABLE 8.1 — Ticket Counter Simulation (satuan DETIK)")
    print("=" * W)
    print(f"{'Num Sec':>9} {'Agents':>6} {'Between':>8} {'Service':>8}"
          f" {'AvgWait':>9} {'Served':>7} {'Remain':>7}")
    print("-" * W)

    for ns, ag, bt, sv in configs:
        sim = TicketCounterSimulationSeconds(ag, ns, bt, sv)
        sim.run()
        served, rem, avg = sim.getResults()
        print(f"{ns:>9} {ag:>6} {bt:>8} {sv:>8}"
              f" {avg:>9.2f} {served:>7} {rem:>7}")

    print("=" * W)
    print("  Kesimpulan:")
    print("    - service > between + sedikit agent → antrian membengkak")
    print("    - Tambah 1 agent (3 total) → avg wait turun drastis")


# ─────────────────────────────────────────────────────────────
# SOAL 6 — Fungsi reverseQueue
# ─────────────────────────────────────────────────────────────

def reverseQueue(queue):
    """
    Membalik urutan item dalam queue.
    Hanya menggunakan operasi Queue ADT + stack Python (list) sebagai
    struktur bantu.

    Algoritma:
      1. Dequeue semua item ke stack  → O(n)
      2. Pop stack, enqueue kembali   → O(n)
    Total: O(n) waktu, O(n) ruang tambahan.
    """
    stack = []

    # Langkah 1: pindahkan queue → stack (urutan terbalik di stack)
    while not queue.isEmpty():
        stack.append(queue.dequeue())

    # Langkah 2: pindahkan stack → queue (urutan kembali, tapi terbalik)
    while stack:
        queue.enqueue(stack.pop())

    return queue


# ─────────────────────────────────────────────────────────────
# MAIN — demonstrasi semua soal
# ─────────────────────────────────────────────────────────────

def demo_soal2():
    """
    SOAL 2 — Eksekusi manual:
        values = Queue()
        for i in range(16):
            if i % 3 == 0:
                values.enqueue(i)
    """
    values = Queue()
    for i in range(16):
        if i % 3 == 0:
            values.enqueue(i)

    result = []
    tmp = Queue()
    while not values.isEmpty():
        x = values.dequeue()
        result.append(x)
        tmp.enqueue(x)

    print(f"  Queue akhir (front→rear): {result}")
    print("  Penjelasan: i yang memenuhi i%3==0 dari range(16):")
    print("    i=0,3,6,9,12,15 → semuanya dienqueue")


def demo_soal3():
    """
    SOAL 3 — Eksekusi manual:
        values = Queue()
        for i in range(16):
            if i % 3 == 0:
                values.enqueue(i)
            elif i % 4 == 0:
                values.dequeue()
    """
    values = Queue()
    log = []
    for i in range(16):
        if i % 3 == 0:
            values.enqueue(i)
            log.append(f"i={i:2d}: enqueue({i})")
        elif i % 4 == 0:
            if not values.isEmpty():
                out = values.dequeue()
                log.append(f"i={i:2d}: dequeue() → {out}")

    for line in log:
        print(f"    {line}")

    result = []
    while not values.isEmpty():
        result.append(values.dequeue())
    print(f"  Queue akhir (front→rear): {result}")
    print("  Catatan: i=12 masuk ke if (i%3==0), bukan elif, jadi enqueue bukan dequeue.")


if __name__ == "__main__":
    SEP = "=" * 55

    # ── Soal 2 ──
    print(SEP)
    print("SOAL 2 — Eksekusi Manual Queue (enqueue saja)")
    print(SEP)
    demo_soal2()

    # ── Soal 3 ──
    print()
    print(SEP)
    print("SOAL 3 — Eksekusi Manual Queue (enqueue + dequeue)")
    print(SEP)
    demo_soal3()

    # ── Soal 4 ──
    print()
    print(SEP)
    print("SOAL 4 — Simulasi Loket Tiket (satuan MENIT)")
    print(SEP)
    random.seed(123)
    params = [
        (2, 3, "agents=2, service=3, between=2, 100 menit"),
        (2, 4, "agents=2, service=4, between=2, 100 menit"),
        (3, 4, "agents=3, service=4, between=2, 100 menit"),
    ]
    for ag, sv, desc in params:
        print(f"\n  {desc}")
        sim = TicketCounterSimulation(ag, 100, 2, sv)
        sim.run()
        sim.printResults()

    # ── Soal 5 ──
    print()
    runExperimentTable()

    # ── Soal 6 ──
    print()
    print(SEP)
    print("SOAL 6 — Fungsi reverseQueue")
    print(SEP)
    q = Queue()
    items = [10, 20, 30, 40, 50]
    for v in items:
        q.enqueue(v)
    print(f"  Sebelum dibalik (front→rear): {items}")
    reverseQueue(q)
    hasil = []
    while not q.isEmpty():
        hasil.append(q.dequeue())
    print(f"  Sesudah dibalik (front→rear): {hasil}")
    print("  Kompleksitas: O(n) waktu, O(n) ruang")