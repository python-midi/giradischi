#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#

try:
	from giradischi.backends.fluidsynth import mido_backend
except (ImportError, ModuleNotFoundError):
	mido_backend = None

from giradischi.backends.mido_backend_base import MidoBackendOutputBackendBase

class FluidSynthOutputBackend(MidoBackendOutputBackendBase):
	backend = mido_backend

	@classmethod
	def get_name(cls):
		return "FluidSynth"

	def is_virtual(self):
		return True
