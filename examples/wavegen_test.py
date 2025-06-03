from time import sleep

import scientific_instrument_tools as sit

sit.ResourceManager.list_resources()
print(sit.ResourceManager.resource_tab())

res = sit.ResourceManager.list_resources()[0]
wavegen = sit.ScientificInstrumentFactory.make_waveform_generator(res)
wavegen.connect()

# Square signal
wavegen.set_output(False)
wavegen.set_function("sqr")
wavegen.set_voltage(4)
wavegen.set_frequency(10e3)
wavegen.set_duty_cycle(40)
wavegen.set_output(True)
sleep(2)

# Sinus signal
wavegen.set_output(False)
wavegen.set_function("sin")
wavegen.set_period(10e-6)
wavegen.set_voltage(3.1, 1.2, "HL")
wavegen.set_output(True)
sleep(2)

# DC signal
wavegen.set_output(False)
wavegen.set_function("dc")
wavegen.set_voltage(1, 5)
wavegen.set_output(True)
sleep(2)

# Pulse signal
wavegen.set_output(False)
wavegen.set_function("pulse")
wavegen.set_voltage(4)
wavegen.set_frequency(500)
wavegen.set_width(200e-6)
wavegen.set_output(True)
sleep(2)

# Burst mode
wavegen.set_output(False)
wavegen.set_function("sin")
wavegen.set_period(10e-6)
wavegen.set_voltage(1)
wavegen.set_burst(True)
wavegen.set_burst_ncycles(1)
wavegen.set_burst_period(1)
wavegen.set_burst(False)
wavegen.set_trig_ext(True)

wavegen.disconnect()

sit.ResourceManager.close()
