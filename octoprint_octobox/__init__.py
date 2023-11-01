# Import the necessary modules
import octoprint
from octoprint.util import RepeatedTimer
from octoprint.events import Events
import logging
from LedStripe import LedStripe

class Octobox:
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._temp_timer = None

    def on_after_startup(self):
        self._logger.info("Octobox started.")
        self.ledstripe = LedStripe(17, 27, 22)


    def on_shutdown(self):
        if self._timer is not None:
            self._timer.cancel()
            self._logger.info("Octobox stopped.")

    def on_event(self, event, payload):
        if event == Events.PRINT_STARTED:
            self._temp_timer = RepeatedTimer(60, self.get_temperatures)
            self._temp_timer.start()
        elif event == Events.PRINT_DONE:
            self.ledstripe.print_done()
        elif event == Events.PRINT_FAILED:
            self.ledstripe.print_failed()

    def get_temperatures(self):
        bed_temp = self._printer.get_current_temperatures()["bed"]["actual"]
        nozzle_temp = self._printer.get_current_temperatures()["tool0"]["actual"]

        self._logger.info(f"Bed Temperature: {bed_temp} °C")
        self._logger.info(f"Nozzle Temperature: {nozzle_temp} °C")

    def print_failed():
        pass

def __plugin_load__():
    plugin = Octobox()
    octoprint.plugin.register_plugin(plugin, __plugin_name__)

__plugin_name__ = "Octobox"
__plugin_implementation__ = Octobox()
