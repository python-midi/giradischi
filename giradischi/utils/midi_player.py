#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#

from mido import MidiFile
from pathlib import Path
from threading import Thread, Event
from time import sleep, time

from giradischi.backends import DEFAULT_BACKEND
from giradischi.backends.base import MidiOutputBackendBase

class MidiPlayer:
	"""A basic MIDI player, with play/pause/stop functionality."""
	def __init__(self, backend: MidiOutputBackendBase = None) -> None:
		"""Create a new MIDI player."""
		self.backend = backend if backend else DEFAULT_BACKEND()
		self.file: MidiFile = None

		self.is_started = False

		self.play_event = Event()
		self.stop_event = Event()

		self.current_time = 0.0

		self.thread = Thread(target=self._daemon, daemon=True)
		self.thread.start()

	def set_backend(self, backend: MidiOutputBackendBase) -> None:
		if self.is_started:
			raise RuntimeError("Cannot change backend while playing, stop first")

		self.backend = backend

	def is_playing(self) -> bool:
		"""Return True if the player is currently playing."""
		return self.is_started and self.play_event.is_set()

	def is_paused(self) -> bool:
		"""Return True if the player is currently paused but a file is loaded."""
		return self.is_started and not self.is_playing()

	def is_stopped(self) -> bool:
		"""Return True if the player is currently stopped and no file is loaded."""
		return not self.is_started

	def _daemon(self) -> None:
		while True:
			self.play_event.wait()
			self.stop_event.clear()
			with self.backend.open_device() as output:
				self.is_started = True

				start_time = time()
				self.current_time = 0.0

				for msg in self.file:
					self.current_time += msg.time

					playback_time = time() - start_time
					duration_to_next_event = self.current_time - playback_time

					if duration_to_next_event > 0.0:
						sleep(duration_to_next_event)

					if msg.is_meta:
						continue

					if self.stop_event.is_set():
						output.reset()
						break

					if self.play_event.is_set():
						output.send(msg)
					else:
						# Panic if the user has paused the playback
						output.panic()
						self.play_event.wait()

				self.is_started = False

			self.current_time = 0.0
			self.play_event.clear()
			self.stop_event.clear()

	def open_file(self, midi_file: Path) -> None:
		"""Stops the current playing file if needed and loads a new one."""
		self.stop()
		self.file = MidiFile(midi_file)

	def play(self) -> None:
		"""Start playing the current file."""
		if self.is_playing():
			return

		if not self.file:
			return

		self.play_event.set()

	def pause(self) -> None:
		"""Pause the current playing file."""
		if self.is_paused():
			return

		self.play_event.clear()

	def toggle(self) -> None:
		"""Either play or pause the current file."""
		if self.is_playing():
			self.pause()
		else:
			self.play()

	def stop(self) -> None:
		"""Stop the current playing file and unload it from the daemon."""
		if self.is_stopped():
			return

		self.stop_event.set()
		# Let the thread resume and handle the stop event
		self.play_event.set()
