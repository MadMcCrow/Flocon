# PyQt installer for NixOS
from Flocon.App      import FloconApp
from Flocon.Widgets  import *
from Flocon.Locale   import *
from Flocon.Disks    import *

class FirstPage(Page) :
    def __init__(self, parent = None):
        Page.__init__(self, parent)
        #create questions
        self.hostname = Question(*HOSTNAME)
        self.username = Question(*USERNAME)
        self.password = Question(*INITPSWD, True)
        # create group
        group = Group(HOSTINFO, self)
        group.addWidgets([self.hostname, self.username, self.password])
        # add widgets
        self.addWidgets([Banner(INTRO, self), group])


# Launch app :
App = FloconApp(PROGNAME)
App.run([FirstPage()])
