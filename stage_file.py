from space_network_lib import *
import time
import random
import string


class BrokenConnectionError(CommsError):
    pass


class SecurityBreachError(CommsError):
    pass


space_net = SpaceNetwork(7)


def attempt_transmission(packet):
    while True:
        try:
            space_net.send(packet)
            return
        except TemporalInterferenceError:
            print("Interference, waiting ...")
            time.sleep(2)
            continue
        except DataCorruptedError:
            print("corrupted, retrying...")
            continue
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

        next_jump = max(options, key=lambda e: abs(e.distance_from_earth - current.distance_from_earth))
        route.append(next_jump)
        visited.add(next_jump)
        current = next_jump

    print("Route found:", " -> ".join(e.name for e in route))

    current_sender = packet.sender
    for i in range(len(route)):
        destination = route[i]
        if isinstance(packet, EncryptedPacket):
            step_packet = Packet(packet.data, current_sender, destination)
        else:
            step_packet = Packet(packet.data, current_sender, destination)

        print(f"Transmitting from {current_sender.name} to {destination.name}...")
        attempt_transmission(step_packet)
        current_sender = destination



class RelayPacket(Packet):
    def __init__(self, packet_to_relay, sender, proxy):
        super().__init__(packet_to_relay, sender, proxy)

    def __repr__(self):
        return f"Relaying[{self.data}]to {self.receiver} from {self.sender}"


class EncryptedPacket(Packet):
    def __init__(self, data, sender, receiver, key=None):
        if key is None:
            key = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        self._key = key
        encrypted = self._xor_data(data, self._key)
        for i, ch in enumerate(data):
            encrypted_char = chr(ord(ch) ^ ord(self._key[i % len(self._key)]))
            encrypted += encrypted_char
        super().__init__(encrypted, sender, receiver)
        self.__original_data = data

    def _xor_data(self, data, key):
        result = ""
        for i, ch in enumerate(data):
            result += chr(ord(ch) ^ ord(key[i % len(key)]))
        return result

    def decrypt(self, key_attempt):
        if key_attempt != self._key:
            raise SecurityBreachError("invalid key")
        return self._xor_data(self.data, self._key)




class Satellite(SpaceEntity):
    def __init__(self, name, distance_from_earth):
        super().__init__(name, distance_from_earth)

    def receive_signal(self, packet: Packet):
        inner_packet = packet.data
        if isinstance(packet, RelayPacket):
            print(f"{self.name} received (encrypted): {packet.data}")
            print(f"Unwrapping and forwarding to {inner_packet.receiver}")
            attempt_transmission(inner_packet)
        else:
            print(f"Final destination reached: {packet.data}")


class Earth(SpaceEntity):
    def __init__(self, name, distance_from_earth):
        super().__init__(name, distance_from_earth)

    def receive_signal(self, packet: Packet):
        if isinstance(packet, EncryptedPacket):
            try:
                decrypted_text = packet.decrypt(packet._key)
                print(f"{self.name} Received (decrypted): {decrypted_text}")
            except SecurityBreachError as e:
                print(f"{self.name} Could not decrypt packet: {e}")
        print(f"{self.name} Received: {packet.data}")
