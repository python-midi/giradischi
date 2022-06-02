#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
"""giradischi MIDI output backends"""

from typing import Type

from giradischi.backends.base import MidiOutputBackendBase

# Backends
from giradischi.backends.alsamidi import AlsaMidiOutputBackend
from giradischi.backends.fluidsynth import FluidSynthOutputBackend
from giradischi.backends.portmidi import PortMidiOutputBackend
from giradischi.backends.rtmidi import RtMidiOutputBackend

BACKENDS: list[Type[MidiOutputBackendBase]] = [
	AlsaMidiOutputBackend,
	FluidSynthOutputBackend,
	PortMidiOutputBackend,
	RtMidiOutputBackend,
]

DEFAULT_BACKEND = RtMidiOutputBackend

def get_available_backends() -> list[Type[MidiOutputBackendBase]]:
	"""Get a list of available backends."""
	return [backend for backend in BACKENDS if backend.is_available()]

def get_backend_by_name(name: str):
	"""Find a backend by name."""
	for backend in BACKENDS:
		if backend.get_name() == name:
			return backend

	raise ValueError(f"Backend {name} not found")
