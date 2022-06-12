#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
"""giradischi MIDI output backends."""

from libmidi_io.backends import get_available_backends

from giradischi.backends.base import BaseMidiOutputBackend

backends = [
	BaseMidiOutputBackend(name, backend)
	for name, backend in get_available_backends().items()
]

def get_backend_by_name(name: str):
	"""Find a backend by name."""
	for backend in backends:
		if backend.name == name:
			return backend

	raise ValueError(f"Backend {name} not found")
