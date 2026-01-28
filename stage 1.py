from space_network_lib import SpaceEntity, SpaceNetwork, Packet


class Satellite(SpaceEntity):
    def __init__(self, name, distance_from_earth):
        super().__init__(name, distance_from_earth)

    def receive_signal(self, packet: Packet):
        return f"{self.name} Received: {packet}"

space_net1 = SpaceNetwork(1)

sat1 = Satellite("satellite1", 100)
sat2 = Satellite("satellite2", 200)
new_message = Packet("i found aliens",sat1 ,sat2)
print(space_net1.send(new_message))


