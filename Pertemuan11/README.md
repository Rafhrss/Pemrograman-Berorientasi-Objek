# Refactoring dan Prinsip SOLID dalam Pengembangan Perangkat Lunak
## 1. Apa itu Refactoring

Refactoring adalah proses restrukturisasi kode komputer yang ada tanpa mengubah perilaku eksternalnya.

### Tujuan Refactoring:

* **Meningkatkan Keterbacaan (Readability):** Membuat kode lebih mudah dipahami oleh pengembang lain dan diri Anda sendiri di masa depan.

* **Mengurangi Kompleksitas:** Memecah method atau kelas yang terlalu besar (Code Smell: Long Method atau God Object).

* **Membuat Kode Lebih Fleksibel:** Mempersiapkan kode untuk penambahan fitur baru dengan mudah.

* **Mengurangi Bug:** Kode yang lebih sederhana dan terstruktur cenderung memiliki lebih sedikit bug atau lebih mudah dideteksi.

Refactoring sering kali dilakukan dengan berpegangan pada seperangkat pedoman, dan pedoman paling utama dalam Object-Oriented Programming (OOP) adalah Prinsip SOLID.

---

## 2. Prinsip SOLID

SOLID adalah akronim dari lima prinsip desain yang dimaksudkan untuk membuat desain perangkat lunak lebih mudah dipahami, fleksibel, dan dapat dipelihara. 

#### 1. Single Responsibility Principle 
Sebuah kelas harus hanya memiliki satu alasan untuk berubah.
* Tujuan: Memastikan setiap kelas atau modul berfokus pada satu tugas tunggal.
* Contoh Pelanggaran: Kelas Laporan yang bertanggung jawab untuk membuat format laporan dan menyimpan laporan ke database. Jika ada dua concern (logika bisnis dan persistensi data) dalam satu kelas, maka kelas tersebut melanggar SRP.
* Solusi Refactoring: Pisahkan menjadi dua kelas: ReportFormatter dan ReportRepository.

#### 2. Open/Closed Principle
Entitas perangkat lunak (kelas, modul) harus terbuka untuk ekstensi, tetapi tertutup untuk modifikasi.
* Tujuan: Memungkinkan penambahan fungsionalitas baru (ekstensi) tanpa mengubah kode yang sudah ada dan teruji (modifikasi).
* Contoh Pelanggaran: Sebuah kelas CheckoutService memiliki serangkaian if/elif panjang untuk memproses berbagai metode pembayaran. Setiap penambahan metode pembayaran baru mewajibkan pengubahan kode CheckoutService.
* Solusi Refactoring: Gunakan Abstraksi (Interface/ABC). Buat antarmuka IPaymentProcessor. Implementasi pembayaran baru (misalnya QrisProcessor) dapat dibuat sebagai kelas baru yang mengimplementasikan antarmuka tersebut, tanpa perlu mengubah CheckoutService sama sekali.

#### 3. Liskov Substitution Principle
Objek dalam program harus dapat diganti dengan subtipe (turunannya) tanpa merusak fungsionalitas program.
* Tujuan: Memastikan bahwa pewarisan (Inheritance) digunakan dengan benar, di mana kelas turunan (subclass) harus dapat menggantikan kelas induk (superclass) tanpa mengubah hasil yang diharapkan.
* Contoh Pelanggaran: Jika Anda memiliki kelas Burung dengan method terbang(), dan Anda membuat BurungUnta sebagai subclass. Namun, BurungUnta.terbang() harus melempar error atau tidak melakukan apa-apa. Ini melanggar LSP karena BurungUnta tidak dapat menggantikan Burung dalam konteks terbang().
* Solusi Refactoring: Pastikan subclass mempertahankan semua perilaku dan kontrak dari superclass-nya. Jika tidak, buat abstraksi baru atau ubah hierarki kelas.

#### 4. Interface Segregation Principle
Klien tidak boleh dipaksa untuk bergantung pada antarmuka yang tidak mereka gunakan.
* Tujuan: Memecah antarmuka besar yang berisi banyak method menjadi antarmuka-antarmuka yang lebih kecil dan spesifik (Role Interface).
* Contoh Pelanggaran: Antarmuka IPrinter memiliki method print_document(), scan_document(), dan fax_document(). Kelas SimplePrinter hanya bisa mencetak, namun dipaksa mengimplementasikan method scan_document() dan fax_document() yang mungkin hanya berisi pengecualian atau method kosong.
* Solusi Refactoring: Pisahkan menjadi antarmuka yang lebih kecil: IPrinter, IScanner, dan IFaxMachine.

#### 5. Dependency Inversion Principle
Bergantunglah pada abstraksi, bukan pada detail konkret.
* Tujuan: Memisahkan lapisan logika tingkat tinggi (kebijakan bisnis) dari lapisan detail (implementasi konkret).
* Contoh Pelanggaran: Kelas tingkat tinggi Store membuat (new) objek kelas konkret tingkat rendah seperti DatabaseProductRepository.
* Solusi Refactoring:
    - Gunakan Abstraksi (Interface/ABC) untuk lapisan detail.
    - Kelas tingkat tinggi (seperti Store) harus berkomunikasi melalui Abstraksi tersebut.
    - Terapkan Dependency Injection (DI): Jangan biarkan kelas membuat dependensinya sendiri; biarkan dependensi "disuntikkan" dari luar, biasanya melalui constructor.






# Analisis Pelanggaran Prinsip SOLID pada ValidatorManager

**1. Single Responsibility Principle (SRP):**
Identifikasi: class ValidatorManager memiliki lebih dari satu alasan untuk berubah.
Penjelasan: Tanggung jawab untuk Validasi SKS dan Validasi Prasyarat digabungkan dalam satu class atau method. Jika batas SKS berubah, class harus diubah. Jika logika penentuan prasyarat berubah, class juga harus diubah. Ini melanggar SRP karena class memiliki lebih dari satu tanggung jawab.

**2. Open/Closed Principle (OCP):**
Identifikasi: class ini tidak terbuka untuk ekstensi tetapi tertutup untuk modifikasi.
Penjelasan: Untuk menambahkan aturan validasi baru (misalnya, Validasi Jadwal Bentrok), kita harus memodifikasi kode internal ValidatorManager.validate_registration (menambah if/elif baru). OCP mengharuskan penambahan fungsionalitas ekstensi dilakukan tanpa mengubah kode yang sudah ada atau modifikasi.

**3. Dependency Inversion Principle (DIP):**
Identifikasi: class tingkat tinggi (ValidatorManager) bergantung pada implementasi detail yang konkret.
Penjelasan: Logika Validasi SKS dan Prasyarat diimplementasikan secara langsung (hardcoded) di dalam ValidatorManager. class ini seharusnya bergantung pada Abstraksi (seperti antarmuka IValidationRule), bukan pada detail implementasi (logika if/else SKS atau Prasyarat)


# Penjelasan Studi Kasus Refactoring Sistem Validasi Registrasi Mahasiswa
## 1. Struktur Data Mahasiswa
Ini adalah Model Data sederhana yang menyimpan informasi dasar mahasiswa yaitu NIM, SKS yang diambil, dan status prasyarat mata kuliah.

## 2. Memisahkan Tanggung Jawab (SRP & DIP)
IValidationRule (Abstraksi)	DIP	Ini adalah kontrak. Semua aturan validasi (misalnya SKS, Prasyarat) harus berjanji memiliki method validate(). Kelas koordinator hanya tahu tentang kontrak ini.
SksLimitRule & PrerequisiteRule	SRP	Ini adalah implementasi spesifik. Masing-masing hanya tahu cara melakukan satu tugas (misalnya, SksLimitRule hanya menghitung batas SKS).
JadwalBentrokRule	OCP	Ini adalah fitur baru yang ditambahkan. Ia membuktikan bahwa kita bisa menambah aturan baru hanya dengan membuat kelas baru tanpa mengubah kode inti.

## 3. Kelas Koordinator (RegistrationService)
- Ini adalah "Bos" atau Koordinator.
- Ia tidak tahu detail cara kerja SKS atau Prasyarat; ia hanya tahu bahwa ada sekelompok "Aturan" yang harus dijalankan.
- Dependency Injection (DI): Aturan-aturan spesifik (seperti SksLimitRule) "disuntikkan" (diberikan) kepada RegistrationService saat ia dibuat.
-   Method register_mhs hanya bertugas mengulang semua aturan yang diberikan kepadanya. Jika salah satu aturan gagal, seluruh proses dibatalkan.


## Keuntungan dari Struktur Ini (OCP)
Jika di masa depan ada aturan baru (misalnya, Validasi Pembayaran SPP), kita hanya perlu Membuat kelas baru: PaymentRule dan Meng inject PaymentRule ke dalam RegistrationService saat setup.
Kita tidak perlu mengubah kode internal RegistrationService sama sekali. Ini adalah inti dari kode yang bersih dan mudah dikelola (OCP).


## Kesimpulan
Dengan menerapkan **SRP, OCP, dan DIP**, struktur kode baru menggunakan IValidationRule dan RegistrationService telah berhasil di refactor menjadi sistem yang modular, mudah diuji, dan skalabel.


**Jadi, Refactoring itu sebuah prosses yang penting**

<img src="https://images.prismic.io/superpupertest/575aba46-0b6e-4067-babb-35790ce11306_Frame+2652.png?auto=compress,format&dpr=3" />