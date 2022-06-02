#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#

from argparse import ArgumentParser
from giradischi.ui import GiradischiUI
from pathlib import Path

def main():
	parser = ArgumentParser(description='Giradischi')
	parser.add_argument('file', nargs='?', default=None, help='File to open', type=Path)
	args = parser.parse_args()

	GiradischiUI(args.file).start_ui()
