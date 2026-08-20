# Django
Environment berbeda: Container memiliki sistem operasi dan dependensi minimal. Library Python yang terinstall di lokal belum tentu ada di container.
Database SQLite: File db.sqlite3 yang ada di lokal tidak ikut terbawa (atau terbawa tapi path-nya berbeda). Container menggunakan filesystem terpisah.
Port binding: runserver default bind ke 127.0.0.1 (localhost) yang hanya bisa diakses dari dalam container. Perlu diubah ke 0.0.0.0 agar bisa diakses dari host.
Environment variables: File .env atau setting lokal mungkin tidak terbaca di container.
Python version: Versi Python di lokal dan container bisa berbeda, menyebabkan incompatibility.