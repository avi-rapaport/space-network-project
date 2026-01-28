from space_network_lib import *
import time
class BrokenConnectionError(CommsError):
    pass



class Satellite(SpaceEntity):
    def __init__(self, name, distance_from_earth):
        super().__init__(name, distance_from_earth)

    def receive_signal(self, packet: Packet):
        return f"{self.name} Received: {packet}"


def attempt_transmission(network, packet):
    try:
        network.send(packet)
    except TemporalInterferenceError:
        print("Interference, waiting ...")
        time.sleep(2)
        attempt_transmission(network,packet)
    except DataCorruptedError:
        print("corrupted, retrying...")
        attempt_transmission(network,packet)
    except LinkTerminatedError:
        raise BrokenConnectionError("link lost")
    except OutOfRangeError:
        raise BrokenConnectionError("Target out of range")


