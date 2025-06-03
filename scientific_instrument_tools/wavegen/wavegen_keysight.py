# -*- coding: utf-8 -*-

from ..core import ResourceItem
from .wavegen import WaveformGenerator

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
        self.check_errors()

    def set_frequency(self, frequency: float) -> None:
        super().set_frequency(frequency)
        self.visa.write("FREQ {}".format(self._frequency))
        self.check_errors()

    def set_voltage(self, a: float, b: float = 0, mode: str = "AO") -> None:
        super().set_voltage(a, b, mode)
        self.visa.write("VOLT:OFFS {}".format(self._voltage_offset))
        self.visa.write("VOLT {}".format(self._voltage_amplitude))
        self.check_errors()

    def set_duty_cycle(self, duty_cycle: float) -> None:
        super().set_duty_cycle(duty_cycle)
        if self._function == "PULSE":
            self.visa.write("FUNC:PULS:DCYC {}".format(self._duty_cycle))
        elif self._function == "SQUARE":
            self.visa.write("FUNC:SQU:DCYC {}".format(self._duty_cycle))
        else:
            raise NotImplementedError("Duty cycle does not exist for {} function. Please choose 'PULSE' or 'SQUARE'".format(self._function))
        self.check_errors()

    def set_symmetry(self, symmetry: float) -> None:
        super().set_duty_cycle(symmetry)
        self.visa.write("FUNC:RAMP:SYMM {}".format(self._symmetry))
        self.check_errors()

    def set_burst(self, burst: bool, mode: str = "TRIG", inv_polarity: bool = False) -> None:
        super().set_burst(burst, mode, inv_polarity)
        if burst:
            self.visa.write("BURST:STATE ON")
            if self._burst_gated:
                self.visa.write("BURST:MODE GATED")
                if self._burst_inv_polarity:
                    self.visa.write("BURST:GATE:POL INV")
                else:
                    self.visa.write("BURST:GATE:POL NORM")
            else:
                self.visa.write("BURST:MODE TRIG")
        else:
            self.visa.write("BURST:STATE OFF")
        self.check_errors()

    def set_burst_ncycles(self, ncycles: Union[int, str]) -> None:
        super().set_burst_ncycles(ncycles)
        if type(self._burst_ncycles) == str:
            if self._burst_ncycles in ("INF", "MIN", "MAX"):
                self.visa.write("BURST:NCYCLES {}".format(self._burst_ncycles))
            else:
                raise NotImplementedError("Please choose an integer or 'INF' or 'MIN' or 'MAX' for ncycles")
        else:
            self.visa.write("BURST:NCYCLES {}".format(self._burst_ncycles))
        self.check_errors()

    def set_burst_period(self, period: float) -> None:
        super().set_burst_period(period)
        self.visa.write("BURST:INT:PERIOD {}".format(self._burst_period))
        self.check_errors()

    def set_burst_phase(self, phase: float) -> None:
        super().set_burst_phase(phase)
        self.visa.write("BURST:INT:PHASE {}".format(self._burst_phase))
        self.check_errors()

    def set_trig_ext(self, trig_ext: bool, inv_polarity: bool = False) -> None:
        super().set_trig_ext(trig_ext, inv_polarity)
        if trig_ext:
            self.visa.write("TRIG:SOURCE EXTERNAL")
        else:
            self.visa.write("TRIG:SOURCE IMMEDIATE")
        self.check_errors()

    def get_error(self) -> (int, str):
        code, msg = self.visa.query("SYST:ERR?").replace('"', '').replace("\n", '').split(",")
        return int(code), str(msg)

    def check_errors(self) -> None:
        code, msg = self.get_error()
        while code != 0:
            if -code // 100 == 2: # Error code -2XX
                print("[Warning] Waveform Generator Keysight Error : " + msg)
            else:
                raise RuntimeError("Waveform Generator Keysight Error : " + msg)
            code, msg = self.get_error()
