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
    print("Distance too great Searching for satellite path...")
    entities = sorted(ent_list, key=lambda satellite: satellite.distance_from_earth)

    route = []
    visited = set()
    current = packet.sender
    target = packet.receiver

    while True:
        if abs(target.distance_from_earth - current.distance_from_earth) <= 150:
            route.append(target)
            break

        options = []

        for e in entities:
            if e is current or e in visited:
                continue

            dist = e.distance_from_earth - current.distance_from_earth
            target_dir = target.distance_from_earth - current.distance_from_earth
            if abs(dist) <= 150 and dist * target_dir > 0:
                options.append(e)

        if not options:
            raise BrokenConnectionError("No valid route to target")

        next_jump = max(options,key=lambda e: abs(e.distance_from_earth - current.distance_from_earth))
        route.append(next_jump)
        visited.add(next_jump)
        current = next_jump



    print("Route found:", " -> ".join(e.name for e in route))

    prev = packet.sender

    for jump in route:
        relay = RelayPacket(Packet(packet.data, prev, jump), prev, jump)
        attempt_transmission(relay)
        prev = jump


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
