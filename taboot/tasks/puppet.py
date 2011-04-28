# -*- coding: utf-8 -*-
# Taboot - Client utility for performing deployments with Func.
# Copyright © 2009-2011, Red Hat, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from taboot.tasks import command

PUPPET_LOCKFILE = "/var/lib/puppet/state/puppetdlock"


class Run(command.Run):
    """
    Run 'puppetd --test || true'

    See also: SafeRun
    """

    def __init__(self, **kwargs):
        super(Run, self).__init__('puppetd --test --color=false || true',
                                  **kwargs)


class SafeRun(command.Run):
    """
    Run 'puppetd --test'.

    How is this different from Run? Simple, it will abort everything
    if puppet returns with a non-zero exit status.
    """

    def __init__(self, **kwargs):
        super(SafeRun, self).__init__('puppetd --test --color=false',
                                  **kwargs)


class Enable(command.Run):
    """
    Run 'puppetd --enable'.
    """

    def __init__(self, **kwargs):
        super(Enable, self).__init__('puppetd --enable', **kwargs)


class Disable(command.Run):
    """
    Run 'puppetd --disable'.
    """

    def __init__(self, **kwargs):
        super(Disable, self).__init__('puppetd --disable', **kwargs)


class DeleteLockfile(command.Run):
    """
    Remove the puppet lock file.

    """

    def __init__(self, **kwargs):
        super(DeleteLockfile, self).__init__("rm -f %s" % PUPPET_LOCKFILE,
                                             **kwargs)
