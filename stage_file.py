from space_network_lib import *
import time


class BrokenConnectionError(CommsError):
    pass


space_net = SpaceNetwork(5)


def attempt_transmission(packet):
    try:
        space_net.send(packet)
    except TemporalInterferenceError:
        print("Interference, waiting ...")
        time.sleep(2)
        attempt_transmission(packet)
    except DataCorruptedError:
        print("corrupted, retrying...")
        attempt_transmission(packet)
    except LinkTerminatedError:
        raise BrokenConnectionError("link lost")
    except OutOfRangeError:
        raise BrokenConnectionError("Target out of range")

def smart_send_packet(packet, ent_list):





class RelayPacket(Packet):
    def __init__(self, packet_to_relay, sender, proxy):
        super().__init__(packet_to_relay, sender, proxy)

    def __repr__(self):
        return f"Relaying[{self.data}]to {self.receiver} from {self.sender}"


class Satellite(SpaceEntity):
    def __init__(self, name, distance_from_earth):
        super().__init__(name, distance_from_earth)

    def receive_signal(self, packet: Packet):
        inner_packet = packet.data
        if isinstance(packet, RelayPacket):
            print(f"Unwrapping and forwarding to {inner_packet.receiver}")
            attempt_transmission(inner_packet)
        else:
            print(f"Final destination reached: {packet.data}")


class Earth(SpaceEntity):
    def __init__(self, name, distance_from_earth):
        super().__init__(name, distance_from_earth)

    def receive_signal(self, packet: Packet):
        print(f"{self.name} Received: {packet}")



