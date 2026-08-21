# Django
1. Environment berbeda: Container memiliki sistem operasi dan dependensi minimal. Library Python yang terinstall di lokal belum tentu ada di container.

2. Database SQLite: File db.sqlite3 yang ada di lokal tidak ikut terbawa (atau terbawa tapi path-nya berbeda). Container menggunakan filesystem terpisah.

3. Static files: Django development server otomatis serve static files. Di container, konfigurasi STATIC_ROOT dan collectstatic mungkin perlu diatur.

4. Port binding: runserver default bind ke 127.0.0.1 (localhost) yang hanya bisa diakses dari dalam container. Perlu diubah ke 0.0.0.0 agar bisa diakses dari host.

5. Environment variables: File .env atau setting lokal mungkin tidak terbaca di container.

6. Python version: Versi Python di lokal dan container bisa berbeda, menyebabkan incompatibility.

## Soal 5 - Query Analysis & Optimization

### Endpoint
- `/api/courses/list-unoptimized/` — Versi A (tanpa optimasi)
- `/api/courses/list-optimized/` — Versi B (dengan `prefetch_related`)

### Perbandingan Query (20 Course, 100 Lesson)

| Versi | Jumlah Query | Teknik |
|---|---|---|
| A | 21 | QuerySet biasa (N+1) |
| B | 2 | `prefetch_related('lessons')` |

### Mengapa N+1 Query Berbahaya?
N+1 query mengirim 1 query tambahan untuk setiap item yang di-loop. 
Jika ada 1.000 course, total query menjadi 1.001 kali. 
Ini menyebabkan latency tinggi, database overload, dan performa buruk saat data besar.
Solusinya adalah `prefetch_related()` atau `select_related()` sesuai jenis relasi.