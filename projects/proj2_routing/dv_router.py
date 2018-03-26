"""Your awesome Distance Vector router for CS 168."""

import sim.api as api
import sim.basics as basics
import time

# We define infinity as a distance of 16.
INFINITY = 16


class DVRouter(basics.DVRouterBase):
    # NO_LOG = True # Set to True on an instance to disable its logging
    # POISON_MODE = True # Can override POISON_MODE here
    # DEFAULT_TIMER_INTERVAL = 5 # Can override this yourself for testing

    def __init__(self):
        """
        Called when the instance is initialized.
        You probably want to do some additional initialization here.
        """
        self.routing_table = {} # {dest : {cost, next_hop}}
        self.neighbors = {} # {port : latency}
        self.start_timer()  # Starts calling handle_timer() at correct rate

    def handle_link_up(self, port, latency):
        """
        Called by the framework when a link attached to this Entity goes up.
        The port attached to the link and the link latency are passed
        in.
        """
        self.neighbors[port] = latency

    def handle_link_down(self, port):
        """
        Called by the framework when a link attached to this Entity does down.
        The port number used by the link is passed in.
        """
        pass

    def handle_rx(self, packet, port):
        """
        Called by the framework when this Entity receives a packet.
        packet is a Packet (or subclass).
        port is the port number it arrived on.
        You definitely want to fill this in.
        """
        #self.log("RX %s on %s (%s)", packet, port, api.current_time())
        
        if isinstance(packet, basics.RoutePacket):
            print "switch: " + self.name
            print "src: " + packet.src.name
            print "latency: " + str(packet.latency)
            print "dst: " + packet.destination.name
            print "port: " + str(port)
        elif isinstance(packet, basics.HostDiscoveryPacket):
            # should monitor for these packets so it knows what hosts exist
            # and where they are attached.
            # should never send/forward these packets
            latency = self.neighbors[port]
            self.neighbors.pop(port)
            self.routing_table[packet.src.name] = port
            
            for port in self.neighbors:
                self.send(basics.RoutePacket(packet.src, latency), port)
        else:
            # Totally wrong behavior for the sake of demonstration only: send
            # the packet back to where it came from!
            self.send(packet, port=port)

    def handle_timer(self):
        """
        Called periodically.
        When called, your router should send tables to neighbors.  It
        also might not be a bad place to check for whether any entries
        have expired.
        """
    pass