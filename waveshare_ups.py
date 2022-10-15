from prometheus_client import Gauge

_gauges = {
    "load_voltage": Gauge("waveshare_load_voltage", "Load Voltage", ["device"]),
    "current": Gauge("waveshare_current", "Current", ["device"]),
    "power": Gauge("waveshare_power", "Power", ["device"]),
    "percent": Gauge("waveshare_percent", "Percent", ["device"]),
}


def extract_metrics(logger, ina219):

    bus_voltage = ina219.getBusVoltage_V()  # voltage on V- (load side)
    # voltage between V+ and V- across the shunt
    shunt_voltage = ina219.getShuntVoltage_mV() / 1000
    current = ina219.getCurrent_mA()  # current in mA
    power = ina219.getPower_W()  # power in W
    p = (bus_voltage - 6) / 2.4 * 100
    if p > 100:
        p = 100
    if p < 0:
        p = 0

    # INA219 measure bus voltage on the load side. So PSU voltage = bus_voltage + shunt_voltage
    # print("PSU Voltage:   {:6.3f} V".format(bus_voltage + shunt_voltage))
    # print("Shunt Voltage: {:9.6f} V".format(shunt_voltage))
    # print("Load Voltage:  {:6.3f} V".format(bus_voltage))
    # print("Current:       {:9.6f} A".format(current / 1000))
    # print("Power:         {:6.3f} W".format(power))
    # print("Percent:       {:3.1f}%".format(p))
    # print("")

    _gauges['load_voltage'].labels(device="Raspberry Pi 4").set(round(bus_voltage, 3))
    _gauges['current'].labels(device="Raspberry Pi 4").set(round(current / 1000, 6))
    _gauges['power'].labels(device="Raspberry Pi 4").set(round(power, 3))
    _gauges['percent'].labels(device="Raspberry Pi 4").set(round(p, 1))
