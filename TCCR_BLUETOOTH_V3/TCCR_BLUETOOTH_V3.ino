// Deklarasi pin motor
int NA1 = 3;
int NA2 = 11;
const int motorPin1 = A0;
const int motorPin2 = A1;
const int motorPin3 = A2;
const int motorPin4 = A3;
bool TANDA = false;
char receivedData[256];  // buat array dengan ukuran cukup besar
int receivedDataNumbers[256];  // array untuk menyimpan angka yang diterima
int dataSize = 0;  // variabel untuk menyimpan ukuran data yang akan diterima
int index = 0;  // variabel untuk melacak berapa banyak item telah ditambahkan ke array

void setup() {
  // Mengatur pin sebagai OUTPUT
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
  pinMode(motorPin3, OUTPUT);
  pinMode(motorPin4, OUTPUT);
  pinMode(NA1, OUTPUT);
  pinMode(NA2, OUTPUT);
  analogWrite(NA1, 50);
  analogWrite(NA2, 50);
  Serial.begin(9600);

  TCCR1A = 0;
  TCCR1B = 0B00000111;
  TCNT1 = 0;
  TIMSK1 = 0B00000010;

  interrupts();
  Serial.begin(9600);
}

void loop() {
  // cek apakah ada data yang masuk
  while (Serial.available() > 0) {
    // baca seluruh baris
    char line[256];
    Serial.readBytesUntil('\n', line, sizeof(line) - 1);

    // bagi baris menjadi instruksi berdasarkan koma
    char* instruction = strtok(line, ",");
    while (instruction != NULL) {
      // bagi setiap instruksi menjadi huruf dan angka
      receivedData[index] = instruction[0];
      receivedDataNumbers[index] = atoi(instruction + 1);

      // pergi ke instruksi berikutnya
      instruction = strtok(NULL, ",");
      index++;
    }

    // sekarang index adalah ukuran data
    dataSize = index;

    // jalankan fungsi sesuai data
    for(int i = 0; i < dataSize; i++) {
      char action = receivedData[i];
      int number = receivedDataNumbers[i];
      if(action == 'F') moveForward(number);
      else if(action == 'B') moveBackward(number);
      else if(action == 'L') turnLeft(number);
      else if(action == 'R') turnRight(number);
      else if(action == 'S') stop();
    }
    dataSize = 0;  // reset ukuran data untuk pengiriman data selanjutnya
    index = 0;  // reset index untuk pengiriman data selanjutnya
  }
  delay(1000);
}

ISR(TIMER1_COMPA_vect) {
  TANDA = true;
  digitalWrite(motorPin1, LOW);
  digitalWrite(motorPin2, LOW);
  digitalWrite(motorPin3, LOW);
  digitalWrite(motorPin4, LOW);
}

// Fungsi untuk mengontrol motor
void motorControl(int pin1, int pin2, int pin3, int pin4) {
  digitalWrite(motorPin1, pin1);
  digitalWrite(motorPin2, pin2);
  digitalWrite(motorPin3, pin3);
  digitalWrite(motorPin4, pin4);
}

void moveForward(int number) {
  TCNT1 = 0;
  OCR1A = 150*(number/10);
  motorControl(LOW, HIGH, LOW, HIGH);
  analogWrite(NA1, 130);
  analogWrite(NA2, 130);
  Serial.println("ini F dan OCR1A bernilai: " + String(OCR1A) + " - Atau Berjarak: " + String(number) + "cm");
  delay(1000);
}

void moveBackward(int number) {
  TCNT1 = 0;
  OCR1A = 150*(number/10);
  motorControl(HIGH, LOW, HIGH, LOW);
  analogWrite(NA1, 130);
  analogWrite(NA2, 130);
  Serial.println("ini B dan OCR1A bernilai: " + String(OCR1A) + " - Atau Berjarak: " + String(number) + "cm");
  delay(1000);
}

void turnLeft(int number) {
  TCNT1 = 0;
  if(number == 30) {
    OCR1A = 78;
  } else if (number == 45)
  {
    OCR1A = 102;
  } else if (number == 60)
  {
    OCR1A = 122;
  } else if (number == 90)
  {
    OCR1A = 154;
  }
  motorControl(LOW, HIGH, HIGH, LOW);
  analogWrite(NA1, 150);
  analogWrite(NA2, 150);
  Serial.println("ini L dan OCR1A bernilai: " + String(OCR1A) + " - Atau Berjarak: " + String(number) + " derajat");
  delay(1000);
}

void turnRight(int number) {
  TCNT1 = 0;
  if(number == 30) {
    OCR1A = 78;
  } else if (number == 45)
  {
    OCR1A = 102;
  } else if (number == 60)
  {
    OCR1A = 122;
  } else if (number == 90)
  {
    OCR1A = 154;
  }
  motorControl(HIGH, LOW, LOW, HIGH);
  analogWrite(NA1, 150);
  analogWrite(NA2, 150);
  Serial.println("ini R dan OCR1A bernilai: " + String(OCR1A) + " - Atau Berjarak: " + String(number) + " derajat");
  delay(1000);
}

void stop() {
  TCNT1 = 0;
  OCR1A = 0;
  motorControl(LOW, LOW, LOW, LOW);
  analogWrite(NA1, 150);
  analogWrite(NA2, 150);
  Serial.println("ini S dan OCR1A bernilai: " + String(OCR1A) + " - Dan Berhenti");
  delay(1000);
}