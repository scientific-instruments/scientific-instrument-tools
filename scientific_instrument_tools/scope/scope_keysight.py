# -*- coding: utf-8 -*-

from ..core import ResourceItem
from .scope import Oscilloscope

class OscilloscopeKeysight(Oscilloscope):
    """Generic class for Keysight Oscilloscopes."""

    def __init__(self, resource: ResourceItem):
        super().__init__(resource)