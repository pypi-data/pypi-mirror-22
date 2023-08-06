``peng3d_sphinxext`` - A Sphinx plugin adding support for `peng3d <https://github.com/not-na/peng3d>`_ events
=============================================================================================================

This Sphinx plugin adds support for `peng3d Events <http://peng3d.readthedocs.io/en/latest/events.html>`_\ .
It also supports old-style pyglet events sent via peng3d.

Short documentation
*******************

There are only two directives added by ``peng3d_sphinxext``::

    .. peng3d:event:: some:event.name
      
        Documentation for the event.
and

    .. peng3d:pgevent:: on_pyglet_event
        
        Documentation for a pyglet event.

These directives can be referred to as usual, via ``:peng3d:event:`some:event.name` `` and ``:peng3d:pgevent:`on_pyglet_event` ``.
