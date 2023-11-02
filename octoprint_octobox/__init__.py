# Import the necessary modules

# coding=utf-8
from __future__ import absolute_import


import octoprint
from octoprint.util import RepeatedTimer
from octoprint.events import Events
import logging
#from LedStripe import LedStripe

plugin_url = "https://github.com/Sna8xs/Octobox/archive/refs/tags/Beta2.zip"

class Octobox(octoprint.plugin.OctoPrintPlugin):
    def __init__(self):
        self._temp_timer = None
        #self.ledstripe = None

    def on_after_startup(self):
        self._logger.info("Octobox started.")
        bed_temp = self._printer.get_current_temperatures()["bed"]["actual"]
        nozzle_temp = self._printer.get_current_temperatures()["tool0"]["actual"]
        self._logger.info(f"Bed Temperature: {bed_temp} °C")
        self._logger.info(f"Nozzle Temperature: {nozzle_temp} °C")
        #self.ledstripe = LedStripe(17, 27, 22)


    def on_shutdown(self):
        if self._timer is not None:
            self._temp_timer.cancel()
            self._logger.info("Octobox stopped.")

    def on_event(self, event, payload):
        if event == Events.PRINT_STARTED:
            self._temp_timer = RepeatedTimer(60, self.get_temperatures)
            self._temp_timer.start()
        if event == Events.PRINT_DONE:
            #self.ledstripe.print_done()
        if event == Events.PRINT_FAILED:
            #self.ledstripe.print_failed()

    def get_temperatures(self):
        bed_temp = self._printer.get_current_temperatures()["bed"]["actual"]
        nozzle_temp = self._printer.get_current_temperatures()["tool0"]["actual"]

        self._logger.info(f"Bed Temperature: {bed_temp} °C")
        self._logger.info(f"Nozzle Temperature: {nozzle_temp} °C")



    def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
		# for details.
		return dict(
			restorelevelingafterg28=dict(
				displayName="OctoBox",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="Sna8xs",
				repo="Octobox",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/Sna8xs/Octobox/archive/refs/tags/Beta2.zip"
			)
		)


__plugin_pythoncompat__ = ">=3.9,<4"

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = Octobox()
    octoprint.plugin.register_plugin(plugin, __plugin_name__)

    global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}


