from gpiozero import LED, DigitalOutputDevice
import sounddevice as sd
import wavio as wv
import librosa
import numpy as np
import pandas as pd
import time
from tensorflow.keras.models import load_model

# File output MFCC ke CSV
file_mfcc_csv = 'output_mfcc.csv'
model = load_model('model_lstm_fix_v2.h5')

# GPIO Device Configuration
lamp_back = LED(5)
lamp_front = LED(6)
solenoid = DigitalOutputDevice(25)
fan = LED(22)
indicator_lamp = LED(16)

# Fungsi merekam suara
def rekam_suara(freq, durasi):
    recording = sd.rec(int(durasi * freq),
                       samplerate=freq, channels=1)
    print('Sedang merekam...')
    sd.wait()
    print('Perekaman berhasil')
    # Simpan hasil rekaman ke file .wav
    filename = "rekaman.wav"
    wv.write(filename, recording, freq, sampwidth=2)
    return filename

# Fungsi ekstraksi fitur MFCC
def ekstraksiFiturMFCC(audio, max_len=44, n_mfcc=13):
    signal, sr = librosa.load(audio)
    mfccs = librosa.feature.mfcc(y=signal, n_mfcc=n_mfcc, sr=sr)

    # Padding
    if mfccs.shape[1] < max_len:
        mfccs = np.pad(mfccs, ((0, 0), (0, max_len - mfccs.shape[1])), mode='constant')
    else:
        mfccs = mfccs[:, :max_len]

    # Transposisi
    mfccs = mfccs.T
    return mfccs

# Fungsi menyimpan MFCC ke CSV
def mfccToCSV(datamfcc):
    df = pd.DataFrame(datamfcc)
    output_csv_path = file_mfcc_csv
    df.to_csv(output_csv_path, index=False, header=False)

# Fungsi kontrol perangkat berdasarkan prediksi
def kontrolPerangkat(kelas_terpilih):
    if kelas_terpilih == "lampu belakang menyala":
        lamp_back.on()
        print("Lampu belakang dinyalakan")
    elif kelas_terpilih == "lampu belakang mati":
        lamp_back.off()
        print("Lampu belakang dimatikan")
    elif kelas_terpilih == "lampu depan menyala":
        lamp_front.on()
        print("Lampu depan dinyalakan")
    elif kelas_terpilih == "lampu depan mati":
        lamp_front.off()
        print("Lampu depan dimatikan")
    elif kelas_terpilih == "buka pintu":
        solenoid.on()
        print("Solenoid dinyalakan (pintu dibuka)")
    elif kelas_terpilih == "kunci pintu":
        solenoid.off()
        print("Solenoid dimatikan (pintu dikunci)")
    elif kelas_terpilih == "kipas menyala":
        fan.on()
        print("Kipas dinyalakan")
    elif kelas_terpilih == "kipas mati":
        fan.off()
        print("Kipas dimatikan")
    elif kelas_terpilih == "silence":
        indicator_lamp.on()
        time.sleep(3)
        indicator_lamp.off()

# Fungsi prediksi
def prediksiInput(filecsvmfcc):
    data = pd.read_csv(filecsvmfcc, header=None)
    data_mfcc = data.to_numpy()

    # Menambahkan dimensi batch
    data_mfcc = np.expand_dims(data_mfcc, axis=0)

    # Prediksi
    prediksi = model.predict(data_mfcc)

    # Daftar kelas
    kelas = ["lampu belakang menyala", "lampu belakang mati", "lampu depan menyala", "lampu depan mati",
             "buka pintu", "kunci pintu", "kipas menyala", "kipas mati", "silence"]

    # Mendapatkan indeks kelas dengan probabilitas tertinggi
    indeks_kelas_tertinggi = np.argmax(prediksi)

    # Mendapatkan nama kelas
    kelas_terpilih = kelas[indeks_kelas_tertinggi]
    print("Kelas yang diprediksi:", kelas_terpilih)

    # Kontrol perangkat berdasarkan prediksi
    kontrolPerangkat(kelas_terpilih)

# Loop utama
while True:
    indicator_lamp.on()
    time.sleep(5)
    indicator_lamp.off()
    print("Tekan tombol 'x' untuk keluar dari program.")
    while True:
        indicator_lamp.on()
        filename = rekam_suara(16000, 2)
        indicator_lamp.off()
        mfccs = ekstraksiFiturMFCC(filename)
        mfccToCSV(mfccs)
        prediksiInput(file_mfcc_csv)

        # Tunggu 5 detik sebelum iterasi berikutnya
        time.sleep(5)