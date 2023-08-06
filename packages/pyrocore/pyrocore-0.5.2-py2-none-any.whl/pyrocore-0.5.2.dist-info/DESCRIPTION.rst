This project provides a collection of tools for the BitTorrent protocol
and especially the `rTorrent client`_. They enable you to filter
rTorrent's item list for displaying or changing selected items, also
creating, inspecting and changing ``.torrent`` files, and much more.

An optional daemon process (``pyrotorque``) can add flexible queue
management for rTorrent, starting items added in bulk slowly over time
according to customizable rules. The same daemon can also watch one or
more directory trees recursively for new metafiles using inotify,
resulting in instantaneous loading without any polling and no extra
configuration for nested directories.

The ``PyroScope`` command line utilities are *not* the same as the
sibling project `rTorrent-PS`_, and they work perfectly fine without it;
the same is true the other way 'round. It's just that both
unsurprisingly have synergies if used together, and some features *do*
only work when both are present.

Further information can be found in the `main documentation`_.

To get in contact and share your experiences with other users of *PyroScope*,
join the `pyroscope-users`_ mailing list or the inofficial ``##rtorrent``
channel on ``irc.freenode.net``.

.. _rTorrent client: https://github.com/rakshasa/rtorrent
.. _rTorrent-PS: https://github.com/pyroscope/rtorrent-ps
.. _main documentation: http://pyrocore.readthedocs.io/
.. _pyroscope-users: http://groups.google.com/group/pyroscope-users

Copyright (c) 2009 - 2017 The PyroScope Project <pyroscope.project@gmail.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

