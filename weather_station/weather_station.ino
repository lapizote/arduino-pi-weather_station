#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Adafruit_BMP085.h>
#include <DHT.h>

const int lcd_address = 0x27; //address is either 0x27 or 0x3F

DHT dht(2, DHT22); //(pin, type); type is either DHT11, DHT22, DHT21
LiquidCrystal_I2C lcd(lcd_address, 16, 2); //(address, columns, rows)
Adafruit_BMP085 bmp;

void displayText(String top, String bottom) {
  //note, this will cut off at a row string is longer than 16 characters
  lcd.setCursor(0,0);
  lcd.print(top);
  lcd.setCursor(0,1);
  lcd.print(bottom);
}

void setup() {
  //setup serial
  Serial.begin(9600);
  Serial.println("--- Arduino Weather Station ---");

  //setup LCD
  Serial.println("Setting up LCD...");

  lcd.init();
  lcd.backlight();
  displayText("Weather Station", "by: Axl & Gian");

  //setup BMP180 & DHT22
  Serial.println("Setting up DHT22 and BMP180...");
  if (!bmp.begin()) { Serial.println("Error in initializing BMP180 sensor."); }
  else { Serial.println("Setting up BMP180 done!"); }

  Serial.println("Setting up DHT22 done!");
}

void loop() {
  //read DHT22 data
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();
  if (isnan(humidity)) {Serial.println("DHT22 ERROR: Failed to read humidity!"); humidity = -99; }
  if (isnan(temperature)) {Serial.println("DHT22 ERROR: Failed to read temperature!"); temperature = -99; };

  //read BMP180 data
  float pressure = bmp.readPressure();
  if (isnan(pressure)) {Serial.println("BMP180 ERROR: Failed to read air pressure!"); pressure = 0; }

  lcd.clear();
  String top_text = "H: " + String(humidity) + " T: " + String(temperature);
  String bottom_text = "P: " + String(pressure/101325, 3) + " atm";
  displayText(top_text, bottom_text);

  delay(5000); //dht22 requires 2 seconds of delay, but we'll just do it at 5 seconds since it doesnt need to be reading that often

  
  
}
