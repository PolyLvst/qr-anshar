# qr-anshar 1.0

## Installation
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