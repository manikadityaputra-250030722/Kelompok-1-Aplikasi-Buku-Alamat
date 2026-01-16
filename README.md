# Kelompok-1-Aplikasi-Buku-Alamat

1. Judul Project
Aplikasi Buku Alamat berbasis Web

2. Deskripsi Project
Aplikasi Buku Alamat berbasis Web adalah aplikasi web backend yang memungkinkan pengguna untuk menyimpan, mengelola, mencari, dan mengelompokkan kontak. Sistem menggunakan autentikasi JWT serta menyediakan endpoint CRUD untuk manajemen kontak.

3. Daftar Anggota
HENDRO PEKU WALI (240030394)
NI KADEK ARDELIA MEIZA (230030593)
LUH GEDE INDAH PURNAMA SARI (240030272)
I PUTU MANIK ADITYA PUTRA (250030722)

4. Lingkungan Pengembangan
4.1 Bahasa Pemrograman & Framework Backend
Python 3.x
Bahasa pemrograman yang digunakan untuk mengembangkan backend aplikasi.
FastAPI
Web framework Python modern untuk membangun REST API. Digunakan untuk
membuat endpoint autentikasi (register, login), manajemen kontak (CRUD), serta
fitur pencarian dan filter kategori kontak.
4.2 Server Aplikasi
Uvicorn
ASGI (Asynchronous Server Gateway Interface) server yang menjalankan aplikasi
FastAPI. Digunakan selama pengembangan dan demo aplikasi untuk
mendengarkan request dari frontend.
4.3 Database dan ORM
MySQL
Sistem manajemen basis data relasional (RDBMS) yang menyimpan data pengguna
dan daftar kontak secara persisten. Database ini diakses melalui koneksi TCP/IP
dengan konfigurasi host, user, password, dan nama database di file database.py.
SQLAlchemy
Object Relational Mapper (ORM) yang memungkinkan pendefinisian model data
(tabel User dan Contact) dalam bentuk class Python. ORM ini menangani proses
konversi antara tipe data Python dan tipe data SQL, serta mengelola operasi CRUD
ke database MySQL.
mysqlclient / PyMySQL
Driver atau connector yang menghubungkan Python (SQLAlchemy) ke MySQL.
Memungkinkan eksekusi query SQL dari kode Python.
4.4 Keamanan dan Autentikasi
Passlib (bcrypt)
Library untuk hashing password pengguna menggunakan algoritma bcrypt. Fungsi
ini menjamin password tidak disimpan dalam bentuk plain text di database,
melainkan dalam bentuk hash yang aman dan terverifikasi.
Python-Jose / PyJWT
Library untuk pembuatan (encoding) dan validasi (decoding) token JWT (JSON Web
Token). JWT digunakan sebagai mekanisme autentikasi: saat pengguna login
berhasil, sistem mengembalikan token yang disimpan di browser; setiap request ke
endpoint kontak harus menyertakan token ini di header Authorization: Bearer
<token> untuk memastikan pengguna terautentikasi dan hanya dapat mengakses
data kontaknya sendiri.
4.5 Frontend
HTML5
Markup language untuk mendefinisikan struktur halaman web, termasuk form
registrasi, form login, form input kontak baru, dan tabel daftar kontak yang
ditampilkan melalui folder static/.
CSS3
Stylesheet language untuk mengatur tampilan visual aplikasi: tema dark modern,
layout dashboard dengan sidebar, responsive design untuk berbagai ukuran layar
(desktop, tablet, mobile), serta efek visual seperti gradient button, card shadow, dan
hover effects.
JavaScript (Vanilla)
Bahasa scripting untuk menambahkan interaktivitas di sisi klien tanpa
menggunakan framework (React, Vue, Angular). JavaScript digunakan untuk:
Memanggil REST API FastAPI menggunakan fetch() API.
Mengelola token JWT: menyimpan ke localStorage, mengambil untuk header
request.
Menampilkan data kontak dari response API ke dalam tabel HTML secara
dinamis.
Mengimplementasikan fitur pencarian dan filter kategori kontak.
Menangani event dari form dan tombol (submit, click, change).
4.6 Version Control & Hosting Kode
Git
Version control system untuk mengelola perubahan kode secara terstruktur.
Memungkinkan tracking history, branching, dan kolaborasi tim.
GitHub
Platform hosting repository Git jarak jauh. Digunakan untuk menyimpan source
code project Buku Alamat dan memudahkan berbagi kode dengan dosen, teman,
atau tim pengembang.
4.7 Arsitektur Sistem
Aplikasi Buku Alamat menggunakan arsitektur three-tier:
a. Presentation Layer (Frontend)
HTML, CSS, dan JavaScript di folder static/ menyajikan antarmuka pengguna. Layer
ini berkomunikasi dengan backend melalui REST API menggunakan fetch().
b. Application Layer (Backend)
FastAPI di file app.py mengelola business logic: validasi input, autentikasi JWT,
operasi CRUD kontak, pencarian, dan filter. Layer ini menggunakan dependency
injection (contoh: get_current_user) untuk memastikan setiap request terproteksi
dan user hanya akses data miliknya.
c. Data Layer (Database)
MySQL menyimpan tabel User (username, email, password_hash) dan Contact
(name, phone, email, address, category, user_id). SQLAlchemy menjembatani antara
kode Python dan query SQL ke MySQL.

3. Proses Bisnis
1. Pengguna melakukan registrasi.
2. Pengguna login dan mendapatkan JWT token.
3. Pengguna dapat membuat, melihat, mengedit, menghapus kontak.
4. Pengguna dapat mencari atau mengelompokkan kontak.
5. Sistem menjaga session menggunakan JWT.


4. ERD
Tabel Users:
id (PK)
username
password_hash

Tabel Contacts:
id (PK)
user_id (FK → Users)
name
phone
email
address
category (opsional)
Relasi: Users 1..N Contacts

5. Struktur Detail Tabel Database


6. Hasil Pengembangan 
6.1 Autentikasi Pengguna
Registrasi: Pengguna baru dapat membuat akun dengan username, email, dan
password. Password di-hash menggunakan bcrypt sebelum disimpan ke database.
Login: Pengguna login dengan username dan password. Sistem memverifikasi
kredensial dan mengembalikan JWT token jika valid.
Proteksi Endpoint: Semua endpoint kontak dilindungi dengan dependency
get_current_user yang memvalidasi token JWT pada setiap request.
6.2 Manajemen Kontak (CRUD)
Create: Tambah kontak baru via form di frontend. Data dikirim ke endpoint POST
/contacts dengan token JWT di header.
Read: Lihat daftar kontak di tabel. Data diambil dari endpoint GET /contacts yang
menampilkan kontak milik user yang login.
Update: Edit data kontak yang sudah ada melalui endpoint PUT /contacts/{id} (fitur
opsional di UI).
Delete: Hapus kontak via tombol Hapus di tabel. Request dikirim ke endpoint
DELETE /contacts/{id}.
6.3 Pencarian & Filter
Pencarian Nama/Email/Alamat: User dapat mengetik kata kunci di field pencarian.
Frontend mengirim query parameter search=... ke backend, yang melakukan filter
menggunakan ilike() untuk case-insensitive matching di kolom name, email, dan
address.
Filter Kategori: User dapat memilih kategori (Keluarga, Teman, Kerja) dari
dropdown. Frontend mengirim query parameter category=... ke backend untuk
memfilter kontak berdasarkan kategori yang dipilih.
Reset Filter: Tombol Reset mengembalikan pencarian ke kondisi awal
(menampilkan semua kontak).

7. Struktur Folder
Kelompok-1-Aplikasi-Buku-Alamat/
├── app.py # File utama FastAPI, routing & endpoint
├── database.py # Konfigurasi koneksi MySQL & SessionLocal
├── models.py # Definisi model SQLAlchemy (User, Contact)
├── schemas.py # Validasi Pydantic (UserCreate, ContactCreate, dll)
├── auth.py # Fungsi hash password & JWT token
├── requirements.txt # Daftar library Python yang diperlukan
├── static/ # Folder frontend (HTML, CSS, JS)
│ ├── index.html # Halaman utama aplikasi
│ ├── styles.css # Stylesheet aplikasi
│ └── main.js # Logic interaktivitas frontend
├── images/ # Folder gambar
│ ├── ERD.png # gambar ERD aplikasi

8. Cara Instalasi dan Menjalankan Aplikasi
8.1 Prasyarat
Python 3.7 atau lebih tinggi.
MySQL Server sudah terinstall dan berjalan.
Database MySQL sudah dibuat (sesuai konfigurasi di database.py).
8.2 Langkah Instalasi & Menjalankan
8.2.1 Clone Repository
git clone https://github.com/manikadityaputra-250030722/Kelompok-1-Aplikasi-Buku-Alamat.git
cd buku-alamat-fastapi
8.2.2 Buat Virtual Environment (Opsionaltapi Disarankan)
Windows:
python -m venv venv
venv\Scripts\activate
Linux / macOS:
python -m venv venv
source venv/bin/activate
8.2.3 Install Dependensi Python
pip install -r requirements.txt
File requirements.txt berisi library yang diperlukan:
fastapi
uvicorn
sqlalchemy
mysql-connector-python
passlib[bcrypt]
python-jose[cryptography]
pydantic
8.2.4 Konfigurasi Database (Database.py)
Pastikan setting di database.py sesuai dengan konfigurasi MySQL kamu:
SQLALCHEMY_DATABASE_URL =
"mysql+mysqlconnector://username:password@localhost/buku_alamat"
Ganti username, password, dan nama database sesuai setup MySQL kamu.
8.2.5 Jalankan Server FastAPI
Mode biasa (localhost hanya untuk laptop sendiri):
uvicorn app:app --reload
Mode dengan akses dari HP/teman (satu jaringan Wi-Fi yang sama):
uvicorn app:app --reload --host 0.0.0.0 --port 8000
8.2.6 Akses Aplikasi
Dari laptop yang menjalankan server:
http://127.0.0.1:8000/
Dari perangkat lain (HP/laptop teman) di jaringan yang sama:
http://IP_LAPTOP:8000/
Cari IP laptop dengan perintah:
Windows: ipconfig (lihat IPv4 Address)
Linux/macOS: ifconfig atau hostname -I









