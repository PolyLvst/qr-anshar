@echo off
@REM Pastikan rclone sudah terinstall dan memiliki config yg sesuai. Ganti nama-remote sesuaikan dengan saat rclone config
@REM Pastikan foto siswa telah terupload ke google drive pada folder QR_Anshar_Foto
@REM Ganti C:\folder-program-qr-anshar ke folder program asli
@REM Contoh jika ada di folder Download/QrAnshar maka shift klik kanan folder QrAnshar lalu copy as path
@REM Masukkan ke folder-program-qr-anshar. Pastikan tidak ada tanda petik
@REM Contoh : "C:\Users\windows\Downloads\QrAnshar" menjadi C:\Users\zeef\Downloads\QrAnshar
@REM Contoh akhir adalah :
@REM rclone sync --progress "nama-remote:QR_Anshar_Foto" "C:\Users\zeef\Downloads\QrAnshar\static\assets\student-pictures"
:loop
echo Cek file dari google drive ...
rclone sync --progress --retries 10 "nama-remote:QR_Anshar_Foto" "C:\folder-program-qr-anshar\static\assets\student-pictures"
echo Cek selesai, menunggu 1 Jam untuk cek selanjutnya ...
echo Restart program bila ingin melakukannya sekarang ...
ping 127.0.0.1 -n 3600 > nul
goto loop