

void setup() {
  Serial.begin(9600);
  calibrate();
}

float analogPins[] = {0, 1, 2, 3, 4, 5};
int numAnalogPins = 6;
int thresholds[6];
float percentThresh = 1.03;
int absoluteThresh = 20;

int sensorHistory[6][10];
int bufferIndex = 0;

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
  
  for (int i = 0; i < 6; i++) {
    for (int j = 0; j < 10; j++) {
       sensorHistory[i][j] = thresholds[i];
    }
  }
  
}

void loop() {
  
  for (int i = 0; i < numAnalogPins; i++) {
    int val = analogRead(analogPins[i]);
    //Serial.println(val);
    int oldAvg = 0;
    for (int j = 0; j < 10; j++) {
      oldAvg += sensorHistory[i][j];
    }
    oldAvg = oldAvg / 10;
//    Serial.print(oldAvg);
//    Serial.print(";");
//    Serial.print(val);
//    Serial.print(";");
//    Serial.print(bufferIndex);
//    Serial.println();
    if (val > oldAvg + absoluteThresh) {
       Serial.print(1);
    }
    else {
      Serial.print(0);
    }
    sensorHistory[i][bufferIndex] = val;
    //if (val > thresholds[i] * percentThresh) {
//    if (val > thresholds[i] + absoluteThresh) {
//      Serial.print(1);
//    }
//    
//    else {
//      Serial.print(0);
//    }
   }
  bufferIndex = (bufferIndex + 1) % 10;
  Serial.println();
  delay(40);
}
