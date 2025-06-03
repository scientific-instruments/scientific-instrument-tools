# -*- coding: utf-8 -*-

from ..core import ScientificInstrument, ResourceItem
from math import sqrt, log

class WaveformGenerator(ScientificInstrument):
    """Generic class for Waveform Generators."""

    def __init__(self, resource: ResourceItem):
        self._output = False
        self._function = None
        self._frequency = None
        self._voltage_amplitude = None
        self._voltage_offset = None
        self._duty_cycle = None
        self._symmetry = None
        
        super().__init__(resource)

    def set_output(self, output: bool = True) -> None:
        self._output = output

    def set_function(self, function: str) -> None:
        if "SIN" in function.upper():
            self._function = "SINUS"
        elif "SQ" in function.upper():
            self._function = "SQUARE"
        elif "RAMP" in function.upper():
            self._function = "RAMP"
        elif "PULS" in function.upper():
            self._function = "PULSE"
        elif "NOIS" in function.upper():
            self._function = "NOISE"
        elif "DC" in function.upper() or "CST" in self._function.upper():
            self._function = "DC"
        elif "USER" in function.upper():
            self._function = "USER"
        else:
            raise NotImplementedError()

    def set_frequency(self, frequency: float) -> None:
        self._frequency = frequency

    def set_period(self, period: float) -> None:
        self.set_frequency(1/period)

    def set_voltage(self, a: float, b: float = 0, mode: str = "AO") -> None:
        if mode == "AO":
            self._voltage_amplitude = a
            self._voltage_offset = b
        elif mode == "HL":
            self._voltage_amplitude = abs(a - b)
            self._voltage_offset = (a + b)/2
        else:
            raise NotImplementedError(mode + "mode is not implemented. Please choose 'AO' or 'HL'")

    def set_duty_cycle(self, duty_cycle: float) -> None:
        self._duty_cycle = duty_cycle

    def set_width(self, width: float) -> None:
        self.set_duty_cycle(100*width*self._frequency)

    def set_symmetry(self, symmetry: float) -> None:
        self._duty_cycle = symmetry

    def get_error(self) -> (int, str):
        raise NotImplementedError()

    def check_error(self) -> None:
        raise NotImplementedError()


class WaveformGeneratorKeysight(WaveformGenerator):
    """Generic class for Keysight Waveform Generators."""

    def __init__(self, resource: ResourceItem):
        super().__init__(resource)

    def set_output(self, output: bool = True) -> None:
        super().set_output(output)
        if output:
            self.visa.write('OUTPUT ON')
        else:
            self.visa.write('OUTPUT OFF')

    def set_function(self, function: str) -> None:
        super().set_function(function)
        function_dict = {"SINUS": "SIN",
                         "SQUARE": "SQU",
                         "RAMP": "RAMP",
                         "PULSE": "PULS",
                         "NOISE": "NOIS",
                         "DC": "DC",
                         "USER": "USER"}
        self.visa.write("FUNC " + function_dict[self._function])
        self.check_error()

    def set_frequency(self, frequency: float) -> None:
        super().set_frequency(frequency)
        self.visa.write("FREQ {}".format(self._frequency))
        self.check_error()

    def set_voltage(self, a: float, b: float = 0, mode: str = "AO") -> None:
        super().set_voltage(a, b, mode)
        self.visa.write("VOLT:OFFS {}".format(self._voltage_offset))
        self.visa.write("VOLT {}".format(self._voltage_amplitude))
        self.check_error()

    def set_duty_cycle(self, duty_cycle: float) -> None:
        super().set_duty_cycle(duty_cycle)
        if self._function == "PULSE":
            self.visa.write("FUNC:PULS:DCYC {}".format(self._duty_cycle))
        elif self._function == "SQUARE":
            self.visa.write("FUNC:SQU:DCYC {}".format(self._duty_cycle))
        else:
            raise NotImplementedError("Duty cycle does not exist for {} function. Please choose 'PULSE' or 'SQUARE'".format(self._function))
        self.check_error()

    def set_symmetry(self, symmetry: float) -> None:
        super().set_duty_cycle(symmetry)
        self.visa.write("FUNC:RAMP:SYMM {}".format(self._symmetry))
        self.check_error()

    def get_error(self) -> (int, str):
        code, msg = self.visa.query("SYST:ERR?").replace('"', '').replace("\n", '').split(",")
        return int(code), str(msg)

    def check_error(self) -> None:
        code, msg = self.get_error()
        if code == 0:
            return
        elif -code // 100 == 2: # Error code -2XX
            print("[Warning] Waveform Generator Keysight Error : " + msg)
        else:
            raise RuntimeError("Waveform Generator Keysight Error : " + msg)
