# -*- coding: utf-8 -*-

from ..core import ScientificInstrument, ResourceItem

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
        self._burst = None
        self._burst_gated = None
        self._burst_ncycles = None
        self._burst_period = None
        self._burst_phase = None
        self._burst_inv_polarity = None
        self._trig_ext = None
        self._trig_ext_inv_polarity = None
        
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

    def set_burst(self, burst: bool, mode: str = "TRIG", inv_polarity: bool = False) -> None:
        self._burst = burst
        if mode == "TRIG":
            self._burst_gated = False
        elif mode == "GATE":
            self._burst_gated = True
        else:
            raise NotImplementedError("Mode {} is not implemented. Please choose 'TRIG' or 'GATE'".format(mode))

    def set_burst_ncycles(self, ncycles: Union[int, str]) -> None:
        self._burst_ncycles = ncycles
        
    def set_burst_period(self, period: float) -> None:
        self._burst_period = period
        
    def set_burst_phase(self, phase: float) -> None:
        self._burst_phase = phase
    
    def set_trig_ext(self, trig_ext: bool, inv_polarity: bool = False) -> None:
        self._trig_ext = trig_ext
        self._trig_ext_inv_polarity = inv_polarity

    def get_error(self) -> (int, str):
        raise NotImplementedError()

    def check_errors(self) -> None:
        raise NotImplementedError()

