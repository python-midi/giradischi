#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
"""giradischi GUI."""

from PySide6.QtCore import QFile, Signal
from PySide6.QtGui import QAction
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (
	QApplication,
	QFileDialog,
	QLabel,
	QListWidget,
	QListWidgetItem,
	QProgressBar,
	QPushButton,
	QStatusBar,
	QStyle,
)
from pathlib import Path
from threading import Thread
from time import sleep

from giradischi.backends import get_backend_by_name, get_available_backends
from giradischi.utils.midi_player import MidiPlayer

ui_path = Path(__file__).parent

class GiradischiUI(QApplication):
	update_time = Signal(float)

	def __init__(self, file: Path = None) -> None:
		super().__init__()
		self.setApplicationName("giradischi")
		self.setApplicationDisplayName("Giradischi")

		mainwindow_ui_file = QFile(ui_path / "mainwindow.ui")
		mainwindow_ui_file.open(QFile.ReadOnly)

		backend_selector_dialog_ui_file = QFile(ui_path / "backend_selector_dialog.ui")
		backend_selector_dialog_ui_file.open(QFile.ReadOnly)

		backend_settings_dialog_ui_file = QFile(ui_path / "backend_settings_dialog.ui")
		backend_settings_dialog_ui_file.open(QFile.ReadOnly)

		loader = QUiLoader()
		self.mainwindow = loader.load(mainwindow_ui_file)
		self.backend_selector_dialog = loader.load(backend_selector_dialog_ui_file)
		self.backend_settings_dialog = loader.load(backend_settings_dialog_ui_file)

		# mainwindow
		self.status_bar: QStatusBar = self.mainwindow.findChild(QStatusBar, "statusBar")

		self.open_file_action: QAction = self.mainwindow.findChild(QAction, "openFileAction")
		self.open_file_action.triggered.connect(self._select_file)

		self.open_file_button: QPushButton = self.mainwindow.findChild(QPushButton, "openFileButton")
		self.open_file_button.setIcon(self.style().standardIcon(QStyle.SP_DirIcon))
		self.open_file_button.clicked.connect(self._select_file)

		self.play_button: QPushButton = self.mainwindow.findChild(QPushButton, "playPauseButton")
		self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
		self.play_button.clicked.connect(self._play_pause)

		self.stop_button: QPushButton = self.mainwindow.findChild(QPushButton, "stopButton")
		self.stop_button.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
		self.stop_button.clicked.connect(self._stop)

		self.settings_button: QPushButton = self.mainwindow.findChild(QPushButton, "settingsButton")
		self.settings_button.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
		self.settings_button.clicked.connect(self._open_backend_selector_dialog)

		self.title_label: QLabel = self.mainwindow.findChild(QLabel, "titleLabel")
		self.current_time_label: QLabel = self.mainwindow.findChild(QLabel, "currentTimeLabel")
		self.duration_time_label: QLabel = self.mainwindow.findChild(QLabel, "durationTimeLabel")
		self.progress_bar: QProgressBar = self.mainwindow.findChild(QProgressBar, "progressBar")

		# backend_selector_dialog
		self.backend_selector_list_widget: QListWidget = self.backend_selector_dialog.findChild(QListWidget, "backendSelectorListWidget")
		self.backend_selector_list_widget.itemClicked.connect(self._change_backend)

		self.backend_settings_button: QPushButton = self.backend_selector_dialog.findChild(QPushButton, "backendSettingsButton")
		self.backend_settings_button.clicked.connect(self._open_backend_settings_dialog)

		# backend_settings_dialog
		self.backend_settings_list_widget: QListWidget = self.backend_settings_dialog.findChild(QListWidget, "devicesListWidget")
		self.backend_settings_list_widget.itemClicked.connect(self._change_device)

		self.midi_player = MidiPlayer()
		self.opened_file: Path = None

		self.update_time.connect(self._update_time_label)

		self.thread = Thread(target=self._daemon, daemon=True)
		self.thread.start()

		if file and file.suffix == ".mid":
			self._open_file(file)

	def start_ui(self):
		self.mainwindow.show()

		self.exec()

	def _update_time_label(self, time: float):
		if self.midi_player.is_playing():
			self.current_time_label.setText(self._format_time(time))
			self.progress_bar.setValue(time / self.midi_player.file.length * 100)
		else:
			self.current_time_label.setText("00:00")
			self.progress_bar.setValue(0)

	def _daemon(self):
		while True:
			self.update_time.emit(self.midi_player.current_time)
			sleep(1)

	def _select_file(self) -> None:
		filename, _ = QFileDialog.getOpenFileName(self.mainwindow,
				"Select MIDI file", "", "MIDI files (*.mid)")
		if not filename:
			return

		self._open_file(Path(filename))

	def _open_file(self, file: Path):
		self.opened_file = file
		self.midi_player.open_file(self.opened_file)
		self.title_label.setText(self.opened_file.name)
		self.duration_time_label.setText(self._format_time(self.midi_player.file.length))

	def _play_pause(self) -> None:
		self.midi_player.toggle()
		icon = QStyle.SP_MediaPause if self.midi_player.is_playing() else QStyle.SP_MediaPlay
		self.play_button.setIcon(self.style().standardIcon(icon))

	def _stop(self):
		self.midi_player.stop()

	def _format_time(self, time: float) -> str:
		minutes = int(time // 60)
		seconds = int(time % 60)
		return f"{minutes:02}:{seconds:02}"

	def _open_backend_selector_dialog(self):
		backends = [backend.get_name() for backend in get_available_backends()]
		self.backend_selector_list_widget.clear()
		self.backend_selector_list_widget.addItems(backends)

		if self.midi_player.backend:
			current_backend = self.midi_player.backend.get_name()
			if current_backend in backends:
				self.backend_selector_list_widget.setCurrentRow(backends.index(current_backend))

		self.backend_selector_dialog.show()

	def _open_backend_settings_dialog(self):
		devices = self.midi_player.backend.get_devices()
		self.backend_settings_list_widget.clear()
		self.backend_settings_list_widget.addItems(devices)

		if self.midi_player.backend:
			current_device = self.midi_player.backend.get_device()
			if current_device in devices:
				self.backend_settings_list_widget.setCurrentRow(devices.index(current_device))

		self.backend_settings_dialog.show()

	def _change_backend(self, item: QListWidgetItem):
		new_backend_name = item.text()
		if self.midi_player.backend and (new_backend_name == self.midi_player.backend.get_name()):
			return

		try:
			backend = get_backend_by_name(new_backend_name)()
		except Exception as e:
			self.status_bar.showMessage(f"Error: {e}")
			return

		try:
			self.midi_player.set_backend(backend)
		except Exception as e:
			self.status_bar.showMessage(f"Error: {e}")

	def _change_device(self, item: QListWidgetItem):
		self.midi_player.backend.set_device(item.text())
