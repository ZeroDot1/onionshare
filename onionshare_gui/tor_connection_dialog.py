# -*- coding: utf-8 -*-
"""
OnionShare | https://onionshare.org/

Copyright (C) 2017 Micah Lee <micah@micahflee.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from PyQt5 import QtCore, QtWidgets, QtGui

from onionshare import strings, helpers

class TorConnectionDialog(QtWidgets.QProgressDialog):
    """
    Connecting to Tor dialog.
    """
    def __init__(self, settings, onion):
        super(TorConnectionDialog, self).__init__(None)
        self.settings = settings

        self.setWindowTitle("OnionShare")
        self.setWindowIcon(QtGui.QIcon(helpers.get_resource_path('images/logo.png')))
        self.setModal(True)

        # Label
        self.setLabelText(strings._('connecting_to_tor', True))
        self.setCancelButtonText(strings._('gui_tor_connection_exit', True))

        # Progress bar ticks from 0 to 100
        self.setRange(0, 100)
        # Don't show if connection takes less than 200ms (for non-bundled tor)
        self.setMinimumDuration(200)

        # If bundled tor, prepare to display Tor connection status
        if settings.get('connection_type') == 'bundled':
            tor_status_update = self.tor_status_update
        else:
            tor_status_update = None

        # Connect to the Onion
        self.setValue(0)
        try:
            onion.connect(self.settings, tor_status_update)
        except (TorTooOld, TorErrorInvalidSetting, TorErrorAutomatic, TorErrorSocketPort, TorErrorSocketFile, TorErrorMissingPassword, TorErrorUnreadableCookieFile, TorErrorAuthError, TorErrorProtocolError, BundledTorNotSupported, BundledTorTimeout) as e:
            print(e.args[0])
            # TODO: Open settings to connect to Tor properly
            sys.exit()

        self.exec_()

    def tor_status_update(self, progress, summary):
        if summary == 'Done':
            # All done
            self.close()
        else:
            self.setValue(int(progress))
        self.setLabelText("<strong>{}</strong><br>{}".format(strings._('connecting_to_tor', True), summary))