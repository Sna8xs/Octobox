# Import the necessary modules
import octoprint
from octoprint.util import RepeatedTimer
from octoprint.events import Events
import octoprint.plugin
import logging
#from LedStripe import LedStripe

class Octobox(octoprint.plugin.StartupPlugin):
    def __init__(self):
        self._temp_timer = None
        #self.ledstripe = None

    def on_after_startup(self):
        self._logger.info("Octobox started.")
        self._logger.info(f"Bed Temperature: {self._printer.get_current_temperatures()["bed"]["actual"]} °C")
        self._logger.info(f"Nozzle Temperature: {self._printer.get_current_temperatures()["tool0"]["actual"]} °C")
        #self.ledstripe = LedStripe(17, 27, 22)


    def on_shutdown(self):
        if self._timer is not None:
            self._temp_timer.cancel()
            self._logger.info("Octobox stopped.")

    def on_event(self, event, payload):
        if event == Events.PRINT_STARTED:
            self._temp_timer = RepeatedTimer(60, self.get_temperatures)
            self._temp_timer.start()
        elif event == Events.PRINT_DONE:
            #self.ledstripe.print_done()
        elif event == Events.PRINT_FAILED:
            #self.ledstripe.print_failed()

    def get_temperatures(self):
        bed_temp = self._printer.get_current_temperatures()["bed"]["actual"]
        nozzle_temp = self._printer.get_current_temperatures()["tool0"]["actual"]

        self._logger.info(f"Bed Temperature: {bed_temp} °C")
        self._logger.info(f"Nozzle Temperature: {nozzle_temp} °C")

def __plugin_load__():
    plugin = Octobox()
    octoprint.plugin.register_plugin(plugin, __plugin_name__)

__plugin_pythoncompat__ = ">=3.11.3,<4"
__plugin_implementation__ = Octobox()
