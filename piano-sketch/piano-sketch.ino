/**
 * piano-sketch.ino
 * Author: Bonnie Eisenman
 *
 * Arduino-side code for taking in inputs from several sensors,
 * and if they pass the thresholds, send information to
 * Serial for processing.
 **/

void setup() {
  Serial.begin(9600);
  calibrate();
}

float analogPins[] = {0, 1, 2, 3, 4, 5};
int numAnalogPins = 6;
int thresholds[6];

// These values can be tuned depending on sensor installation.
float percentThresh = 1.03; // Not currently used
int absoluteThresh = 20; // The actual threshold value used

// Keep track of the last N x H sensor readings,
// where N = number of inputs
// and H = history length.
// This allows us to do smoothing.
int sensorHistory[6][10];

// This is used to cycle through the previous array
// along the H dimension.
int bufferIndex = 0;

void calibrate() {
  // How many steps' worth of data we use for calibration purposes
  int maxSteps = 10;

  // Begin by accumulating several steps' worth of baseline data
  for (int curStep = 0; curStep < maxSteps; curStep++) {
    for (int pin = 0; pin < numAnalogPins; pin++) {
       thresholds[pin] += analogRead(analogPins[pin]);   
    }
  }

  // Average out the baseline readings based on how many input readings we did
  for (int pin = 0; pin < numAnalogPins; pin++) {
    thresholds[pin] = thresholds[pin] / maxSteps;
  }
  
  // Fill the entire sensorHistory array with baseline data
  for (int i = 0; i < 6; i++) {
    for (int j = 0; j < 10; j++) {
       sensorHistory[i][j] = thresholds[i];
    }
  } 
}

void loop() {
  
  for (int i = 0; i < numAnalogPins; i++) {
    int val = analogRead(analogPins[i]);
    int oldAvg = 0;
    for (int j = 0; j < 10; j++) {
      oldAvg += sensorHistory[i][j];
    }
    oldAvg = oldAvg / 10;

    if (val > oldAvg + absoluteThresh) {
       Serial.print(1);
    }
    else {
      Serial.print(0);
    }
    sensorHistory[i][bufferIndex] = val;
   }
  bufferIndex = (bufferIndex + 1) % 10;
  Serial.println();
  delay(40);
}
