class SeedBaseException(Exception):
    """All exception should derive from this."""

class IrradianceDataException(SeedBaseException):
    def __init__(self, validation_error) -> None:
        self.message=(f"Irradiance data invalid --> {validation_error}")
        super().__init__(self.message)

class SolarParametersException(SeedBaseException):
    def __init__(self, validation_error) -> None:
        self.message=(f"Solar parameter invalid --> {validation_error}")
        super().__init__(self.message)

class InverterParametersException(SeedBaseException):
    def __init__(self, validation_error) -> None:
        self.message=(f"Inverter parameter invalid --> {validation_error}")
        super().__init__(self.message)
    

