#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#

from mido.ports import BaseOutput
from typing import Callable, Type

from giradischi.backends.base import MidiOutputBackendBase

class MidoBackend:
	get_devices: Callable[[], list[dict]]
	Output: Type[BaseOutput]

class MidoBackendOutputBackendBase(MidiOutputBackendBase):
	backend: Type[MidoBackend]
	api: str

	def __init__(self) -> None:
		super().__init__()

		self.device = None

		devices = self.get_devices()
		if devices:
			self.device = devices[0]

	@classmethod
	def is_available(cls):
		return cls.backend is not None

	def can_have_multiple_devices(self):
		return True

	def get_devices(self):
		devices = self.backend.get_devices()

		return [device["name"] for device in devices if device["is_output"]]

	def get_device(self):
		return self.device

	def set_device(self, device: str):
		devices = self.get_devices()

		assert device in devices, "Device not found"

		self.device = device

	def open_device(self, **kwargs):
		assert self.device, "No device set"

		return self.backend.Output(self.device, **self._add_api(kwargs))

	# Utils
	def _add_api(self, kwargs):
		"""Adds the API to the keyword arguments."""
		if getattr(self, 'api', None) and 'api' not in kwargs:
			kwargs['api'] = self.api
		return kwargs
