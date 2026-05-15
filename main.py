import uasyncio
import wlancred
from mipyalpaca.alpacaserver import AlpacaServer
from mipyalpaca.SunFlipFlatCover import SunFlipFlatCover

async def main():
    srv = AlpacaServer("MyPicoServer", "RTJoe", "0.91", "Unknown")

    srv.installDevice("covercalibrator", 0, SunFlipFlatCover(0, "Pico W CoverCalibrator", "a1b2c3d4-e5f6-7890-abcd-ef1234567890", "covercalibrator0.json"))

    AlpacaServer.connectStationMode(wlancred.ssid, wlancred.password)

    await AlpacaServer.startServer()

uasyncio.run(main())

