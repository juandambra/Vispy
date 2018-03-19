import sys

import rtmidi
from vispy.app import use_app, Application
from vispy.ext.six import string_types
from vispy.util.event import EmitterGroup, Event


class MidiInputHandler(object):
    def __init__(self, midiMonitor, port):
        #self.port = port
        #self._wallclock = time.time()
        self.midiMonitor = midiMonitor

    def __call__(self, event, data=None):
        message= event[0]
        #self._wallclock += deltatime
        self.midiMonitor._midiIn(message)
        # print("[%s] @%0.6f %r" % (self.port, self._wallclock, message))



class MidiMonitor(object):
    def __init__(self, connect=None, start=True, app=None):
        self.events = EmitterGroup(source=self,
                                   start=Event,
                                   stop=Event,
                                   midiIn=Event)

        if app is None:
            self._app = use_app(call_reuse=False)
        elif isinstance(app, Application):
            self._app = app
        elif isinstance(app, string_types):
            self._app = Application(app)
        else:
            raise ValueError('Invalid value for app %r' % app)
        self._running = False
        if connect is not None:
            self.connect(connect)
        if start:
            self.start()

    @property
    def running(self):
        return self._running

    def start(self):
        if self.running:
            return  # don't do anything if already running
        port = sys.argv[1] if len(sys.argv) > 1 else None
        try:
            self.midiin = rtmidi.MidiIn(name="game")
            available_ports = self.midiin.get_ports()
            if available_ports:
                self.midiin.open_port(0)
            else:
                self.midiin.open_virtual_port("My virtual output")
        except (EOFError, KeyboardInterrupt):
            sys.exit()
        self.midiInputHandler = MidiInputHandler(self, port)
        self.midiin.set_callback(self.midiInputHandler)
        self._running = True
        self.events.start(type='midi_start')
        print(self.midiin)

    def stop(self):
        self.events.stop(type='midi_stop')

    def _midiIn(self, message):
        if not self.running:
            return
        if message[0] == 144:
            print(message)
            self.events.midiIn(type='midi_in', message=message)

    def connect(self, callback):
        return self.events.midiIn.connect(callback)

    def disconnect(self, callback=None):
        return self.events.midiIn.disconnect(callback)