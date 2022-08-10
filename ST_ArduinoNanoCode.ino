/*
  Arduino LSM9DS1 - Adapted from Simple Accelerometer

  This example reads the acceleration values from the LSM9DS1
  sensor and continuously prints them to the Serial Monitor
  or Serial Plotter.

  The circuit:
  - Arduino Nano 33 BLE Sense
*/
#include <PDM.h>
// this library is for reading PDM signals
// See: https://www.arduino.cc/en/Reference/PDM
//
#include <Arduino_LSM9DS1.h>
// this library allows you to read the 3-axes of XL, gyro, mag
// connection is by I2C on nano board
// values returned are signed floats
// the library sets sensor initialization
// XL range is +/- 4g at 104 Hz, gyro +/- 2000 dps at 104 Hz, mag +/- 400 uT at 20 Hz
// It is possible to grab the Arduino.LSM9DS1.h code and make adjustments if needed

// add timing
unsigned long timer = 0;    // used to check current time [microseconds]
long loopTime = 0;       // default time between updates, but will be set in python Code [microseconds]
bool initLooptime = false;  // boolean (T/F) to check if loop time has already been set
bool stopProgram = false;

// in our DSC code, we initialize values to zero and as int
// signed floats in c++ are 4 bytes
float x = 0;
float y = 0;
float z = 0;
float wx = 0;
float wy = 0;
float wz = 0;
float bx = 0;
float by = 0;
float bz = 0;
float xo = 0;
float yo = 0;
float zo = 0;
float wxo = 0;
float wyo = 0;
float wzo = 0;
float bxo = 0;
float byo = 0;
float bzo = 0;

// The next lines are for sound measurement from on-board microphone
// buffer to read samples from microphone, each sample is 16-bits
short sampleBuffer[256];
float rms;

// number of samples read
volatile int samplesRead;

void setup() {
  Serial.begin(9600); // default 9600; can it be higher?
  // if using I2C, add: Wire.begin();
//  while (!Serial);
//  Serial.println("Started");
//
//  if (!IMU.begin()) {
//    Serial.println("Failed to initialize IMU!");
//    while (1);
//  }
  if (IMU.begin() == false){ // Waits until device connection is made
    while(1);
  }  
  // initialize basic settings?  
  timer = micros(); // start timer - we may not need this if we have loop interval
  // change ranges?

  // can change settings on range of sensors
  // e.g., IMU.setXLRange(2) could be a command that sets the FS range on the accelerometer
  // may want to do similar setup on gyro, magnetometer, etc.
  // anything needed on digital microphone?
  // need description of IMU functions available
  // arduino.cc/en/Reference/ArduinoLSM9DS1
  // -begin()
  // -end()
  // -readAcceleration()
  // -readGyroscope()
  // -accelerationAvailabe()
  // -accelertaionSampleRate() - returns sample rate
  // -gyroscopeSampleRate()
  // -readMagneticField()
  // -magneticFieldSampleRate()
  // -magneticFieldAvailble()

  // configure the data receive callback for PDM use (microphone)
  PDM.onReceive(onPDMdata); // void onPDMdata() is a function defined below

  // optionally set the gain, defaults to 20
  // PDM.setGain(30);

  // initialize PDM with:
  // - one channel (mono mode)
  // - a 16 kHz sample rate
  if (!PDM.begin(1, 16000)) {
    Serial.println("Failed to start PDM!");
    while (1);
  }
  rms = 0; // zero the rms variable

  // end of setup()
}

void loop() {
  if (Serial.available() > 0) {       // if data is available
    String str = Serial.readStringUntil('\n');
    readFromPC(str);
  }
  if (initLooptime && !stopProgram)      // once loop time has been initialized
  {
    timeSync(loopTime); // sync up time to match data rate
    unsigned long currT = micros(); // get current time
    // try just a read
//    IMU.readAcceleration(x, y, z);
//    IMU.readGyroscope(wx, wy, wz);
    
    sendToPC(&currT);
    // original example code
    if (IMU.accelerationAvailable()) {
      IMU.readAcceleration(x, y, z);
      sendToPC(&x);
      sendToPC(&y);
      sendToPC(&z);
    }
    else
    {
      sendToPC(&xo); // not really needed here 
      sendToPC(&yo);
      sendToPC(&zo);      
    }
    if (IMU.gyroscopeAvailable()) {
      IMU.readGyroscope(wx, wy, wz);
      sendToPC(&wx);
      sendToPC(&wy);
      sendToPC(&wz);
    }
    else
    {
      sendToPC(&wxo); // not really needed here
      sendToPC(&wyo);
      sendToPC(&wzo);       
    }

    if (IMU.magneticFieldAvailable()) {
      IMU.readMagneticField(bx, by, bz);
      sendToPC(&bx);
      sendToPC(&by);
      sendToPC(&bz);
      // this is needed for magnetometer - slower rate
      bxo = bx; // assign value to 'hold' variables
      byo = by; // assign value to 'hold' variables
      bzo = bz; // assign value to 'hold' variables
    }
    else
    {
      sendToPC(&bxo); // if not ready, zero-order hold
      sendToPC(&byo); // if not ready, zero-order hold
      sendToPC(&bzo); // if not ready, zero-order hold       
    }
    // tool motor current sensing - analog input
    // can insert calibration factor if desired
    int sensorValue = analogRead(A0); // reading from current sensor
    float Isens = sensorValue * (3.3 / 1023.0); // this is a voltage proportional to current
    sendToPC(&Isens); 

    // Sound capture - first attempt doing this along with all other sensors
    // wait for samples to be read
    if (samplesRead) {
      // print samples to the serial monitor or plotter
      }
      // the following is a crude RMS estimate of the sound level
      // can improve, but seems to track output from a sound level meter (SLM)
      // analog output, so reasonable
      // actual SLM dB outputs are weighted by filters
      for (int i = 0; i < samplesRead; i++) {
        rms = rms + (sampleBuffer[i])*(sampleBuffer[i]);
        }
      rms = sqrt(rms);
      sendToPC(&rms);
      
  }
  else if (initLooptime && stopProgram)
  {
    // do nothing
    //IMU.end(); // done with the IMU
  }

  // end of loop()
}

// The rest of this was added from our DSC code to allow timing and communications via serial
// Inserted 10-12-21 without modification (RGL)

/*
 * Timesync calculates the time the arduino needs to wait so it 
 * outputs data at the specified rate
 * Input: deltaT - the data transfer period in microseconds
 */
void timeSync(unsigned long deltaT)
{
  unsigned long currTime = micros();  // get current time
  long timeToDelay = deltaT - (currTime - timer); // calculate how much time to delay for [us]
  
  if (timeToDelay > 5000) // if time to delay is large 
  {
    // Split up delay commands into delay(milliseconds)
    delay(timeToDelay / 1000);

    // and delayMicroseconds(microseconds)
    delayMicroseconds(timeToDelay % 1000);
  }
  else if (timeToDelay > 0) // If time to delay is positive and small
  {
    // Use delayMicroseconds command
    delayMicroseconds(timeToDelay);
  }
  else
  {
      // timeToDelay is negative or zero so don't delay at all
  }
  timer = currTime + timeToDelay;
}


void readFromPC(const String input)
{
  // "r,50"
  int commaIndex = input.indexOf(',');
  char command = input.charAt(commaIndex - 1);
  String data = input.substring(commaIndex + 1);    
  int rate = 0;
  switch(command)
  {
    case 'r':
      // rate command
      rate = data.toInt();
      loopTime = 1000000/rate;         // set loop time in microseconds to 1/frequency sent
      initLooptime = true;             // no longer check for data
      timer = micros();
      break;
    case 's':
      // stop command
      stopProgram = true;
      break;
    default:
    // Otherwise, do nothing
      break;
  
  }

}

// ------------------------------------------------------------------------------------------------------------
// Send Data to PC: Methods to send different types of data to PC
// ------------------------------------------------------------------------------------------------------------

void sendToPC(int* data)
{
  byte* byteData = (byte*)(data);
  Serial.write(byteData, 2);
}

void sendToPC(float* data)
{
  byte* byteData = (byte*)(data);
  Serial.write(byteData, 4);
}
 
void sendToPC(double* data)
{
  byte* byteData = (byte*)(data);
  Serial.write(byteData, 4);
}

void sendToPC(unsigned long* data)
{
  byte* byteData = (byte*)(data);
  Serial.write(byteData, 4);
}

void onPDMdata() {
  // query the number of bytes available
  int bytesAvailable = PDM.available();

  // read into the sample buffer
  PDM.read(sampleBuffer, bytesAvailable);

  // 16-bit, 2 bytes per sample
  samplesRead = bytesAvailable / 2;
}
