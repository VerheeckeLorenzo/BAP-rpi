from flask import Flask, jsonify
import Adafruit_DHT
import spidev
import time
from gpiozero import MCP3008

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4  # GPIO pin number

SPI_PORT = 0
SPI_DEVICE = 0
spi = spidev.SpiDev()
spi.open(SPI_PORT, SPI_DEVICE)

# LDR is connected to MCP channel 1
divider = MCP3008(1)

app = Flask(__name__)

def read_data():
    values = {}
    try:
        # Read temperature and humidity from DHT11 sensor
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        
        ldr_value = divider.value
        values['ldr'] = round(ldr_value*100,2)
        print(f'LDR Value: {ldr_value*100}')
        if humidity is not None and temperature is not None:
            values['temp'] = temperature
            values['humidity'] = humidity
            print(f'Temperature: {temperature:.1f}°C | Humidity: {humidity:.1f}%')
        else:
            print('Failed to retrieve DHT11 data')
        
        print(f'Light Intensity: {ldr_value}')
        
    except KeyboardInterrupt:
        print('Exiting...')
    except Exception as e:
        print(f'Error: {e}')
    return values
    time.sleep(2)  # delay

@app.route('/sensor-data', methods=['GET'])
def get_sensor_data():
    sensor_data = read_data()
    return jsonify(sensor_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
