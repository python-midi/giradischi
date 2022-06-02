#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#

from mido.ports import BaseOutput

class MidiOutputBackendBase:
	"""MIDI output backend."""
	def __init__(self):
		"""Initialize the MIDI output backend."""
		if not self.is_available():
			raise RuntimeError("Backend not available")

	@classmethod
	def get_name(cls) -> str:
		"""Returns the name of the backend."""
		raise NotImplementedError

	@classmethod
	def is_available(cls) -> bool:
		"""Returns True if the backend is available on the system."""
		raise NotImplementedError

	def is_virtual(self) -> bool:
		"""Returns True if the device is virtual."""
		raise NotImplementedError

	def can_have_multiple_devices(self) -> bool:
		"""Returns True if the backend can have multiple devices."""
		raise NotImplementedError

	def get_devices(self) -> list[str]:
		"""Returns a list of MIDI output devices available on the system.

		If only one device is always available (like for virtual synthesizers), either return
		the name of the device or a dummy one (like "default" or "virtual").
		If no device is available, return an empty list.
		"""
		raise NotImplementedError

	def get_device(self) -> str:
		"""Returns the current MIDI device.

		If can_have_multiple_devices() returns False,
		return the device returned by get_devices()."""
		raise NotImplementedError

	def set_device(self, device: str) -> None:
		"""Sets the MIDI device to use.

		Value should be one of the values returned by get_devices().

		If can_have_multiple_devices() returns False, don't implement this method."""
		raise NotImplementedError

	def open_device(self, **kwargs) -> BaseOutput:
		"""Opens the MIDI device.

		Returns a BaseOutput instance.
		Assert that the device is set before calling this function.
		"""
		raise NotImplementedError
