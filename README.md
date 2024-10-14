# qr-anshar 1.0

[GitHub Pages](https://github.com/PolyLvst/qr-anshar).

## Installation
### Windows
**Icon desktop windows**

Klik kanan, send to > desktop
- run.bat

Copy file ini ke desktop
- Scan Absensi - Shortcut

Jika ingin merubah icon shortcut, foto ada di folder resources

**Aplikasi langsung hidup setelah mesin dihidupkan**

Klik kanan create shortcut
- after_system_on.bat

Copy file dibawah, ke directory startup
- after_system_on.bat - Shortcut
- Scan Absensi - Shortcut

**Copy kedua file diatas ke dalam folder startup ini**
```
WIN + R
shell:startup
```

**Auto download gdrive**
Cek perintah di script auto_download_gdrive.bat

**Untuk mengupload foto dan excel**
Persiapkan folder QR_Anshar_Foto dan QR_Anshar_Dapodik pada google drive\
Pastikan folder ada di paling depan (tidak di dalam folder lain)\
Masukkan foto ke folder terkait dengan format nis.jpg atau nis.png\
Masukkan file excel dapodik ke folder terkait dengan nama dapodik.xlsx, file lain akan di abaikan

Hidupkan mesin tunggu download selesai\
Lakukan proses absensi

Jika ada perubahan data siswa entah foto atau dapodik, dan sedang berlangsung absensi\
Silahkan restart program

**Jika terdapat error**
- **Select column for import** ganti column_nama dan column_nis di file .env
- **No .env file found** edit .env.example ke .env lalu sesuaikan isinya
- **Error wrong data type [dapodik_import]** pastikan di nis tidak ada huruf, hanya angka. Lalu edit .env column_name dan column_nis sesuaikan dengan kolom nis dan nama

Restart mesin

## Installation (linux)
### Linux
Pastikan bootstrapper sudah diberi izin execute. Run bootstrapper
```bash
chmod +x ./bootstrap_linux.sh
./bootstrap_linux.sh
```
Jika tidak bisa, coba 
```bash
sudo apt-get install -y dos2unix
dos2unix ./bootstrap_linux.sh
```
### Usage
Klik ikon di desktop atau run langsung run.sh
```bash
./run.sh
```

CRONTAB ->
Buka crontab untuk mengautomatisasi program
```bash
crontab -e
```
Copy dan paste dari crontab.txt