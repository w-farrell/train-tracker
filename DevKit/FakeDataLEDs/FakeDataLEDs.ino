#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "WFarrell";
const char* password = "mynameiswill";
const char* apiKey = "32873f6871244285b19ea056b65a2d25";
const char* apiUrl = "http://lapi.transitchicago.com/api/1.0/ttpositions.aspx";

const int NUM_STATIONS = 5;
const int LED_PINS[NUM_STATIONS] = {13, 12, 14, 27, 26};
const char* STATION_NAMES[NUM_STATIONS] = {"Howard", "Belmont", "Fullerton", "Grand", "Roosevelt"};

bool trainAtStation[NUM_STATIONS] = {false, false, false, false, false};

void setup() {
  Serial.begin(115200);
  for (int i = 0; i < NUM_STATIONS; i++) {
    pinMode(LED_PINS[i], OUTPUT);
  }

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    updateTrainPositionsFromAPI();
    updateLEDs();
    printTrainPositions();
  }
  
  delay(15000);  // Update every 2 seconds
}

void updateTrainPositionsFromAPI() {
  HTTPClient http;
  String url = String(apiUrl) + "?key=" + apiKey + "&rt=Red&outputType=JSON";
  
  http.begin(url);
  int httpResponseCode = http.GET();
  
  if (httpResponseCode > 0) {
    String payload = http.getString();
    DynamicJsonDocument doc(8192);
    deserializeJson(doc, payload);
    
    // Reset all stations
    for (int i = 0; i < NUM_STATIONS; i++) {
      trainAtStation[i] = false;
    }
    
    // Update based on API data
    JsonArray trains = doc["ctatt"]["route"][0]["train"];
    for (JsonObject train : trains) {
      String nextStation = train["nextStaNm"].as<String>();
      for (int i = 0; i < NUM_STATIONS; i++) {
        if (nextStation == STATION_NAMES[i]) {
          trainAtStation[i] = true;
          break;
        }
      }
    }
  }
  
  http.end();
}

void updateLEDs() {
  for (int i = 0; i < NUM_STATIONS; i++) {
    digitalWrite(LED_PINS[i], trainAtStation[i] ? HIGH : LOW);
  }
}

void printTrainPositions() {
  Serial.println("Current train positions:");
  for (int i = 0; i < NUM_STATIONS; i++) {
    Serial.print(STATION_NAMES[i]);
    Serial.print(": ");
    Serial.println(trainAtStation[i] ? "Train present" : "No train");
  }
  Serial.println();
}