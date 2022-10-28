
// Define the number of samples to keep track of. The higher the number, the
// more the readings will be smoothed, but the slower the output will respond to
// the input. Using a constant rather than a normal variable lets us use this
// value to determine the size of the readings array.
const int windowlength = 10;
float window[windowlength];
float prev_window[windowlength];
int k = 0;
int i = 0;
int z = 0;
int v = 0;

float average,prev_average = 0;                // the average
int inputPin = A0;
int y = 0;
float timeindex;
float myTime,myprevTime;
int toolstatus;
int st,sp,wst,wsp;
#define GREEN 23
#define RED 22  
#define BLUE 24



void setup() {
  // initialize serial communication with computer:
  Serial.begin(9600);
  
  //initialize the digital Pin as an output
  digitalWrite(GREEN,HIGH);
  digitalWrite(RED,LOW);
  digitalWrite(BLUE,HIGH);
  // Initialize tool status
  toolstatus = 0;
}

void loop() {
  //Create previous window array 
  for(z=0;z<windowlength;z++){
      prev_window[z]=window[z];
  }
  //Redefine window by populating elements from shifted previous window array
  for(v=0;v<windowlength-1;v++){
      window[v]=prev_window[v+1];
  }
  //Populate rightmost value of new window array with newly read sensor value
  window[windowlength-1]=analogRead(A0);


  //calculate the average:
  prev_average = average;
  Serial.print("Prev Average: ");
  Serial.print(average);
  Serial.print(" ");
  average = av(window,windowlength);
  Serial.print("Current Average: ");
  Serial.print(average);
  Serial.print(" ");
  Serial.print("instantanteous value: ");
  Serial.print(analogRead(A0));
  

/////////////////////////// Smart tools logic///////////////////////////////// 



  //Tool status:
  // 0: off
  // 1: on (idling) 
  // 2: working 

  
  //Identify start time
  float start_ll = 10;
  if ((prev_average <= start_ll) and (average > start_ll)){
    st++;
    toolstatus=1;
    digitalWrite(RED,HIGH); // Turn off red LED
    digitalWrite(GREEN,LOW); // Turn on green LED
  }
  Serial.print(" Number of Starts: ");
  Serial.print(st);

  //Identify stop time
  float stop_ll = 60;
  if ((average <= stop_ll) and (prev_average > stop_ll)){
    sp++;
    toolstatus=0;
    digitalWrite(GREEN,HIGH); // Turn off green LED
    digitalWrite(RED,LOW); // Turn on red LED
  }
  Serial.print(" Number of Stops: ");
  Serial.println(sp);
  delay(7.8);
  

//  //for printing array
//  unsigned int j; 
//  Serial.print("Array: ");
//  for(j=0;j<numReadings;j++){
//        Serial.print(readings[j]);
//        Serial.print(" ");
//      }
//   Serial.print(" ");

   
//// Sampling frequency:
//    myprevTime = myTime;
//    myTime = millis();
//    float delta;
//    delta=(myTime-myprevTime)/1000;
//    float freq;
//    freq= 1/delta;
//    Serial.print("  freq: ");
//    Serial.println(freq);

}

//////////////////////////Functions/////////////////////////////
int j;
float av(float data[], int sample_length){
  int n = sample_length;
  float dsum,ave;
  //reset values
  dsum=0;
  ave=0;
  //Calculate Average
  for (j=0;j<n;j++) dsum += data[j];
  ave=dsum/n;
  return(ave);
}
