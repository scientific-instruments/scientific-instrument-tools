# -*- coding: utf-8 -*-

from .core import ResourceItem
from .scope.factory import OscilloscopeFactory
from .wavegen.factory import WaveformGeneratorFactory


class ScientificInstrumentFactory:
    """Factory for ScientificInstrument and derivatives"""

    @classmethod
    def make_oscilloscope(cls, resource: ResourceItem):
        if resource.manufacturer == "Keysight" or resource.manufacturer == "Agilent Technologies":
            return OscilloscopeFactory.make_keysight(resource)
        elif resource.manufacturer == "Tektronix":
            return OscilloscopeFactory.make_tektronix(resource)
        else:
            cls.__unknown_message__(resource)

    @classmethod
    def make_waveform_generator(cls, resource: ResourceItem):
        if resource.manufacturer == "Keysight" or resource.manufacturer == "Agilent Technologies":
            return WaveformGeneratorFactory.make_keysight(resource)
        elif resource.manufacturer == "Tektronix":
            return WaveformGeneratorFactory.make_tektronix(resource)
        else:
            cls.__unknown_message__(resource)

    @classmethod
    def __unknown_message__(cls, resource: ResourceItem):
        print("Unknown manufacturer", resource.manufacturer)
        print("The requested resource may exist but is not implemented yet. SIT is a collaborative library, feel free to contribute with an implementation for your hardware!")
        raise NotImplementedError

