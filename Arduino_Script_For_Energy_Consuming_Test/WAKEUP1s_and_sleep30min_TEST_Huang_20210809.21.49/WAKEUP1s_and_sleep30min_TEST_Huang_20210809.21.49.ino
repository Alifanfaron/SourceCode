//When using the function of ESP.deepSleep(): once the code uploaded to ESP board, RST shall connect to D0 immediately
// Feather HUZZAH ESP8266 note: use pins 3, 4, 5, 12, 13 or 14 -- 
// Pin 15, 8, 7, 6 can work but DHT must be disconnected during program upload. 






/*
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include "max6675.h"
int ktcSO = 7; //choose the Data Channel - choose the Pin #
int ktcCS = 6;
int ktcCLK = 5;
MAX6675 robojax(ktcCLK, ktcCS, ktcSO);
//input your SSID & Password
const char* ssid = "Hubert";  // Enter SSID here
const char* password = "ceshen1532";  //Enter Password here
*/










//Alert Range for the severe change of Temp, and other variable
float TempDiffAlert = 4.80; //Alert for the sharp change of degree centigrade (default value would better be 4.80℃)
float HIGH_TEMP = 40.0; //the high temp that the alert will happen (default is 40℃), Alert for the high Temp of degree centigrade

int statusFlag = 1;
// statusFlag = 0 → Go to active status
// statusFlag = 1 → Go to deepSleep Circle (test-default-value of DutyCycle is 60sec) 




float Temperature;
float TempDetect1=-888.88;
float TempDetect2=-999.99;
float DangerDetectInterval = 1.00; //second, DangerDetectInterval's (default value would better be 1.00 sec)

int SensorNum = 3; //Number of the sensors, SensorNum's test-default-value would better be 3
int DutyCycleSec = 60; //second - the time duration for every dutycycle, and DutyCycleSec's test-default-value would better be 60s





int PresetAwakeTimeTimeMillisecond = (int)(((float)DutyCycleSec/(float)SensorNum)*1000.0+0.5);
int PresetWakeUpTimeSec = (int)(((float)DutyCycleSec)/((float)SensorNum)+0.5);






void GoToDeepSleep(){
  int DeepSleepMillisecond = (1000*DutyCycleSec - millis());//"millis()" is the time of how long the program has gone through started from every ReSeT
  int PresetSleepTimeSec = (int)(((float)(DeepSleepMillisecond))/1000.0+0.5);
  int SleepTimeRandomFactor = random(0,(int)(((float)DutyCycleSec)/((float)SensorNum)/2.0+0.5));
  
  uint64_t ONE_SEC_64_t=(1e6); //setting up a ESP.deepSleep needs the format of "uint64_t"
  uint64_t SleepTime = (uint64_t)((PresetSleepTimeSec+SleepTimeRandomFactor)*ONE_SEC_64_t);
  
  Serial.print("Going to sleep for time: ");
  Serial.print(PresetSleepTimeSec+SleepTimeRandomFactor);
  Serial.println(" sec.");
  ESP.deepSleep(SleepTime); //When using the function of ESP.deepSleep(): once the code uploaded to ESP board, RST shall connect to D0 immediately
}



void ConnectWiFi(){
delay(random(3000,15000)); //for test
}

void UploadDataToBasestation(){
delay(random(1000,3000)); //for test
}


void StayAwakeAndDoSomethingUntilDangerDismiss(){
UploadDataToBasestation();  //for test
delay(random(30000,40000)); //for test
}




float ReadCelsius(){
  //float DC = robojax.readCelsius(); // Read temperature as Celsius
  float DC = -777.77 + ((float)random(0,100))/100.0; //for test
  return DC;
}


void ReadTemp(){
  //Detecting_Function and ESP_Webserver
TempDetect1 = ReadCelsius();
delay((int)(DangerDetectInterval*1000.00));
TempDetect2 = ReadCelsius();
}









//setup function
void setup() {
  Serial.begin(9600);
  delay(100);







// 【CODE INSERTION↓:】 wake up time: 1 sec AND sleep time random 20 to 30 sec
while (1)
{
  Serial.println("Before the 1 sec delay ①!");
  Serial.println("Before the 1 sec delay ②!");
  Serial.println("Before the 1 sec delay ③!");
  delay(1000-100); //THIS reprensents for the wake up time: 1 sec
  Serial.println("After the 1 sec delay ①!");
  Serial.println("After the 1 sec delay ②!");
  Serial.println("After the 1 sec delay ③!");
  int PresetSleepTimeSec_TEST = 1798;
  int SleepTimeRandomFactor_TEST = random(0,2);
  uint64_t ONE_SEC_64_t=(1e6); //setting up a ESP.deepSleep needs the format of "uint64_t"
  uint64_t SleepTime_TEST = (uint64_t)((PresetSleepTimeSec_TEST+SleepTimeRandomFactor_TEST)*ONE_SEC_64_t);
  Serial.print("Going to sleep for time: ");
  Serial.print(PresetSleepTimeSec_TEST+SleepTimeRandomFactor_TEST);
  Serial.println(" sec.");
  ESP.deepSleep(SleepTime_TEST); //When using the function of ESP.deepSleep(): once the code uploaded to ESP board, RST shall connect to D0 immediately
  }
// 【CODE INSERTION↑:】 wake up time: 1 sec AND sleep time random 20 to 30 sec















  
  Serial.println("[Connecting to WiFi...]");
  ConnectWiFi();
}





//loop function
void loop() {


ReadTemp();

if (TempDetect1-TempDetect2>TempDiffAlert || TempDetect2-TempDetect1>TempDiffAlert||TempDetect1>HIGH_TEMP)
{statusFlag=0;}
else
{statusFlag=1;}




if (statusFlag==0)
{
Serial.print("Wake up time (Alerted MODE): ");
Serial.print(PresetWakeUpTimeSec); 
Serial.println(" sec.");

Serial.print("Duration of wakeup (Alerted MODE): ");
Serial.print(((float)millis())/1000.00); Serial.println(" sec.");

Serial.print("Temperature report (Alerted MODE): ");
Serial.print(TempDetect2); Serial.println(" °C.");

while (statusFlag==0)
{
StayAwakeAndDoSomethingUntilDangerDismiss();
if (!(TempDetect1-TempDetect2>TempDiffAlert || TempDetect2-TempDetect1>TempDiffAlert)||(TempDetect1>HIGH_TEMP))//to decide whether to dismiss the ALERT MODE
{statusFlag=1;}
}
}



if(statusFlag==1)
{

Serial.print("Wake up time: ");
Serial.print(PresetWakeUpTimeSec); 
Serial.println(" sec.");

Serial.print("Duration of wakeup: ");
Serial.print(((float)millis())/1000.00); Serial.println(" sec.");

Serial.print("Temperature report: ");
Serial.print(TempDetect2); Serial.println(" °C.");

Serial.println("[sending data]");
UploadDataToBasestation();

if (PresetAwakeTimeTimeMillisecond<=millis())
{GoToDeepSleep();}

}










  
}
