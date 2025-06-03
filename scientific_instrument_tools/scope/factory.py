# -*- coding: utf-8 -*-

from ..core import ResourceItem

class OscilloscopeFactory:
    """Factory for ScientificInstrument and derivatives"""

    @classmethod
    def make_keysight(cls, resource: ResourceItem):
        cls.__unknown_message__(resource)

    @classmethod
    def make_tektronix(cls, resource: ResourceItem):
        cls.__unknown_message__(resource)

    @classmethod
    def __unknown_message__(cls, resource: ResourceItem):
        raise NotImplementedError(f"Unknown model {resource.model} for {resource.manufacturer}\n"
         f"The requested resource may exist but is not implemented yet. SIT is a collaborative library, feel free to contribute with an implementation for your hardware!\n")

