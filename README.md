# 🏷️ Studi Kasus 9 — Generator Slogan / Tagline

Aplikasi Flask berbasis LLM untuk membuat slogan atau tagline kreatif untuk produk, komunitas, atau kampanye.

---

## 📋 Deskripsi

Aplikasi ini menerima informasi tentang suatu entitas (nama, deskripsi, nilai utama) dan menggunakan LLM untuk menghasilkan beberapa slogan atau tagline kreatif dalam **Bahasa Indonesia**, **Bahasa Inggris**, atau **keduanya**.

---

## 🗂️ Struktur Proyek

```
modsim-2026-p9-ifs25009/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── config.py                # Konfigurasi dari .env
│   ├── extensions.py            # SQLAlchemy engine & session
│   ├── models/
│   │   ├── slogan_request.py    # Model SloganRequest
│   │   └── slogan.py            # Model Slogan
│   ├── routes/
│   │   └── slogan_routes.py     # Blueprint endpoint API
│   ├── services/
│   │   ├── llm_service.py       # Komunikasi dengan OpenRouter API
│   │   └── slogan_service.py    # Business logic generate & query
│   └── utils/
│       └── parser.py            # Parser JSON dari LLM
├── db/
│   └── .gitignore
├── static/
│   └── index.html               # Frontend UI
├── .env                         # Konfigurasi environment
├── .gitignore
├── app.http                     # File uji API (REST Client)
├── app.py                       # Entry point aplikasi
└── requirements.txt
```

---

## 🗃️ Model Database

### `SloganRequest`
| Field        | Tipe         | Keterangan                          |
|--------------|--------------|-------------------------------------|
| id           | Integer (PK) | Primary key                         |
| entity_name  | String(200)  | Nama produk/komunitas/kampanye      |
| description  | String(500)  | Deskripsi singkat entitas           |
| core_values  | String(300)  | Nilai utama (koma-separated)        |
| language     | String(20)   | "id", "en", atau "both"             |
| created_at   | DateTime     | Waktu pembuatan request             |

### `Slogan`
| Field       | Tipe         | Keterangan                          |
|-------------|--------------|-------------------------------------|
| id          | Integer (PK) | Primary key                         |
| text        | Text         | Teks slogan/tagline                 |
| language    | String(10)   | Bahasa slogan ("id" atau "en")      |
| request_id  | Integer (FK) | Referensi ke SloganRequest          |
| created_at  | DateTime     | Waktu pembuatan slogan              |

---

## 🔌 Endpoint API

### `POST /slogans/generate`
Generate slogan baru menggunakan LLM.

**Body JSON:**
```json
{
  "entity_name": "EduTech Nusantara",
  "description": "Platform belajar online untuk pelajar Indonesia",
  "core_values": "inovasi, inklusif, inspiratif",
  "total": 5,
  "language": "both"
}
```

**Response:**
```json
{
  "entity_name": "EduTech Nusantara",
  "language": "both",
  "total": 5,
  "data": [
    {"text": "Belajar Tanpa Batas, Meraih Tanpa Henti.", "language": "id"},
    {"text": "Empowering Every Student, Everywhere.", "language": "en"}
  ]
}
```

---

### `GET /slogans`
Ambil semua slogan yang tersimpan (dengan paginasi).

**Query Params:** `page`, `per_page`

**Response:**
```json
{
  "page": 1,
  "per_page": 10,
  "total": 15,
  "total_pages": 2,
  "data": [...]
}
```

---

### `GET /slogans/<id>`
Ambil detail satu slogan beserta metadata request-nya.

**Response:**
```json
{
  "id": 1,
  "text": "Belajar Tanpa Batas, Meraih Tanpa Henti.",
  "language": "id",
  "request_id": 1,
  "created_at": "2026-04-24T10:35:12.123456",
  "request": {
    "id": 1,
    "entity_name": "EduTech Nusantara",
    "description": "Platform belajar online untuk pelajar Indonesia",
    "core_values": "inovasi, inklusif, inspiratif",
    "language": "both",
    "created_at": "2026-04-24T10:35:10.000000"
  }
}
```

---

## ⚙️ Cara Menjalankan

### 1. Clone / ekstrak proyek
```bash
cd modsim-2026-p9-ifs25009
```

### 2. Buat Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Konfigurasi `.env`
Edit file `.env` dan isi dengan token LLM Anda:
```env
APP_PORT=5000
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_TOKEN=sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxx
```

### 5. Jalankan Aplikasi
```bash
python app.py
```

Buka browser di: **http://localhost:5000**

---

## 🧪 Pengujian API

Gunakan file `app.http` dengan ekstensi **REST Client** di VS Code, atau gunakan **Postman** / **curl**.

```bash
# Generate slogan
curl -X POST http://localhost:5000/slogans/generate \
  -H "Content-Type: application/json" \
  -d '{"entity_name":"Test Brand","description":"Brand test","core_values":"inovasi","total":3,"language":"id"}'

# Ambil semua slogan
curl http://localhost:5000/slogans?page=1&per_page=10

# Detail slogan
curl http://localhost:5000/slogans/1
```
