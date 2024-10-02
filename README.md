# qr-anshar 1.0

[GitHub Pages](https://github.com/PolyLvst/qr-anshar).

## Installation
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

## Usage
Klik ikon di desktop atau run langsung run.sh
```bash
./run.sh
```

DB ->
Import database main, ke MySQL / phpmyadmin

CRONTAB ->
Buka crontab untuk mengautomatisasi program
```bash
crontab -e
```
Copy dan paste dari crontab.txt