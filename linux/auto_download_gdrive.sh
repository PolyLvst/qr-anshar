#!/bin/bash

# Pastikan rclone sudah terinstall dan memiliki config yang sesuai. Ganti nama_remote sesuai dengan saat rclone config
# Pastikan foto siswa telah terupload ke Google Drive pada folder QR_Anshar_Foto
# Ganti /path/to/folder-program-qr-anshar ke folder program yang sesuai
# Contoh jika ada di ~/Downloads/QrAnshar, maka ganti jadi /home/username/Downloads/QrAnshar
# Contoh akhir:
# rclone sync --progress "nama_remote:QR_Anshar_Foto" "/home/username/Downloads/QrAnshar/static/assets/student-pictures"

REMOTE_NAME="nama_remote:QR_Anshar_Foto"
LOCAL_FOLDER="/path/to/folder-program-qr-anshar/static/assets/student-pictures"

while true; do
    echo "Cek file dari Google Drive ..."
    rclone sync --progress --retries 10 "$REMOTE_NAME" "$LOCAL_FOLDER"
    echo "Cek selesai, menunggu 1 jam untuk cek selanjutnya ..."
    echo "Restart program bila ingin melakukannya sekarang ..."
    sleep 3600
done
