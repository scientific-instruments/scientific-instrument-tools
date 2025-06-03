# -*- coding: utf-8 -*-

from ..core import ResourceItem
from .scope import Oscilloscope

class OscilloscopeRhodeSchwartz(Oscilloscope):
    """Generic class for Rhode & Schwartz Oscilloscopes."""

    def __init__(self, resource: ResourceItem):
        super().__init__(resource)