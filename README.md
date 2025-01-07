# Voice-Recognition-Based-Smart-Home-System-Using-Long-Short-Term-Memory-Model
File yang diperlukan untuk menggunakan sistem

langkah 1:
Silahkan unduh file berikut:

"realTimeCodeRaspberry.py", dan "model_lstm_fix_v2.h5"
Jika anda telah mengunduhnya, silahkan buat folder baru pada raspberry pi 5 anda untuk menyimpan file tersebut. Pastikan kedua file terletak pada folder yang sama dan tidak terpisah.
Jika sudah program siap digunakan.


langkah 2:
Buat virtual enviroment untuk program dan library yang dibutuhkan. Penting untuk diingat bahwa library yang dibutuhkan harus diinstall di dalam virtual environment dan program dijalankan di dalam virtual environment tersebut. pastikan dahulu bahwa anda telah menginstall pyhthon 3.
Jalankan kode berikut pada terminal:

kode 1: python3 -m venv nama_env (nama_env bisa diganti dengan nama virtual environment yang anda mau)
kode 2: source nama_env/bin/activate (untuk mengaktifkan virtual environment)


langkah 3:
Install library yang dibutuhkan.
Jalankan kode berikut:

kode 1: pip3 install gpiozero sounddevice wavio librosa numpy pandas tensorflow keras
kode 2: pip3 install scipy matplotlib


langkah 4:
Wiring sistem sesuai dengan gambar pada file skematik.png
