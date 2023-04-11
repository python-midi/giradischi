#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#

from libmidi_io.types.backend import BackendModule
from libmidi_io.types.port import BasePort
from typing import List, Optional

class BaseMidiOutputBackend:
	"""MIDI output backend."""
	def __init__(self, name: str, backend: BackendModule):
		"""Initialize the MIDI output backend."""
		self.name = name
		self.backend = backend

		self.device: Optional[str] = None

		devices = self.get_devices()
		if devices:
			self.device = devices[0]

	def get_devices(self) -> List[str]:
		"""
		Returns a list of MIDI output devices available on the system.

		If only one device is always available (like for virtual synthesizers), either return
		the name of the device or a dummy one (like "default" or "virtual").
		If no device is available, return an empty list.
		"""
		devices = self.backend.get_devices()

		return [device.name for device in devices if device.is_output]

	def get_device(self) -> Optional[str]:
		"""Returns the current MIDI device."""
		return self.device

	def set_device(self, device: str) -> None:
		"""
		Sets the MIDI device to use.

		Value should be one of the values returned by get_devices().
		"""
		devices = self.get_devices()

		assert device in devices, "Device not found"

		self.device = device

	def open_device(self, **kwargs) -> BasePort:
		"""
		Opens the MIDI device.

		Returns a BaseOutput instance.
		Assert that the device is set before calling this function.
		"""
		assert self.device is not None, "No device set"

		return self.backend.Port(name=self.device, **kwargs)
