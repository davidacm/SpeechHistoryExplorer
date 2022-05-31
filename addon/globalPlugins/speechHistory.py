# NVDA Add-on: Speech History
# Copyright (C) 2012 Tyler Spivey
# Copyright (C) 2015-2021 James Scholes
# This add-on is free software, licensed under the terms of the GNU General Public License (version 2).
# See the file LICENSE for more details.

from collections import deque
import weakref
import wx

import addonHandler
import api
import config
from eventHandler import FocusLossCancellableSpeechCommand
from globalCommands import SCRCAT_SPEECH
import globalPluginHandler
import gui
from gui import guiHelper
from gui import nvdaControls
from gui.dpiScalingHelper import DpiScalingHelperMixin, DpiScalingHelperMixinWithoutInit

from queueHandler import eventQueue, queueFunction
import speech
import speechViewer
import tones
import versionInfo


addonHandler.initTranslation()

BUILD_YEAR = getattr(versionInfo, 'version_year', 2021)


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		confspec = {
			'maxHistoryLength': 'integer(default=500)',
			'trimWhitespaceFromStart': 'boolean(default=false)',
			'trimWhitespaceFromEnd': 'boolean(default=false)',
		}
		config.conf.spec['speechHistory'] = confspec
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(SpeechHistorySettingsPanel)

		self._history = deque(maxlen=config.conf['speechHistory']['maxHistoryLength'])
		self._patch()

	def _patch(self):
		if BUILD_YEAR >= 2021:
			self.oldSpeak = speech.speech.speak
			speech.speech.speak = self.mySpeak
		else:
			self.oldSpeak = speech.speak
			speech.speak = self.mySpeak

	def script_copyLast(self, gesture):
		text = self.getSequenceText(self._history[self.history_pos])
		if config.conf['speechHistory']['trimWhitespaceFromStart']:
			text = text.lstrip()
		if config.conf['speechHistory']['trimWhitespaceFromEnd']:
			text = text.rstrip()
		if api.copyToClip(text):
			tones.beep(1500, 120)

	# Translators: Documentation string for copy currently selected speech history item script
	script_copyLast.__doc__ = _('Copy the currently selected speech history item to the clipboard, which by default will be the most recently spoken text by NVDA.')
	script_copyLast.category = SCRCAT_SPEECH

	def script_prevString(self, gesture):
		self.history_pos += 1
		if self.history_pos > len(self._history) - 1:
			tones.beep(220, 100, 100, 0)
			self.history_pos -= 1
		self.oldSpeak(self._history[self.history_pos])
	# Translators: Documentation string for previous speech history item script
	script_prevString.__doc__ = _('Review the previous item in NVDA\'s speech history.')
	script_prevString.category = SCRCAT_SPEECH

	def script_nextString(self, gesture):
		self.history_pos -= 1
		if self.history_pos < 0:
			tones.beep(220, 100, 0, 100)
			self.history_pos += 1

		self.oldSpeak(self._history[self.history_pos])
	# Translators: Documentation string for next speech history item script
	script_nextString.__doc__ = _('Review the next item in NVDA\'s speech history.')
	script_nextString.category = SCRCAT_SPEECH

	def script_showHistorial(self, gesture):
		gui.mainFrame.prePopup()
		HistoryDialog(gui.mainFrame, self).Show()
		gui.mainFrame.postPopup()

	# Translators: Documentation string for show in a dialog all recent items spoken by NVDA.
	script_showHistorial.__doc__ = _('Opens a dialog showing all most recent items spoken by NVDA')
	script_showHistorial.category = SCRCAT_SPEECH

	def terminate(self, *args, **kwargs):
		super().terminate(*args, **kwargs)
		if BUILD_YEAR >= 2021:
			speech.speech.speak = self.oldSpeak
		else:
			speech.speak = self.oldSpeak
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(SpeechHistorySettingsPanel)

	def append_to_history(self, seq):
		seq = [command for command in seq if not isinstance(command, FocusLossCancellableSpeechCommand)]
		self._history.appendleft(seq)
		self.history_pos = 0

	def mySpeak(self, sequence, *args, **kwargs):
		self.oldSpeak(sequence, *args, **kwargs)
		text = self.getSequenceText(sequence)
		if text.strip():
			queueFunction(eventQueue, self.append_to_history, sequence)

	def getSequenceText(self, sequence):
		return speechViewer.SPEECH_ITEM_SEPARATOR.join([x for x in sequence if isinstance(x, str)])

	def clearHistory(self):
		self._history.clear()
		self.history_pos = 0


	__gestures = {
		"kb:nvda+control+f12":"copyLast",
		"kb:nvda+shift+f11":"prevString",
		"kb:nvda+shift+f12":"nextString",
		"kb:nvda+alt+f12":"showHistorial",
	}


class SpeechHistorySettingsPanel(gui.SettingsPanel):
	# Translators: the label/title for the Speech History settings panel.
	title = _('Speech History')

	def makeSettings(self, settingsSizer):
		helper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		# Translators: the label for the preference to choose the maximum number of stored history entries
		maxHistoryLengthLabelText = _('&Maximum number of history entries (requires NVDA restart to take effect)')
		self.maxHistoryLengthEdit = helper.addLabeledControl(maxHistoryLengthLabelText, nvdaControls.SelectOnFocusSpinCtrl, min=1, max=5000, initial=config.conf['speechHistory']['maxHistoryLength'])
		# Translators: the label for the preference to trim whitespace from the start of text
		self.trimWhitespaceFromStartCB = helper.addItem(wx.CheckBox(self, label=_('Trim whitespace from &start when copying text')))
		self.trimWhitespaceFromStartCB.SetValue(config.conf['speechHistory']['trimWhitespaceFromStart'])
		# Translators: the label for the preference to trim whitespace from the end of text
		self.trimWhitespaceFromEndCB = helper.addItem(wx.CheckBox(self, label=_('Trim whitespace from &end when copying text')))
		self.trimWhitespaceFromEndCB.SetValue(config.conf['speechHistory']['trimWhitespaceFromEnd'])

	def onSave(self):
		config.conf['speechHistory']['maxHistoryLength'] = self.maxHistoryLengthEdit.GetValue()
		config.conf['speechHistory']['trimWhitespaceFromStart'] = self.trimWhitespaceFromStartCB.GetValue()
		config.conf['speechHistory']['trimWhitespaceFromEnd'] = self.trimWhitespaceFromEndCB.GetValue()



class HistoryDialog(
		DpiScalingHelperMixinWithoutInit,
		gui.contextHelp.ContextHelpMixin,
		wx.Dialog  # wxPython does not seem to call base class initializer, put last in MRO
):
	@classmethod
	def _instance(cls):
		""" type: () -> HistoryDialog
		return None until this is replaced with a weakref.ref object. Then the instance is retrieved
		with by treating that object as a callable.
		"""
		return None

	helpId = "SpeechHistoryElementsList"

	def __new__(cls, *args, **kwargs):
		instance = HistoryDialog._instance()
		if instance is None:
			return super(HistoryDialog, cls).__new__(cls, *args, **kwargs)
		return instance

	def __init__(self, parent, addon):
		if HistoryDialog._instance() is not None:
			return
		HistoryDialog._instance = weakref.ref(self)
		# Translators: The title of the history elements Dialog
		title = _("Speech history items")
		super().__init__(
			parent,
			title=title,
			style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.MAXIMIZE_BOX,
		)
		# hte add-on instance
		self.addon = addon
		# the original speech history messages list.
		self.history = None
		# the results of a search, initially equals to history
		self.searchHistory = None
		# indexes of search, to save the selected item in a specific search.
		self.searches = {"": 0}
		# the current search, initially "".
		self.curSearch = ""
		# the indexes of items selected.
		self.selection = set()

		szMain = guiHelper.BoxSizerHelper(self, sizer=wx.BoxSizer(wx.VERTICAL))
		szCurrent = guiHelper.BoxSizerHelper(self, sizer=wx.BoxSizer(wx.HORIZONTAL))
		szBottom = guiHelper.BoxSizerHelper(self, sizer=wx.BoxSizer(wx.HORIZONTAL))

		# Translators: the label for the search text field in the speech history add-on.
		self.searchTextFiel = szMain.addLabeledControl(_("&Search"),
			wx.TextCtrl,
			style =wx.TE_PROCESS_ENTER
		)
		self.searchTextFiel.Bind(wx.EVT_TEXT_ENTER, self.onSearch)
		self.searchTextFiel.Bind(wx.EVT_KILL_FOCUS, self.onSearch)

		# Translators: the label for the history elements list in the speech history add-on.
		entriesLabel = _("History list")
		self.historyList = nvdaControls.AutoWidthColumnListCtrl(
			parent=self,
			autoSizeColumn=1,
			style=wx.LC_REPORT|wx.LC_NO_HEADER
			)
		
		szMain.addItem(
			self.historyList,
			flag=wx.EXPAND,
			proportion=4
		)
		# This list consists of only one column.
		# The provided column header is just a placeholder, as it is hidden due to the wx.LC_NO_HEADER style flag.
		self.historyList.InsertColumn(0, entriesLabel)
		self.historyList.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onSelect)
		self.historyList.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.onDeselect)

		# a multiline text field containing the text from the current selected element.
		self.currentTextElement = szCurrent.addItem(
			wx.TextCtrl(self, style =wx.TE_MULTILINE|wx.TE_READONLY),
			flag=wx.EXPAND,
			proportion=1
		)

		# Translators: the label for the copy button in the speech history add-on.
		self.copyButton = szCurrent.addItem(wx.Button(self, label=_("&Copy item")), proportion=0)
		self.copyButton.Bind(wx.EVT_BUTTON, self.onCopy)
		szMain.addItem(
			szCurrent.sizer,
			border=guiHelper.BORDER_FOR_DIALOGS,
			flag = wx.EXPAND,
			proportion=1,
		)

		szMain.addItem(
			wx.StaticLine(self),
			border=guiHelper.BORDER_FOR_DIALOGS,
			flag=wx.ALL | wx.EXPAND
		)

		# Translators: the label for the copy all button in the speech history add-on. This is based on the current search.
		self.copyAllButton = szBottom.addItem(wx.Button(self, label=_("Copy &all")))
		self.copyAllButton.Bind(wx.EVT_BUTTON, self.onCopyAll)

		# Translators: the label for the clear history button in the speech history add-on. This button clean all items in the historial, both in the dialog and in the add-on.
		self.clearHistoryButton = szBottom.addItem(wx.Button(self, label=_("C&lean history")))
		self.clearHistoryButton.Bind(wx.EVT_BUTTON, self.onClear)

		# Translators: the label for the refresh history button in the speech history add-on. This button updates the list item with the new history elements.
		self.refreshButton = szBottom.addItem(wx.Button(self, label=_("&Refresh history")))
		self.refreshButton.Bind(wx.EVT_BUTTON, self.onRefresh)

		# Translators: The label of a button to close the speech history dialog.
		closeButton = wx.Button(self, label=_("C&lose"), id=wx.ID_CLOSE)
		closeButton.Bind(wx.EVT_BUTTON, lambda evt: self.Close())
		szBottom.addItem(closeButton)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.EscapeId = wx.ID_CLOSE

		szMain.addItem(
			szBottom.sizer,
			border=guiHelper.BORDER_FOR_DIALOGS,
			flag=wx.ALL | wx.EXPAND,
			proportion=1,
		)
		szMain = szMain.sizer
		szMain.Fit(self)
		self.SetSizer(szMain)
		self.updateHistory()

		self.SetMinSize(szMain.GetMinSize())
		# Historical initial size, result of L{self.historyList} being (550, 350)
		# Setting an initial size on L{self.historyList} by passing a L{size} argument when
		# creating the control would also set its minimum size and thus block the dialog from being shrunk.
		self.SetSize(self.scaleSize((763, 509)))
		self.CentreOnScreen()
		self.historyList.SetFocus()

	def updateHistory(self):
		self.selection = set()
		self.history = [self.addon.getSequenceText(k) for k in self.addon._history]
		self.doSearch(self.curSearch)

	def doSearch(self, text=""):
		self.selection = set()
		if not text:
			self.searchHistory = self.history
		else:
			self.searchHistory = [k for k in self.searchHistory if text in k.lower()]
		self.historyList.DeleteAllItems()
		self.currentTextElement.SetValue("")
		for k in self.searchHistory: self.historyList.Append((k[0:100],))
		if len(self.searchHistory) >0:
			index = self.searches.get(text, 0)
			self.historyList.Select(index, on=1)
			self.historyList.SetItemState(index,wx.LIST_STATE_FOCUSED,wx.LIST_STATE_FOCUSED)

	def updateSelection(self):
		self.currentTextElement.SetValue(self.itemsToString(sorted(self.selection)))

	def itemsToString(self, items):
		s = ""
		for k in items:
			s += self.searchHistory[k] +"\n"
		if s: s= s[0:-1]
		return s

	def onSearch(self, evt):
		t = self.searchTextFiel.GetValue().lower()
		if t == self.curSearch: return
		index = self.historyList.GetFocusedItem()
		if index < 0: index = 0
		self.searches[self.curSearch] = index
		self.curSearch = t
		self.doSearch(t)

	def onClose(self,evt):
		self.DestroyChildren()
		self.Destroy()

	def onCopy(self,evt):
		t = self.currentTextElement.GetValue()
		if t:
			if api.copyToClip(t):
				tones.beep(1500, 120)

	def onCopyAll(self, evt):
		t = self.itemsToString(range(0, len(self.searchHistory)))
		if t and api.copyToClip(t):
			tones.beep(1500, 120)

	def onClear(self, evt):
		self.addon.clearHistory()
		self.searches = {"":0}
		self.updateHistory()

	def onRefresh(self, evt):
		self.updateHistory()

	def onSelect(self, evt):
		index=evt.GetIndex()
		self.selection.add(index)
		self.updateSelection()

	def onDeselect(self, evt):
		index=evt.GetIndex()
		self.selection.remove(index)
		self.updateSelection()
