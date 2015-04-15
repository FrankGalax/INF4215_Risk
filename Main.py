from Controller import *
from MLAgent import *
from AI import *
from RandomAI import *
from FMAI import *

ai1 = MLAgent() # agent adverse avec apprentissage machine
#ai1 = RandomAI() # agent adverse aleatoire
#ai1 = AI() # agent adverse sans apprentissage machine

nbWin = 0
for i in xrange(100):
    ai2 = FMAI(0.5)
    controller = Controller("Americas", "Scrubby", "FM", ai1, ai2)
    winningPlayerIndex = controller.play()
    if winningPlayerIndex == 1:
        nbWin += 1
print nbWin