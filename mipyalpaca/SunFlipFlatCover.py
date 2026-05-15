from mipyalpaca.alpacacover import CoverCalibratorDevice, CoverStatus
from mipyalpaca.alpacaserver import readJson
from mipyalpaca.SimplyServos import KitronikSimplyServos
from microdot_utemplate import render_template
import uasyncio

class SunFlipFlatCover(CoverCalibratorDevice):

    def __init__(self, devnr, devname, uniqueid, config_file):
        super().__init__(devnr, devname, uniqueid)
        self.description = "Sun Flip Flat Cover"
        self.name = "Sun Flip Flat Cover"
        self.driverinfo = "Sun Flip Flat Cover v0.1.0"
        self.driverVersion = "0.1.0"
        self.configfile = config_file
        self._cfg = readJson(config_file)

        # ---- Cover hardware setup ----------------------------------------
        cover_cfg = self._cfg.get("cover", {})
        # self._cover_enabled = cover_cfg.get("enabled", False)
        self._move_time_ms   = int(cover_cfg.get("move_time_ms", 1000))
        self._servo_number   = int(cover_cfg.get("servo_number", 1))
        self._servo_open_angle  = int(cover_cfg.get("servo_open_angle", 250))
        self._servo_close_angle = int(cover_cfg.get("servo_close_angle", 0))
        self._max_degrees    = int(cover_cfg.get("max_degrees", 270))
        self._servos = KitronikSimplyServos(numberOfServos=self._servo_number, maxDegrees=self._max_degrees)
        self._coverstate = CoverStatus.UNKNOWN
        # Set servo immediately to open position to avoid intermediate movement at startup
        self._servos.goToPosition(self._servo_number, self._servo_open_angle)
        self._coverstate = CoverStatus.OPEN
        self._covermoving = False

    # ------------------------------------------------------------------ #
    # Cover hardware actions                                               #
    # ------------------------------------------------------------------ #

    async def _move_cover(self, target_state):
        """Async task: move servo to target angle then update state."""
        self._covermoving = True
        self._coverstate  = CoverStatus.MOVING
        if target_state == CoverStatus.OPEN:
            self._servos.goToPosition(self._servo_number, self._servo_open_angle)
        else:
            self._servos.goToPosition(self._servo_number, self._servo_close_angle)
        await uasyncio.sleep_ms(self._move_time_ms)
        self._coverstate  = target_state
        self._covermoving = False

    def opencover(self):
        uasyncio.create_task(self._move_cover(CoverStatus.OPEN))

    def closecover(self):
        uasyncio.create_task(self._move_cover(CoverStatus.CLOSED))

    def haltcover(self):
        raise NotImplementedError("HaltCover is not supported by this device")

    # ------------------------------------------------------------------ #
    # Setup page                                                           #
    # ------------------------------------------------------------------ #

    def setupRequest(self, request):
        return render_template('covercalibrator0.html', devname=self.name, cfgfile=self.configfile)
