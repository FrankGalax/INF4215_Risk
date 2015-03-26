from Controller import *
from AI import *

ai1 = AI()
ai2 = AI()
controller = Controller("Americas", "Pedro", "Redde", ai1, ai2)
controller.play()