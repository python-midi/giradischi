#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#

from sebaubuntu_libs.liblogging import setup_logging

from giradischi.ui import GiradischiUI

def main():
	setup_logging()

	GiradischiUI().start_ui()
