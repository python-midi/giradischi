#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
"""giradischi KDMAPI backend."""

try:
	from kdmapi import KDMAPI, mido_backend
except (OSError, ModuleNotFoundError):
	KDMAPI = None
	mido_backend = None

from giradischi.backends.mido_backend_base import MidoBackendOutputBackendBase

class KDMAPIOutputBackend(MidoBackendOutputBackendBase):
	backend = mido_backend

	@classmethod
	def get_name(cls):
		return "Keppy's Direct MIDI"

	@classmethod
	def is_available(cls):
		return super().is_available() and KDMAPI and KDMAPI.IsKDMAPIAvailable()

	def is_virtual(self):
		return True
