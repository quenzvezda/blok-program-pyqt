import serial
import time

ser = serial.Serial('COM3', 9600)  # ganti 'COM4' dengan port yang sesuai
time.sleep(2)  # memberi waktu untuk koneksi serial untuk membuka

with open('output.txt', 'r') as f:
    data = f.read().replace('\n', ',')  # baca file dan ganti newline dengan koma

ser.write(data.encode())  # kirim data
time.sleep(1)  # menunggu sedikit

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        print(line)

ser.close()  # tutup koneksi ketika selesai