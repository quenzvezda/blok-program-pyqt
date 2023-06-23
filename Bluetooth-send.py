import serial
import time
import re

ser = serial.Serial('COM3', 9600)  # ganti 'COM4' dengan port yang sesuai
time.sleep(2)  # memberi waktu untuk koneksi serial untuk membuka

with open('output.txt', 'r') as f:
    lines = f.read().splitlines()  # baca file dan hapus newline di akhir setiap baris
    data = [[re.findall("[a-zA-Z]+", line)[0], re.findall("\d+", line)[0]] for line in lines]  # pisahkan huruf dan angka

ser.write(str(len(data)).encode())  # kirim ukuran array
time.sleep(1)  # menunggu sedikit

for pair in data:
    ser.write(pair[0].encode())  # kirim huruf
    time.sleep(1)
    ser.write(pair[1].encode())  # kirim angka
    time.sleep(1)

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        print(line)

ser.close()  # tutup koneksi ketika selesai
