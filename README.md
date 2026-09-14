Nama : Zulfa Rahmi Nasution

NPM : 2506598324

Kelas : PBP A

MVT Architecture & Workflow
Proses penayangan halaman portofolio baru pada aplikasi web berbasis Django mengikuti alur arsitektur MVT (Model-View-Template). Ketika pengguna mengakses URL portofolio melalui browser, Django pertama-tama akan menerima HTTP request tersebut dan mengarahkannya ke file urls.py tingkat proyek untuk menentukan rute aplikasi yang dituju. Selanjutnya, urls.py pada tingkat aplikasi mencocokkan pola URL spesifik dan meneruskan permintaan ke fungsi view yang sesuai. Fungsi view bertindak sebagai pengolah logika utama; ia meminta data portofolio dari Model, yang bertugas berkomunikasi dengan database. Setelah data diambil oleh Model dan dikembalikan ke View, View menyuntikkan data tersebut ke dalam Template HTML. Template menyusun tampilan akhir menggunakan data dinamis tersebut dan menghasilkan HTTP response utuh yang siap ditampilkan di browser pengguna.

Data Management: Model vs Hardcoded Template
Data portofolio dikelola menggunakan Model dan disimpan di dalam database, alih-alih ditulis secara langsung (hardcoded) di dalam berkas template HTML. Pendekatan ini diterapkan untuk menjaga prinsip separation of concerns serta meningkatkan kemudahan pemeliharaan dan pengembangan aplikasi. Dengan menyimpan data pada Model, penambahan, perubahan, atau penghapusan konten portofolio dapat dilakukan dengan mudah (misalnya melalui Django Admin) tanpa perlu mengubah struktur kode HTML. Selain itu, pemisahan ini membuat template berfungsi sebagai cetakan dinamis yang dapat digunakan kembali untuk banyak data (scalable), meminimalkan risiko kesalahan pengetikan pada struktur tampilan, dan memudahkan integrasi fitur tingkat lanjut seperti pencarian, pemfilteran, maupun paginasi di masa mendatang.

Database Migration: makemigrations & migrate
Dalam manajemen database Django, perintah makemigrations dan migrate memiliki peran yang saling melengkapi dalam mengelola perubahan struktur tabel (schema). Perintah makemigrations berfungsi untuk mengevaluasi perubahan pada file models.py dan mendokumentasikannya ke dalam berkas instruksi migrasi baru di folder migrations/ tanpa mengubah database secara langsung. Sementara itu, perintah migrate bertugas mengeksekusi instruksi dari berkas migrasi tersebut untuk memperbarui struktur tabel yang ada di dalam database nyata. Sebagai contoh, ketika terdapat penambahan bidang baru seperti created_at = models.DateField() pada model Portfolio, perintah makemigrations akan mencatat rancangan penambahan kolom tersebut, dan perintah migrate akan mengeksekusi penambahan kolom created_at ke dalam tabel database.

AI DISCLOSURE
Saya menggunakan AI gemini untuk memperbaiki tampilan css dan beberapa tampilan yang tidak muncul pada bagian web seperti gambar, organisasi, dan lain-lain

Chat dengan gemini: https://gemini.google.com/share/d/1vK890OqxO4YDOPfcnuDQskwB-UMYFf3P?usp=sharing