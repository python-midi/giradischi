#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#

try:
	from mido.backends import portmidi
except OSError:
	portmidi = None

from giradischi.backends.mido_backend_base import MidoBackendOutputBackendBase

class PortMidiOutputBackend(MidoBackendOutputBackendBase):
	backend = portmidi

	@classmethod
	def get_name(cls):
		return "PortMidi"

	def is_virtual(self):
		return False
