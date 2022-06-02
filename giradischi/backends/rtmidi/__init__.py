#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#

try:
	from mido.backends import rtmidi
except ModuleNotFoundError:
	try:
		from mido.backends import rtmidi_python as rtmidi
	except ModuleNotFoundError:
		rtmidi = None

from giradischi.backends.mido_backend_base import MidoBackendOutputBackendBase

class RtMidiOutputBackend(MidoBackendOutputBackendBase):
	backend = rtmidi

	@classmethod
	def get_name(cls):
		return "RtMidi"

	def is_virtual(self):
		return False
