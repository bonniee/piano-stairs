

void setup() {
  Serial.begin(9600);
  calibrate();
}

float analogPins[] = {0, 1, 2, 3, 4, 5};
int numAnalogPins = 6;
int thresholds[6];
float percentThresh = 1.02;
int absoluteThresh = 40;

void calibrate() {
  int maxSteps = 10;  
  for (int curStep = 0; curStep < maxSteps; curStep++) {
    for (int pin = 0; pin < numAnalogPins; pin++) {
       thresholds[pin] += analogRead(analogPins[pin]);   
    }
  }
  for (int pin = 0; pin < numAnalogPins; pin++) {
    thresholds[pin] = thresholds[pin] / maxSteps;
  }
  
}

int reCalibrate = 50;
int loopCount = 0;

void loop() {
  
  for (int i = 0; i < numAnalogPins; i++) {
    int val = analogRead(analogPins[i]);
    if (val > thresholds[i] + absoluteThresh) {
      Serial.print(1);
    }
    else {
      Serial.print(0);
    }
  }
  Serial.println();
  delay(250);
  
//  loopCount = loopCount + 1;
//  if (loopCount >= reCalibrate) {
//    //Serial.println("calibrating");
//    //calibrate();
//    loopCount = 0;
//  }

}
