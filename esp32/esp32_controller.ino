#define GREEN_LED 12
#define YELLOW_LED 13
#define BLUE_LED 15

String command = "";

void setup() {
  Serial.begin(115200);

  pinMode(GREEN_LED, OUTPUT);
  pinMode(YELLOW_LED, OUTPUT);
  pinMode(BLUE_LED, OUTPUT);

  // Initialize all LEDs to OFF
  resetLEDs();

  Serial.println("ESP32 Brain Tumor LED Controller Ready");
}

void resetLEDs() {
  digitalWrite(GREEN_LED, LOW);
  digitalWrite(YELLOW_LED, LOW);
  digitalWrite(BLUE_LED, LOW);
}

void loop() {
  if (Serial.available()) {
    command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "INVALID") {
      resetLEDs();
      Serial.println("Invalid Image - All LEDs OFF");

    } else if (command == "NORMAL") {
      resetLEDs();
      digitalWrite(GREEN_LED, HIGH);
      Serial.println("Normal Brain - GREEN LED ON");

    } else if (command == "GLIOMA") {
      resetLEDs();
      digitalWrite(YELLOW_LED, HIGH);
      Serial.println("Glioma Detected - YELLOW LED ON");

    } else if (command == "MENINGIOMA") {
      resetLEDs();
      digitalWrite(BLUE_LED, HIGH);
      Serial.println("Meningioma Detected - BLUE LED ON");

    } else if (command == "PITUITARY") {
      resetLEDs();
      // Combine Yellow and Blue for Pituitary
      digitalWrite(YELLOW_LED, HIGH);
      digitalWrite(BLUE_LED, HIGH);
      Serial.println("Pituitary Detected - YELLOW & BLUE LEDs ON");
    }
  }
}