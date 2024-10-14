@echo off
@REM Pastikan rclone sudah terinstall dan memiliki config yg sesuai. Ganti nama-remote sesuaikan dengan saat rclone config
@REM Pastikan foto siswa telah terupload ke google drive pada folder QR_Anshar_Foto
@REM Ganti C:\folder-program-qr-anshar ke folder program asli
@REM Contoh jika ada di folder Download/QrAnshar maka shift klik kanan folder QrAnshar lalu copy as path
@REM Masukkan ke folder-program-qr-anshar. Pastikan tidak ada tanda petik
@REM Contoh : "C:\Users\windows\Downloads\QrAnshar" menjadi C:\Users\windows\Downloads\QrAnshar
@REM Contoh akhir adalah :
@REM rclone sync --progress --retries 10 "nama-remote:QR_Anshar_Foto" "C:\Users\windows\Downloads\QrAnshar\static\assets\student-pictures"
@REM rclone sync --progress --retries 10 "nama-remote:QR_Anshar_Dapodik" "C:\Users\windows\Downloads\QrAnshar\import_dapodik\excel"

echo Cek file dari google drive ...
rclone sync --progress --retries 10 "nama-remote:QR_Anshar_Foto" "C:\folder-program-qr-anshar\static\assets\student-pictures"
rclone sync --progress --retries 10 "nama-remote:QR_Anshar_Dapodik" "C:\folder-program-qr-anshar\import_dapodik\excel"