# -*- coding: utf-8 -*-

from ..core import ResourceItem
from .scope import Oscilloscope

class OscilloscopeTektronix(Oscilloscope):
    """Generic class for Tektronix Oscilloscopes."""

    def __init__(self, resource: ResourceItem):
        super().__init__(resource)