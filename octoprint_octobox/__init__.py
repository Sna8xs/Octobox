# Import the necessary modules
from __future__ import absolute_import
from octoprint.plugin import OctoPrintPlugin
from octoprint.util import RepeatedTimer
from octoprint.events import Events
import logging
import octoprint

# Define the plugin version
plugin_version = "0.1.0"

class Octobox(octoprint.plugin.StartupPlugin):
    def __init__(self):
        self._temp_timer = None

    def on_after_startup(self):
        self._logger.info("Octobox started.")
        bed_temp = self._printer.get_current_temperatures()["bed"]["actual"]
        nozzle_temp = self._printer.get_current_temperatures()["tool0"]["actual"]
        self._logger.info(f"Bed Temperature: {bed_temp} °C")
        self._logger.info(f"Nozzle Temperature: {nozzle_temp} °C")

    def on_shutdown(self):
        if self._temp_timer is not None:
            self._temp_timer.cancel()
            self._logger.info("Octobox stopped.")

    def on_event(self, event, payload):
        if event == Events.PRINT_STARTED:
            self._temp_timer = RepeatedTimer(60, self.get_temperatures)
            self._temp_timer.start()
        if event == Events.PRINT_DONE:
            pass
        if event == Events.PRINT_FAILED:
            pass

    def get_temperatures(self):
        bed_temp = self._printer.get_current_temperatures()["bed"]["actual"]
        nozzle_temp = self._printer.get_current_temperatures()["tool0"]["actual"]

        self._logger.info(f"Bed Temperature: {bed_temp} °C")
        self._logger.info(f"Nozzle Temperature: {nozzle_temp} °C")

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        return dict(
            octobox=dict(
                displayName="OctoBox",
                displayVersion=plugin_version,
                type="github_release",
                user="Sna8xs",
                repo="Octobox",
                current=plugin_version,
                pip="https://github.com/Sna8xs/Octobox/archive/refs/tags/Beta2.zip"
            )
        )

__plugin_pythoncompat__ = ">=3.0.2,<4"

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = Octobox()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
