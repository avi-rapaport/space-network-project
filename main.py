from space_network_lib import *
from stage_file import *


sat1 = Satellite("satellite1", 100)
sat2 = Satellite("satellite2", 200)
earth = Earth("earth", 0)
new_message = Packet("i found aliens", sat1, sat2)
p_final = Packet("hello from earth", sat1, sat2)
p_earth_to_set1 = RelayPacket(p_final, earth, sat1)

#space_net.send(new_message)
try:
    attempt_transmission(p_earth_to_set1)
except BrokenConnectionError:
    print("Transmission failed")
