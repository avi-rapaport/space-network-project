
from stage_file import *

earth = Earth("earth", 0)
sat1 = Satellite("satellite1", 100)
sat2 = Satellite("satellite2", 140)
sat3 = Satellite("satellite3", 250)
sat4 = Satellite("satellite4", 220)
sat5 = Satellite("satellite5", 400)

new_message = Packet("i found aliens", earth, sat5)
p_final = Packet("hello from earth", sat3, sat4)
p_sat2_to_set3 = RelayPacket(p_final, sat2, sat3)
p_sat1_to_set2 = RelayPacket(p_sat2_to_set3, sat1, sat2)
p_earth_to_set1 = RelayPacket(p_sat1_to_set2, earth, sat1)
entities = [earth, sat1, sat2, sat3, sat4, sat5]

# space_net.send(new_message)
# try:
#     attempt_transmission(p_earth_to_set1)
# except BrokenConnectionError:
#     print("Transmission failed")

encrypted_msg = EncryptedPacket("hello aliens",earth, sat5)

smart_send_packet(encrypted_msg, entities)
