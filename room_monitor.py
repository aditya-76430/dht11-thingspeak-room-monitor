import time
import serial
import requests

COM_PORT = "COM3"  # Change this to your Arduino port
BAUD_RATE = 9600
WRITE_API_KEY = "PASTE_YOUR_THINGSPEAK_WRITE_API_KEY_HERE"

arduino = serial.Serial(COM_PORT, BAUD_RATE, timeout=2)
time.sleep(2)

print("Reading DHT11 data and sending it to ThingSpeak...")

while True:
    line = arduino.readline().decode("utf-8", errors="ignore").strip()

    if line:
        print("Arduino says:", line)

    if "," not in line:
        continue

    # Arduino sends: temperature,humidity
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
                "field2": humidity
            },
            timeout=15
        )
        
        print("ThingSpeak:", response.status_code, response.text)

        if response.text != "0":
            print(f"Uploaded: {temperature} °C, {humidity} %")
        else:
            print("ThingSpeak rejected the update.")

    except ValueError:
        print("Ignored invalid Serial data:", line)
    except requests.RequestException as error:
        print("Internet upload error:", error)

    time.sleep(20)
    
    
    
    
