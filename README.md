# **Kelompok-1-Aplikasi-Buku-Alamat**

## 1. Judul Project
**Aplikasi Buku Alamat berbasis Web**

---

## 2. Deskripsi Project
Aplikasi Buku Alamat berbasis Web adalah aplikasi backend yang memungkinkan pengguna untuk menyimpan, mengelola, mencari, dan mengelompokkan kontak. Sistem menggunakan autentikasi **JWT** serta menyediakan endpoint **CRUD** untuk manajemen kontak.

---

## 3. Daftar Anggota
- **HENDRO PEKU WALI (240030394)**
- **NI KADEK ARDELIA MEIZA (230030593)**
- **LUH GEDE INDAH PURNAMA SARI (240030272)**
- **I PUTU MANIK ADITYA PUTRA (250030722)**

---

## 4. Lingkungan Pengembangan

### **4.1 Bahasa Pemrograman & Framework Backend**
- **Python 3.x**  
- **FastAPI**

### **4.2 Server Aplikasi**
- **Uvicorn**

### **4.3 Database dan ORM**
- **MySQL**  
- **SQLAlchemy**  
- **mysqlclient / PyMySQL**

### **4.4 Keamanan dan Autentikasi**
- **Passlib (bcrypt)**  
- **Python-Jose / PyJWT**

### **4.5 Frontend**
- **HTML5**  
- **CSS3**  
- **JavaScript (Vanilla)**  

### **4.6 Version Control & Hosting Kode**
- **Git**  
- **GitHub**

### **4.7 Arsitektur Sistem**
Aplikasi menggunakan arsitektur **Three-tier**:

#### a. Presentation Layer (Frontend)
Menggunakan HTML, CSS, JavaScript.

#### b. Application Layer (Backend)
Menggunakan FastAPI.

#### c. Data Layer (Database)
Menggunakan MySQL + SQLAlchemy.

---

## 5. Proses Bisnis
a. Registrasi pengguna  
b. Login dan mendapatkan JWT  
c. CRUD kontak  
d. Pencarian dan pengelompokan kontak  
e. Session dijaga menggunakan JWT  

---

## 6. ERD

### **Tabel Users**
- id (PK)  
- username
- email  
- password_hash
- created_at

### **Tabel Contacts**
- id (PK)  
- user_id (FK → Users)  
- name  
- phone  
- email  
- address  
- category
- created_at

**Relasi:** Users **1..N** Contacts

![Entity Relationship Diagram](images/ERD.png)

---

## 7. Struktur Detail Tabel Database

## Tabel: `users`

| Nama Kolom     | Tipe Data                | Keterangan                      |
|----------------|---------------------------|----------------------------------|
| id             | INTEGER                   | Primary Key, Auto Increment      |
| username       | VARCHAR(50)               | Unique, Not Null                 |
| email          | VARCHAR(100)              | Unique, Not Null                 |
| password_hash  | VARCHAR(255)              | Not Null                         |
| created_at     | TIMESTAMP (TZ)            | Default: CURRENT_TIMESTAMP       |

---

## Tabel: `contacts`

| Nama Kolom | Tipe Data         | Keterangan                                    |
|------------|--------------------|-----------------------------------------------|
| id         | INTEGER            | Primary Key, Auto Increment                    |
| user_id    | INTEGER            | Foreign Key → users.id, Not Null               |
| name       | VARCHAR(100)       | Not Null                                      |
| phone      | VARCHAR(50)        | Opsional                                       |
| email      | VARCHAR(100)       | Opsional                                       |
| address    | TEXT               | Opsional                                       |
| category   | VARCHAR(50)        | Opsional                                       |
| created_at | TIMESTAMP (TZ)     | Default: CURRENT_TIMESTAMP                    |

---

## 8. Hasil Pengembangan

### **8.1 Autentikasi Pengguna**
- Registrasi dengan hashing bcrypt  
- Login menggunakan JWT  
- Proteksi endpoint dengan `get_current_user`  

### **8.2 Manajemen Kontak (CRUD)**
- Create: POST /contacts  
- Read: GET /contacts  
- Update: PUT /contacts/{id}  
- Delete: DELETE /contacts/{id}  

### **8.3 Pencarian & Filter**
- Pencarian berdasarkan name/email/address  
- Filter berdasarkan kategori  
- Reset filter  

---

## 9. Struktur Folder
```text
Kelompok-1-Aplikasi-Buku-Alamat/ 
├── app.py 
├── database.py 
├── models.py 
├── schemas.py 
├── auth.py 
├── requirements.txt 
├── static/ 
│   ├── index.html 
│   ├── styles.css 
│   └── main.js 
├── images/ 
│   └── ERD.png
```
---

## 10. Cara Instalasi dan Menjalankan Aplikasi

### **10.1 Prasyarat**
- Python 3.7+  
- MySQL Server  
- Database sudah dibuat  

### **10.2 Langkah Instalasi**

#### **1. Clone Repository**
git clone 
```sh
https://github.com/manikadityaputra-250030722/Kelompok-1-Aplikasi-Buku-Alamat.git
```

```sh
cd buku-alamat-fastapi
```
#### **2. Buat Virtual Environment**
- Windows
```sh
python -m venv venv
venv\Scripts\activate
```


- Linux / macOS
```sh
python -m venv venv
source venv/bin/activate
```

### **3. Install Dependensi**
```sh
pip install -r requirements.txt
```

### **4. Konfigurasi Database (database.py)**
```sh
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://username:password@localhost/buku_alamat"
```

### **5. Menjalankan Server FastAPI**
```sh
uvicorn app:app --reload
```
- Akses dari perangkat lain:
```sh
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```
### **6. Akses Aplikasi**

- Lokal:
```sh
http://127.0.0.1:8000/
```
- Perangkat lain:
```sh
http://IP_LAPTOP:8000/
```
