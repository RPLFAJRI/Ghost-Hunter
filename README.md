
# Ghost Hunter

> Game aksi 2D berbasis Python dan Pygame — lawan para musuh, kumpulkan diamond, dan selamatkan dunia!
---


## Deskripsi Project

**Ghost Hunter** adalah game aksi 2D side-scrolling yang dibangun menggunakan **Python** dan **Pygame**. Pemain berperan sebagai karakter pemberani yang harus melewati 3 level berbeda sambil melawan musuh-musuh hantu yang berkeliaran. Gunakan senjata tembak dan granat untuk mengalahkan semua musuh, kumpulkan diamond, ambil potion untuk memulihkan HP, dan capai garis akhir di setiap level!

---



## Anggota Kelompok

| No | Nama | Peran |
|----|------|-------|
| 1 | **Fajriandi Ramadhan** | Developer |
| 2 | **M Afiffudin Zain** | Developer |
| 3 | **Ibrahim Al Albany** | Developer |
| 4 | **Felix Nathaniel NP** | Developer |

---

## Fitur Utama

- **3 Level Unik** — Setiap level memiliki desain peta yang berbeda dengan musuh dan rintangan yang semakin menantang.
- **Sistem Musuh (Ghost/AI)** — Musuh berpatroli secara otomatis dan menembak peluru ke arah pemain saat berada dalam jangkauan.
- **Sistem Senjata Ganda** — Pemain dapat menembak peluru biasa (klik kiri) dan melempar granat (tombol `G`) yang memiliki efek ledakan berdampak area.
- **Grenade dengan Damage Area** — Granat memiliki tiga tingkat damage berdasarkan jarak ledakan (dekat, sedang, jauh).
- **Collectible Items** — Kumpulkan diamond untuk skor dan ambil health potion untuk memulihkan HP.
- **Sistem HP & Animasi** — HP bar berwarna hijau/merah dinamis, serta animasi karakter lengkap: idle, jalan, lompat, serang, terkena, dan mati.
- **Hazard Zona Air** — Menyentuh air langsung mereset pemain.
- **Musik & Sound Effects** — Musik latar berjalan terus-menerus, dilengkapi SFX untuk tembakan, lompat, ledakan, diamond, dan navigasi menu.
- **Parallax Background** — Latar belakang bergerak dengan efek parallax 3 lapis untuk kesan kedalaman.
- **Menu Navigasi Lengkap** — Main Menu, halaman About, halaman Controls, dan layar kemenangan.
- **Level Editor** — Dilengkapi tool level editor untuk membuat dan menyunting data level.

---

## Cara Menjalankan Project

### Prasyarat

Pastikan sudah menginstal:
- Python 3.10+
- Pygame

```bash
pip install pygame
```

### Langkah Menjalankan

1. Clone atau ekstrak folder project ini.
2. Masuk ke direktori utama project: Ghost Hunter

3. Jalankan file utama dari dalam folder `main/`: Main.py


### Kontrol Game

| Tombol | Aksi |
|--------|------|
| `A` | Gerak ke kiri |
| `D` | Gerak ke kanan |
| `W` | Lompat |
| `Klik Kiri`| Tembak peluru |
| `G` | Lempar granat |
| `ESC` / `Q` | Keluar game |

---

## Struktur Project

```
Ghost Hunter/
├── main/
│   ├── main.py           # Entry point & GameManager
│   ├── base.py           # Abstract base classes (OOP core)
│   ├── player.py         # Kelas Player
│   ├── enemies.py        # Kelas Enemy & Ghost
│   ├── projectiles.py    # Kelas Bullet & Grenade
│   ├── world.py          # Kelas World & WorldObject
│   ├── particles.py      # Efek partikel (Trail, Explosion)
│   ├── button.py         # Kelas Button UI
│   ├── texts.py          # Kelas teks & pesan UI
│   └── level_editor.py   # Tool level editor
├── Assets/               # Sprite gambar player, ghost, UI
├── Fonts/                # File font kustom (.ttf)
├── Levels/               # Data level tersimpan
└── Sounds/               # File audio (.mp3 / .wav)
```

---

## Penjelasan Implementasi OOP

Project ini dirancang dengan prinsip OOP secara menyeluruh menggunakan **abstract base class**, **inheritance**, **encapsulation**, dan **polymorphism**.

### 1. Abstract Base Classes — `base.py`

Semua entitas game dibangun di atas hierarki abstrak yang terdefinisi di `base.py`:

```
Drawable (ABC)          → wajib implementasi draw()
Updatable (ABC)         → wajib implementasi update()
    │
GameEntity (Sprite + Drawable + Updatable)
    │   → properti health, alive (dengan encapsulation getter/setter)
    │   → abstract: _load_animations(), _update_animation()
    │
    ├── Character        → tambah: movement, gravity, jump, hit
    │       ├── Player   → kontrol pemain, tembak, granat
    │       └── Enemy    → patroli, shoot range, cooldown timer
    │               └── Ghost   → implementasi konkret musuh
    │
WorldObject (Sprite + Updatable)  → tile/objek dunia (Diamond, Potion, dll)
Projectile (Sprite + Drawable + Updatable)  → proyektil dasar
    ├── Bullet           → peluru lurus cepat
    └── Grenade          → granat parabolik dengan area damage
```

### 2. Encapsulation

Atribut sensitif dilindungi dengan **property** dan **setter** bervalidasi:

```python
# Contoh di base.py — health tidak bisa negatif
@health.setter
def health(self, value: int) -> None:
    self._health = max(0, value)   # validasi otomatis
    if self._health <= 0:
        self._alive = False        # side-effect terkelola
```

Atribut privat animasi di `Player` (seperti `__idle_index`, `__walk_index`) hanya dapat diubah dari dalam kelas itu sendiri.

### 3. Inheritance

`Player` dan `Ghost` mewarisi `Character` → `GameEntity`, sehingga berbagi logika animasi, HP, gravity, dan sprite tanpa duplikasi kode. `Ghost` juga mewarisi `Enemy` yang menambahkan logika patroli dan penembakan.

### 4. Polymorphism

Method `update()` dan `draw()` diimplementasikan berbeda di setiap kelas sesuai kebutuhan:

- `Bullet.update()` → gerak horizontal lurus, cek tabrakan tile
- `Grenade.update()` → fisika parabola, pantul dinding, hitung timer ledakan
- `Ghost.update()` → patroli bolak-balik, transisi animasi kematian, tembak jika pemain dalam range

### 5. Kelas `GameManager` — Pengelola Utama

`GameManager` di `main.py` bertanggung jawab penuh atas game loop, manajemen state (menu, gameplay, menang), pengelolaan sprite group, loading aset, dan routing event — memisahkan logika game dari logika tampilan secara bersih.

---

## Screenshot Tampilan Program

| Tampilan | Deskripsi |
|----------|-----------|
| ![image alt](https://github.com/RPLFAJRI/Ghost-Hunter/blob/7e47547e0d9c3c304a19472f6e7909ac2c5772d5/Gameplay.png) | Main Menu dengan tombol Play, About, Controls, Exit |
| ![image alt](https://github.com/RPLFAJRI/Ghost-Hunter/blob/0f6ebb9e1c458ae810a529d3f9ee6aeaa4ac8802/Gameplay.png) | Gameplay dengan HP bar, grenade counter, dan musuh |
| ![image alt](https://github.com/RPLFAJRI/Ghost-Hunter/blob/0f6ebb9e1c458ae810a529d3f9ee6aeaa4ac8802/Win.png) | Layar kemenangan setelah menyelesaikan semua level |

---

## Tujuan

Project ini dibuat untuk keperluan tugas akademik.
