# -*- coding: utf-8 -*-

import pyvisa

class ResourceManager:
    """Improved version of pyvisa.ResourceManager for SIT usage"""

    resourceManager:pyvisa.ResourceManager = None
    resourceList:list = []

    @classmethod
    def close(cls):
        cls.resourceManager.close()

    @classmethod
    def list_resources(cls) -> list:
        """Check for all available resources and return a list of ResourceItem objects"""
        cls.resourceManager = pyvisa.ResourceManager()
        pyvisa_resource_list = cls.resourceManager.list_resources()
        sit_resource_list = []
        for resource_address in pyvisa_resource_list:
            try:
                resource = cls.resourceManager.open_resource(resource_address)
                resource.read_termination = '\n'
                resource.write_termination = '\n'
                resource_idn = resource.query("*IDN?").split(',')
                resource.close()
                resource_info = ResourceItem(resource_address,
                                             resource_idn[0], resource_idn[1], resource_idn[2], resource_idn[3])
                sit_resource_list.append(resource_info)
            except pyvisa.VisaIOError:
                print("Could not open resource", resource_address)
                continue
        cls.resourceList = sit_resource_list
        return cls.resourceList

    @classmethod
    def resource_tab(cls) -> str:
        """Return string tabular representation of available resources.
        Designed using ChatGPT."""
        if not cls.resourceList:
            return "No resource available"

        # Extract column names from object attributes
        columns = vars(cls.resourceList[0]).keys()
        column_names = {"address": "Address",
                        "manufacturer": "Manufacturer",
                        "model": "Model",
                        "serial": "Serial Number",
                        "firmware": "Firmware Version"}

        # Compute the maximum width for each column
        column_widths = {col: max(len(column_names[col]), *(len(str(vars(row)[col])) for row in cls.resourceList)) for col in columns}

        # Create the table header
        header = " | ".join(f"{column_names[col]:{column_widths[col]}}" for col in columns)
        separator = "+".join(f"-" * (column_widths[col] + 2) for col in columns)

        # Create table rows
        rows = [" | ".join(f"{str(vars(row)[col]):{column_widths[col]}}" for col in columns) for row in cls.resourceList]

        # Combine all parts into the final table with border
        return f"+{separator}+\n| {header} |\n|{separator}|\n" + "\n".join(f"| {row} |" for row in rows) + f"\n+{separator}+"

    @classmethod
    def open_resource(cls, address) -> pyvisa.Resource:
        return cls.resourceManager.open_resource(address)


class ResourceItem:
    """Base class for Resource properties"""
    def __init__(self, address, manufacturer="", model="", serial="", firmware=""):
        self.address = address
        self.manufacturer = manufacturer
        self.model = model
        self.serial = serial
        self.firmware = firmware

    def __str__(self):
        return (f"Address: {self.address}\n"
                f"Manufacturer: {self.manufacturer}\n"
                f"Model: {self.model}\n"
                f"Serial: {self.serial}\n"
                f"Firmware: {self.firmware}")

class ScientificInstrument:
    """Generic class for a Scientific Instrument using pyvisa resources"""

    def __init__(self, resource: ResourceItem):
        self.resource = resource
        self.visa = None
        self.is_connected = False

    def connect(self):
        # Use pyvisa ResourceManager command
        self.visa = ResourceManager.open_resource(self.resource.address)
        # Set is_connected flag
        self.is_connected = True

    def disconnect(self):
        # Use pyvisa ResourceManager command
        if self.visa:
            self.visa.close()
        # Clear is_connected flag
        self.is_connected = False

    def write(self, command: str):
        # Check if connection is made
        if not self.is_connected:
            self.connect()
        # Use pyvisa write command
        self.visa.write(command)

    def read(self) -> str:
        # Check if connection is made
        if not self.is_connected:
            self.connect()
        # Use pyvisa read command
        return self.visa.read()

    def query(self, command: str) -> str:
        # Check if connection is made
        if not self.is_connected:
            self.connect()
        # Use pyvisa query command
        return self.visa.query(command)