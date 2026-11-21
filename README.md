#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  delay(2000);

  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  if (isnan(humidity) || isnan(temperature)) {
    return;
  }

  // Python expects: temperature,humidity
  Serial.print(temperature);
  Serial.print(",");
  Serial.println(humidity);
}
```

## ThingSpeak setup

1. Create a free account at [ThingSpeak](https://thingspeak.com/).
2. Create a new channel.
3. Enable and name the fields:
   - Field 1: `Temperature (C)`
   - Field 2: `Humidity (%)`
4. Save the channel.
5. Open the **API Keys** tab and copy the **Write API Key**.

## Python setup

Install the Python packages:

```powershell
py -m pip install pyserial requests
```

Create `room_monitor.py` and add your ThingSpeak Write API Key. Change `COM3` if the Arduino appears on another port.

```python
import time
import serial
import requests

COM_PORT = "COM3"
BAUD_RATE = 9600
WRITE_API_KEY = "PASTE_YOUR_THINGSPEAK_WRITE_API_KEY_HERE"

arduino = serial.Serial(COM_PORT, BAUD_RATE, timeout=2)
time.sleep(2)

print("Reading DHT11 data and sending it to ThingSpeak...")

while True:
    line = arduino.readline().decode("utf-8", errors="ignore").strip()

    if "," not in line:
        continue

    try:
        temperature, humidity = line.split(",")
        temperature = float(temperature)
        humidity = float(humidity)

        response = requests.get(
            "https://api.thingspeak.com/update",
            params={
                "api_key": WRITE_API_KEY,
                "field1": temperature,
                "field2": humidity,
            },
            timeout=15,
        )

        if response.text != "0":
            print(f"Uploaded: {temperature} °C, {humidity} %")
        else:
            print("ThingSpeak rejected the update. Check the Write API Key.")

    except ValueError:
        print("Ignored invalid Arduino data:", line)
    except requests.RequestException as error:
        print("Internet upload error:", error)

    # ThingSpeak free accounts require at least 15 seconds between updates.
    time.sleep(20)
```

Run the script:

```powershell
py room_monitor.py
```

When the upload succeeds, the terminal shows an `Uploaded:` message. Open the ThingSpeak channel in any browser to see the charts.

## Important notes

- Close Arduino Serial Monitor before running the Python script; only one program can use the Arduino's COM port at a time.
- Keep the Arduino connected, the PC switched on, and `room_monitor.py` running for live updates.
- Do not commit or share your ThingSpeak Write API Key. Generate a new key if it is accidentally exposed.
- The free ThingSpeak plan accepts updates no faster than once every 15 seconds.

## License

This project is available under the MIT License.