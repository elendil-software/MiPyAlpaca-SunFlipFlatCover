from mipyalpaca.alpacaserver import *
from mipyalpaca.alpacadevice import AlpacaDevice


class CalibratorStatus:
    """CalibratorStatus enum values (ASCOM Alpaca specification)."""
    NOT_PRESENT = 0   # This device does not have a calibrator
    OFF         = 1   # The calibrator is off
    NOT_READY   = 2   # The calibrator is stabilising or is not yet in the commanded state
    READY       = 3   # The calibrator is ready for use
    UNKNOWN     = 4   # The calibrator state is unknown
    ERROR       = 5   # The calibrator encountered an error


class CoverStatus:
    """CoverStatus enum values (ASCOM Alpaca specification)."""
    NOT_PRESENT = 0   # This device does not have a cover
    CLOSED      = 1   # The cover is closed
    MOVING      = 2   # The cover is moving
    OPEN        = 3   # The cover is open
    UNKNOWN     = 4   # The cover state is unknown
    ERROR       = 5   # The cover encountered an error


# ASCOM Alpaca CoverCalibrator device
class CoverCalibratorDevice(AlpacaDevice):

    def __init__(self, devnr, devname, uniqueid):
        super().__init__(devnr, devname, uniqueid)
        self.interfaceVersion = 2       # ICoverCalibratorV2

        # CoverCalibrator state
        self._brightness = 0                          # current calibrator brightness (0..MaxBrightness)
        self._maxbrightness = 0                       # max brightness (0 = no calibrator)
        self._calibratorstate = CalibratorStatus.NOT_PRESENT
        self._coverstate = CoverStatus.NOT_PRESENT
        self._calibratorchanging = False              # True while calibrator is changing state
        self._covermoving = False                     # True while cover is moving

    # ------------------------------------------------------------------ #
    # GET properties                                                       #
    # ------------------------------------------------------------------ #

    # Returns the current calibrator brightness (0 to MaxBrightness)
    def GET_brightness(self, request):
        if self._calibratorstate == CalibratorStatus.NOT_PRESENT:
            raise NotImplementedError("Calibrator not present")
        return self.reply(request, self._brightness)

    # Returns True if the calibrator is in the process of changing state
    def GET_calibratorchanging(self, request):
        return self.reply(request, self._calibratorchanging)

    # Returns the state of the calibration device (CalibratorStatus enum)
    def GET_calibratorstate(self, request):
        return self.reply(request, self._calibratorstate)

    # Returns True if the cover is in the process of moving
    def GET_covermoving(self, request):
        return self.reply(request, self._covermoving)

    # Returns the state of the cover device (CoverStatus enum)
    def GET_coverstate(self, request):
        return self.reply(request, self._coverstate)

    # Returns the maximum brightness value for the calibrator
    def GET_maxbrightness(self, request):
        if self._calibratorstate == CalibratorStatus.NOT_PRESENT:
            raise NotImplementedError("Calibrator not present")
        return self.reply(request, self._maxbrightness)

    # ------------------------------------------------------------------ #
    # PUT actions                                                          #
    # ------------------------------------------------------------------ #

    # Turns the calibrator off (asynchronous – overridable)
    def calibratoroff(self):
        """Override this method to implement hardware calibrator off."""
        self._brightness = 0
        self._calibratorstate = CalibratorStatus.OFF

    def PUT_calibratoroff(self, request):
        if self._calibratorstate == CalibratorStatus.NOT_PRESENT:
            raise NotImplementedError("Calibrator not present")
        self.calibratoroff()
        return self.reply(request)

    # Turns the calibrator on with the specified brightness
    def calibratoron(self, brightness):
        """Override this method to implement hardware calibrator on."""
        self._brightness = brightness
        self._calibratorstate = CalibratorStatus.READY

    def PUT_calibratoron(self, request):
        if self._calibratorstate == CalibratorStatus.NOT_PRESENT:
            raise NotImplementedError("Calibrator not present")
        bval = request.form.get('Brightness')
        if bval is None:
            raise CallArgError("Missing Brightness parameter")
        try:
            brightness = int(bval)
        except (ValueError, TypeError):
            raise CallArgError("Invalid Brightness value")
        if (brightness < 0) or (brightness > self._maxbrightness):
            raise RangeError("Brightness value out of range (0.." + str(self._maxbrightness) + ")")
        self.calibratoron(brightness)
        return self.reply(request)

    # Initiates cover closing (asynchronous – overridable)
    def closecover(self):
        """Override this method to implement hardware cover close."""
        self._coverstate = CoverStatus.CLOSED

    def PUT_closecover(self, request):
        if self._coverstate == CoverStatus.NOT_PRESENT:
            raise NotImplementedError("Cover not present")
        self.closecover()
        return self.reply(request)

    # Stops any cover movement immediately (asynchronous – overridable)
    def haltcover(self):
        """Override this method to implement hardware cover halt."""
        self._covermoving = False

    def PUT_haltcover(self, request):
        if self._coverstate == CoverStatus.NOT_PRESENT:
            raise NotImplementedError("Cover not present")
        self.haltcover()
        return self.reply(request)

    # Initiates cover opening (asynchronous – overridable)
    def opencover(self):
        """Override this method to implement hardware cover open."""
        self._coverstate = CoverStatus.OPEN

    def PUT_opencover(self, request):
        if self._coverstate == CoverStatus.NOT_PRESENT:
            raise NotImplementedError("Cover not present")
        self.opencover()
        return self.reply(request)

