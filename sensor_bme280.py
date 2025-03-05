import smbus2
import bme280

port = 1
address = 0x76
bus = smbus2.SMBus(port)

calibration_params = bme280.load_calibration_params(bus, address)
data = bme280.sample(bus, address, calibration_params)


print("bme280_temp %.2f" % data.temperature)
print("bme280_pressure %.2f" % data.pressure)
print("bme280_humidity %.2f" % data.humidity)