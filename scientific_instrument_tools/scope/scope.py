# -*- coding: utf-8 -*-

from ..core import ScientificInstrument, ResourceItem

class Oscilloscope(ScientificInstrument):
    """Generic class for Oscilloscopes"""

    def __init__(self, resource: ResourceItem):
        super().__init__(resource)