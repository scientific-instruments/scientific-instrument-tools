# -*- coding: utf-8 -*-

from .wavegen import WaveformGeneratorKeysight

class WaveformGeneratorKeysight(ScientificInstrument):
    """Generic class for Waveform Generators."""

    def __init__(self, resource: ResourceItem):
        super().__init__(resource)