import uasyncio
from mipyalpaca.alpacaserver import AlpacaServer
from mipyalpaca.SunFlipFlatCover import SunFlipFlatCover

async def main():
    srv = AlpacaServer("MyPicoServer", "RTJoe", "0.91", "Unknown")

    srv.installDevice("covercalibrator", 0, SunFlipFlatCover(0, "Pico W CoverCalibrator", "a1b2c3d4-e5f6-7890-abcd-ef1234567890", "covercalibrator0.json"))

    # Choose network mode from config:
    #   "station" -> connect to an existing WiFi network (requires wlancred.py)
    #   "ap"      -> create a WiFi Access Point (no external WiFi needed)
    netmode = AlpacaServer.config.get("networkMode", "station")

    if netmode == "ap":
        ap_ssid = AlpacaServer.config.get("apSsid", "MiPyAlpaca")
        ap_pass = AlpacaServer.config.get("apPassword", "alpaca1234")
        AlpacaServer.startAccessPoint(ap_ssid, ap_pass)
    else:
        import wlancred
        AlpacaServer.connectStationMode(wlancred.ssid, wlancred.password)

    await AlpacaServer.startServer()

uasyncio.run(main())
