# 📦 Latihan Bab 8 — Queue & Simulasi Antrian Tiket

> Implementasi lengkap latihan Bab 8 menggunakan Python 3.
> Topik: **Queue ADT**, **Linked List Queue**, dan **Simulasi Antrian Loket Tiket**.

---

## 📁 Struktur File

```
.
└── latihan_bab8_lengkap.py   # Semua soal (1–6) dalam satu file
```

Tidak ada dependensi eksternal. Cukup Python 3 bawaan.

---

## 🚀 Cara Menjalankan

```bash
python latihan_bab8_lengkap.py
```

Output semua soal akan langsung tampil di terminal secara berurutan.

---

## 📝 Ringkasan Soal & Jawaban

### Soal 1 — Kompleksitas Waktu Worst Case `TicketCounterSimulation`

| Metode | Kompleksitas | Alasan |
|---|---|---|
| `__init__` | O(n) | Loop n kali mengisi array agent |
| `run` | O(m × n) | m menit × n agent per handler |
| `_handleArrival` | O(1) | Random check + enqueue O(1) |
| `_handleBeginService` | O(n) | Iterasi semua n agent |
| `_handleEndService` | O(n) | Iterasi semua n agent |
| `printResults` | O(1) | Hitung dan cetak saja |

> `n` = numAgents, `m` = numMinutes

---

### Soal 2 — Eksekusi Manual Queue (enqueue saja)

```python
values = Queue()
for i in range(16):
    if i % 3 == 0:
        values.enqueue(i)
```

**Hasil akhir queue (front → rear):**

```
[0, 3, 6, 9, 12, 15]
```

`i` yang memenuhi `i % 3 == 0` dari `range(16)` adalah: 0, 3, 6, 9, 12, 15.

---

### Soal 3 — Eksekusi Manual Queue (enqueue + dequeue)

```python
values = Queue()
for i in range(16):
    if i % 3 == 0:
        values.enqueue(i)
    elif i % 4 == 0:
        values.dequeue()
```

**Trace eksekusi:**

| i | Kondisi | Aksi | Queue (front→rear) |
|---|---|---|---|
| 0 | i%3==0 | enqueue(0) | [0] |
| 3 | i%3==0 | enqueue(3) | [0, 3] |
| 4 | i%4==0 | dequeue() → 0 | [3] |
| 6 | i%3==0 | enqueue(6) | [3, 6] |
| 8 | i%4==0 | dequeue() → 3 | [6] |
| 9 | i%3==0 | enqueue(9) | [6, 9] |
| 12 | i%3==0 | enqueue(12) | [6, 9, 12] |
| 15 | i%3==0 | enqueue(15) | [6, 9, 12, 15] |

> ⚠️ `i=12`: memenuhi `i%3==0` **dan** `i%4==0`, tetapi kondisi `if` diutamakan → **enqueue**, bukan dequeue.

**Hasil akhir queue (front → rear):**

```
[6, 9, 12, 15]
```

---

### Soal 4 — Implementasi Metode `TicketCounterSimulation`

Tiga metode yang diimplementasikan:

#### `_handleArrival(cur_time)` — O(1)
Penumpang tiba secara acak berdasarkan probabilitas `1/between_time` per menit.

```python
def _handleArrival(self, cur_time):
    if random.random() <= self._arrive_prob:
        self._passenger_q.enqueue(Passenger(cur_time))
        self._num_passengers += 1
```

#### `_handleBeginService(cur_time)` — O(n)
Agent yang bebas mengambil penumpang dari depan antrian dan mulai melayani.

```python
def _handleBeginService(self, cur_time):
    for agent in self._the_agents:
        if agent.isFree() and not self._passenger_q.isEmpty():
            p = self._passenger_q.dequeue()
            agent.startService(p, cur_time + self._service_time)
            self._total_wait_time += cur_time - p.arrivalTime()
```

#### `_handleEndService(cur_time)` — O(n)
Agent yang sudah selesai melayani dikembalikan ke status bebas.

```python
def _handleEndService(self, cur_time):
    for agent in self._the_agents:
        if agent.isFinished(cur_time):
            agent.stopService()
```

**Contoh output (100 menit):**

```
agents=2, service=3, between=2
  Passengers served         : 46
  Passengers remaining      : 0
  Average wait time (menit) : 1.39

agents=2, service=4, between=2
  Passengers served         : 41
  Passengers remaining      : 14
  Average wait time (menit) : 16.39

agents=3, service=4, between=2
  Passengers served         : 44
  Passengers remaining      : 0
  Average wait time (menit) : 0.39
```

---

### Soal 5 — Modifikasi ke Satuan Detik + Tabel Eksperimen

Kelas `TicketCounterSimulationSeconds` mewarisi `TicketCounterSimulation` dengan parameter dalam **satuan detik** (bukan menit).

**Tabel 8.1 — Hasil Eksperimen (satuan detik):**

| Num Sec | Agents | Between | Service | Avg Wait | Served | Remain |
|---:|---:|---:|---:|---:|---:|---:|
| 6000 | 2 | 120 | 180 | 50.20 | 51 | 0 |
| 30000 | 2 | 120 | 180 | 128.38 | 259 | 0 |
| 60000 | 2 | 120 | 180 | 79.85 | 481 | 3 |
| 6000 | 2 | 120 | 240 | 171.75 | 44 | 2 |
| 30000 | 2 | 120 | 240 | 230.32 | 212 | 2 |
| 60000 | 2 | 120 | 240 | 1782.48 | 498 | 18 |
| 6000 | 3 | 120 | 240 | 47.13 | 47 | 4 |
| 30000 | 3 | 120 | 240 | 89.26 | 257 | 0 |
| 60000 | 3 | 120 | 240 | 93.88 | 564 | 0 |

**Kesimpulan:**
- Saat `service_time > between_time` dengan hanya 2 agent, rata-rata tunggu meledak hingga **1782 detik**.
- Menambah 1 agent (menjadi 3) menurunkan rata-rata tunggu ke **~94 detik** — penurunan hingga 95%.

---

### Soal 6 — Fungsi `reverseQueue`

Membalik urutan item dalam queue **hanya menggunakan operasi Queue ADT**, dengan stack Python `list` sebagai struktur bantu.

```python
def reverseQueue(queue):
    stack = []
    while not queue.isEmpty():   # O(n): pindah queue → stack
        stack.append(queue.dequeue())
    while stack:                 # O(n): pindah stack → queue (terbalik)
        queue.enqueue(stack.pop())
    return queue
```

**Contoh:**

```
Sebelum : [10, 20, 30, 40, 50]  (front → rear)
Sesudah : [50, 40, 30, 20, 10]  (front → rear)
```

**Kompleksitas:** O(n) waktu · O(n) ruang tambahan

---

## 🏗️ Struktur Kelas

```
Queue               ← linked list, enqueue/dequeue O(1)
Array               ← wrapper list Python
TicketAgent         ← representasi satu loket
Passenger           ← representasi satu penumpang
TicketCounterSimulation         ← simulasi satuan menit
  └── TicketCounterSimulationSeconds  ← override ke satuan detik
```

---

## 🐍 Persyaratan

- Python **3.6+**
- Tidak ada library eksternal

---

## 👤 Informasi

| | |
|---|---|
| **Mata Kuliah** | Struktur Data |
| **Bab** | 8 — Queue |
| **Bahasa** | Python 3 |
