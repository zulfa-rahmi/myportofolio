Nama : Zulfa Rahmi Nasution

NPM : 2506598324

Kelas : PBP A

### TUGAS 1
1. Pada Tutorial dan Tugas 1, Anda diberi kebebasan untuk menentukan tampilan dari website portofolio Anda. Saat Anda merancang struktur HTML yang digunakan, apakah Anda menggunakan elemen semantik HTML5 seperti <section>, <article>, atau <aside>? Jika iya, bagaimana elemen tersebut membantu Anda dalam membuat static web? Jika tidak, mengapa tanpa elemen tersebut sudah memenuhi kebutuhan desain Anda?

Jawaban: Saya menggunakan section dalam membuat static web saat ini, penggunaan section membantu saya untuk memisahkan beberapa bagian halaman, dan memudahkan saat menghubungkan bagian untuk navigation bar. Saya sendiri belum menggunakan <article> ataupun <aside>. Ketika saya cari tahu, penggunaan <article> itu untuk membungkus konten yang bisa berdiri sendiri, sepertinya bisa saya implementasikan di tugas berikutnya, mengubah bagian experience dari <section> menjadi <article>. Sedangkan <aside> digunakan untuk membungkus konten sampingan yang terkait secara tidak langsung, sejauh ini sepertinya belum akan saya gunakan.

2. Ketika Anda mengatur CSS Anda agar tetap responsive, tantangan tata letak apa yang Anda temukan? Bagaimana Anda mengevaluasi elemen mana yang harus diubah posisinya atau diprioritaskan ukurannya saat berpindah dari tampilan desktop ke mobile?

Jawaban: tantangannya adalah memperkirakan ukuran pixel yang harus digunakan. Akan lebih mudah jika mendesign menggunakan figma terlebih dahulu agar dapat mengetahui detail px dan lain-lainnya. Saya juga baru belajar mengenai ukuran rem ketika mulai mengerjakan website ini. Beberapa bagian di website saya terlihat kurang cocok jika hanya di resize, oleh karena itu perlu penyesuaian lebih lanjut mengenai tata letaknya jika menggunakan HP ataupun tablet. Untungnya saya menemukan metode yang tepat dengan penggunaan @media pada css. Untuk mengevaluasi elemen mana yang harus saya ubah posisinya, saya memastikan bahwa setiap elemen harus tetap terlihat dan dapat dibaca untuk setiap ukuran.

3. Website yang Anda buat saat ini adalah static web murni. Batasan apa yang Anda rasakan saat mencoba menyajikan informasi pada portofolio Anda secara optimal? Berdasarkan batasan tersebut, fungsionalitas dinamis apa yang paling ingin Anda persiapkan dan tambahkan pada iterasi proyek selanjutnya?

Jawaban: Mungkin saat saya melihat web portofolio milik orang lain, mereka menyiapkan section contact dimana user (yang melihat web tersebut) bisa langsung mengirim pesan kepada pemilik website itu. Selain itu mungkin website statis yang saat ini saya buat tidak begitu interaktif dan menarik.

DEKLARASI PENGGUNAAN AI
Dalam membuat website ini saya menggunakan AI gemini
Karena ini pertama kalinya saya membuat website jadi saya sedikit kebingungan. Pertama saya membuat excel seperti WBS untuk merancang struktur website yang akan saya buat. Kemudian, saya memvisualisasikannya menggunakan canva dan figma (seluruh link saya lampirkan diakhir). AI membantu saya untuk mengubah visualisasi dari figma tersebut menjadi kode.

### TUGAS 2
MVT Architecture & Workflow
Proses penayangan halaman portofolio baru pada aplikasi web berbasis Django mengikuti alur arsitektur MVT (Model-View-Template). Ketika pengguna mengakses URL portofolio melalui browser, Django pertama-tama akan menerima HTTP request tersebut dan mengarahkannya ke file urls.py tingkat proyek untuk menentukan rute aplikasi yang dituju. Selanjutnya, urls.py pada tingkat aplikasi mencocokkan pola URL spesifik dan meneruskan permintaan ke fungsi view yang sesuai. Fungsi view bertindak sebagai pengolah logika utama; ia meminta data portofolio dari Model, yang bertugas berkomunikasi dengan database. Setelah data diambil oleh Model dan dikembalikan ke View, View menyuntikkan data tersebut ke dalam Template HTML. Template menyusun tampilan akhir menggunakan data dinamis tersebut dan menghasilkan HTTP response utuh yang siap ditampilkan di browser pengguna.

Data Management: Model vs Hardcoded Template
Data portofolio dikelola menggunakan Model dan disimpan di dalam database, alih-alih ditulis secara langsung (hardcoded) di dalam berkas template HTML. Pendekatan ini diterapkan untuk menjaga prinsip separation of concerns serta meningkatkan kemudahan pemeliharaan dan pengembangan aplikasi. Dengan menyimpan data pada Model, penambahan, perubahan, atau penghapusan konten portofolio dapat dilakukan dengan mudah (misalnya melalui Django Admin) tanpa perlu mengubah struktur kode HTML. Selain itu, pemisahan ini membuat template berfungsi sebagai cetakan dinamis yang dapat digunakan kembali untuk banyak data (scalable), meminimalkan risiko kesalahan pengetikan pada struktur tampilan, dan memudahkan integrasi fitur tingkat lanjut seperti pencarian, pemfilteran, maupun paginasi di masa mendatang.

Database Migration: makemigrations & migrate
Dalam manajemen database Django, perintah makemigrations dan migrate memiliki peran yang saling melengkapi dalam mengelola perubahan struktur tabel (schema). Perintah makemigrations berfungsi untuk mengevaluasi perubahan pada file models.py dan mendokumentasikannya ke dalam berkas instruksi migrasi baru di folder migrations/ tanpa mengubah database secara langsung. Sementara itu, perintah migrate bertugas mengeksekusi instruksi dari berkas migrasi tersebut untuk memperbarui struktur tabel yang ada di dalam database nyata. Sebagai contoh, ketika terdapat penambahan bidang baru seperti created_at = models.DateField() pada model Portfolio, perintah makemigrations akan mencatat rancangan penambahan kolom tersebut, dan perintah migrate akan mengeksekusi penambahan kolom created_at ke dalam tabel database.

AI DISCLOSURE
Saya menggunakan AI gemini untuk memperbaiki tampilan css dan beberapa tampilan yang tidak muncul pada bagian web seperti gambar, organisasi, dan lain-lain

Chat dengan gemini: https://gemini.google.com/share/d/1vK890OqxO4YDOPfcnuDQskwB-UMYFf3P?usp=sharing


### TUGAS 3
Pertanyaan Reflektif

# 1. Mengapa kita menggunakan ModelForm pada Django alih-alih membuat form HTML secara manual? Mengapa kita diwajibkan menambahkan {% csrf_token %} pada form tersebut?
Pake ModelForm jauh lebih praktis karena bentuk form dan validasinya otomatis ngikutin struktur Model yang udah kita buat di database. Kita ga perlu ngetik tag input manual satu-satu di HTML atau ribet nge-validasi data request.POST sendiri. Kalau struktur field di database diganti, form-nya bakal otomatis menyesuaikan. Selain itu, ModelForm udah punya fungsi is_valid() dan save() yang langsung nyimpan data ke database.

Kalau {% csrf_token %} itu wajib dipasang buat keamanan dari serangan CSRF (Cross-Site Request Forgery). Token ini bakal nyisipin kode unik di form buat mastiin kalau data emang dikirim langsung dari halaman web kita, bukan dari situs lain yang mencoba memanipulasi aksi user. Tanpa token ini, Django bakal otomatis nolak request POST yang masuk.

# 2. Mengapa JSON lebih disukai dalam pengembangan aplikasi web modern dibandingkan XML?
JSON lebih populer dibanding XML karena beberapa alasan:
- Lebih ringkas: JSON ga pake tag pembuka dan penutup yang panjang kayak XML, jadi ukuran datanya lebih kecil dan loading-nya lebih cepat.
- Gampang dibaca: Strukturnya cuma berupa pasangan key-value dan array sederhana, jadi nyaman dibaca manusia.
- Cocok banget sama JavaScript: Karena formatnya berbasis objek JavaScript, data JSON bisa langsung diparsing di browser pakai JSON.parse() tanpa butuh library tambahan.
- Proses parsing cepat: Hampir semua bahasa pemrograman bisa ngolah JSON jauh lebih cepat dan ringan dibanding XML yang terbilang berat.

# 3. Jelaskan alur yang terjadi saat kamu menggunakan fungsi view untuk mengembalikan data portofoliomu dalam bentuk JSON. Mengapa kita perlu melakukan proses serialization pada model Django sebelum datanya dikembalikan?
Alurnya di fungsi get_projects_json:
1. User/browser ngirim request ke URL api/projects/.
2. View bakal ngambil data dari database lewat ORM pakai Project.objects.all().
3. Data yang ditarik dari database ini bentuknya masih berupa Objek Python (Queryset Django).
4. Karena browser cuma ngerti teks/JSON, kita ubah objek Python tadi jadi string JSON pake fungsi serializers.serialize("json", projects).
5. String JSON tersebut dikirim balik ke browser dalam bentuk HttpResponse.
6. Di view show_projects, data JSON itu diambil dan di-deserialize balik jadi objek Project biar bisa di-render rapi di file projects.html.

Proses serialization ini wajib dilakukan karena objek Python/Django ga bisa langsung dikirim lewat protokol HTTP. Objek itu harus diubah dulu ke format teks standar (seperti JSON) supaya datanya bisa dibaca dan diolah oleh browser atau aplikasi lain.

DEKLARASI AI
Dalam membuat website ini saya menggunakan AI gemini
Karena ternyata sudah ada beberapa hal yang saya implementasikan di tugas individu sebelumnya jadi untuk tugas saat ini saya hanya tinggal membuat form dan merapikan tampilan web lewat css. Untuk pembuatan formnya saya menggunakan AI untuk mempelajari beberapa sintaks. Sedangkan untuk proses merapikan tampilannya saya dibantu oleh AI untuk memvisualisasikan keinginan saya.
chat dengan gemini: https://gemini.google.com/share/d/1QAPC16-DN3RL5emaazy5XCcZYWViUq6P?usp=sharing