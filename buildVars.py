# -*- coding: UTF-8 -*-

# Build customizations
# Change this file instead of sconstruct or manifest files, whenever possible.

# Full getext (please don't change)
_ = lambda x : x

# Add-on information variables
addon_info = {
	# for previously unpublished addons, please follow the community guidelines at:
	# https://bitbucket.org/nvdaaddonteam/todo/raw/master/guideLines.txt
	# add-on Name, internal for nvda
	"addon_name" : "speechHistoryExplorer",
	# Add-on summary, usually the user visible name of the addon.
	# Translators: Summary for this add-on to be shown on installation and add-on information.
	"addon_summary" : _("Speech history Explorer"),
	# Add-on description
	# Translators: Long description to be shown for this add-on on add-on information from add-ons manager
	"addon_description" : _("""This add-on allows you to review the most recent strings spoken by NVDA, by default using NVDA+Shift+F11 and NVDA+Shift+F12. 
	Additionally, you can copy any spoken item to the clipboard by pressing NVDA+Control+F12 and shows a dialog of all stored spoken elements with NVDA+Alt+f12.
	Use the settings panel for the add-on to increase or decrease the maximum number of stored history entries, and decide whether whitespace should be trimmed from the start or end of text.
	Use NVDA's Input Gestures dialog to change the supplied keystrokes."""),
	# version
	"addon_version" : "2022.2-dev",
	# Author(s)
	"addon_author" : u"Tyler Spivey, James Scholes, David CM <dhf360@gmail.com>",
	# URL for the add-on documentation support
	"addon_url" : "https://github.com/davidacm/SpeechHistoryExplorer",
	# Documentation file name
	"addon_docFileName" : "readme.html",
	# Minimum NVDA version supported (e.g. "2018.3.0")
	"addon_minimumNVDAVersion" : "2019.3.0",
	# Last NVDA version supported/tested (e.g. "2018.4.0", ideally more recent than minimum version)
	"addon_lastTestedNVDAVersion" : "2022.2",
	# Add-on update channel (default is stable or None)
	"addon_updateChannel" : None,
}

from os import path

# Define the python files that are the sources of your add-on.
# You can use glob expressions here, they will be expanded.
pythonSources = [path.join("addon", "globalPlugins", "beepKeyboard.py")]

# Files that contain strings for translation. Usually your python sources
i18nSources = pythonSources + ["buildVars.py"]

# Files that will be ignored when building the nvda-addon file
# Paths are relative to the addon directory, not to the root directory of your addon sources.
excludedFiles = []
