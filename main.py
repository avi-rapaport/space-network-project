from space_network_lib import *
from stage_file import *

space_net = SpaceNetwork(3)
sat1 = Satellite("satellite1", 100)
sat2 = Satellite("satellite2", 200)
new_message = Packet("i found aliens", sat1, sat2)
#space_net.send(new_message)
try:
    attempt_transmission(space_net,new_message)
except BrokenConnectionError:
    print("Transmission failed")
