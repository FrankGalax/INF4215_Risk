from Controller import *
from MLAgent import *
from AI import *
from FMAI import *

ai1 = AI()
nbWin = 0
for i in xrange(1):
    ai2 = FMAI(0.5)
    controller = Controller("Americas", "Basic", "FM", ai1, ai2)
    winningPlayerIndex = controller.play()
    if winningPlayerIndex == 1:
        nbWin += 1
print nbWin