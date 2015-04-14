from Controller import *
from MLAgent import *
from AI import *
from FMAI import *

ai1 = MLAgent()
nbWin = 0
for i in xrange(100):
    ai2 = FMAI(0.5)
    controller = Controller("Americas", "Scrubby", "FM", ai1, ai2)
    winningPlayerIndex = controller.play()
    if winningPlayerIndex == 1:
        nbWin += 1
print nbWin