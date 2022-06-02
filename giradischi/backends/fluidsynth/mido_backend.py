#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#

from fluidsynth import Synth
from mido.ports import BaseOutput

def get_devices():
	return [
		{
			'name': 'default',
			'is_input': False,
			'is_output': True,
		},
	]

# Apparently we can't create attributes on BaseOutput classes
_synths: dict[int, Synth] = {}
_sfids: dict[int, int] = {}

class Output(BaseOutput):
	def _open(self, **kwargs):
		self_id = id(self)

		_synths[self_id] = Synth()
		synth = _synths[self_id]

		# TODO: Add Soundfont GUI settings
		synth.setting("audio.driver", "pulseaudio")
		synth.start()
		_sfids[self_id] = synth.sfload("/usr/share/sounds/sf2/FluidR3_GM.sf2", 1)

	def _close(self):
		self_id = id(self)

		if not self_id in _synths:
			return

		synth = _synths[self_id]

		if self_id in _sfids:
			synth.sfunload(_sfids[self_id], 1)
			del _sfids[self_id]

		synth.delete()
		del _synths[self_id]

	def _send(self, message):
		self_id = id(self)

		if self_id not in _synths:
			return

		synth = _synths[self_id]

		if message.type == 'note_on':
			synth.noteon(message.channel, message.note, message.velocity)
		elif message.type == 'note_off':
			synth.noteoff(message.channel, message.note)
		elif message.type == 'control_change':
			synth.cc(message.channel, message.control, message.value)
		elif message.type == 'pitchwheel':
			synth.pitch_bend(message.channel, message.pitch)
		elif message.type == 'program_change':
			synth.program_change(message.channel, message.program)
		else:
			print(f"Unimplemented message type: {message.type}")
