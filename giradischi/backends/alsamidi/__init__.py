#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#

try:
	from alsa_midi import mido_backend
except ModuleNotFoundError:
	mido_backend = None

from platform import system

from giradischi.backends.mido_backend_base import MidoBackendOutputBackendBase

class AlsaMidiOutputBackend(MidoBackendOutputBackendBase):
	backend = mido_backend

	@classmethod
	def get_name(cls):
		return "ALSA MIDI"

	@classmethod
	def is_available(cls):
		return super().is_available() is not None and system() == "Linux"

	def is_virtual(self):
		return False
