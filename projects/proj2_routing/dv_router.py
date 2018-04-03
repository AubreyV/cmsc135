"""Your awesome Distance Vector router for CS 168."""

import sim.api as api
import sim.basics as basics

# We define infinity as a distance of 16.
INFINITY = 16


class DVRouter(basics.DVRouterBase):
    # NO_LOG = True # Set to True on an instance to disable its logging
    POISON_MODE = True # Can override POISON_MODE here
    # DEFAULT_TIMER_INTERVAL = 5 # Can override this yourself for testing

    def __init__(self):
        """
        Called when the instance is initialized.

        You probably want to do some additional initialization here.

        """
        self.routing_table = {} # {device : {port, cost, time}}
        self.expired_routes = {} # {device : port}
        self.neighbors = {} # {port : latency}
        self.start_timer()  # Starts calling handle_timer() at correct rate

    def handle_link_up(self, port, latency):
        """
        Called by the framework when a link attached to this Entity goes up.

        The port attached to the link and the link latency are passed
        in.

        """
        # store distance of neighbors
        self.neighbors[port] = latency
        
        for n in self.routing_table:
            self.send(basics.RoutePacket(n, self.routing_table[n]['cost']), port)

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

        You definitely want.0. to fill this in.

        """
        #self.log("RX %s on %s (%s)", packet, port, api.current_time())
        
        if isinstance(packet, basics.RoutePacket):
            current_time = api.current_time()

            # print "switch: " + self.name
            # print "Latency: " + str(packet.latency + self.neighbors[port])
            
            if packet.destination not in self.routing_table:
                self.routing_table[packet.destination] = {'port' : port, 'cost' : self.neighbors.get(port) + packet.latency, 'time' : current_time }
                # print "added to routing table: " + packet.destination.name + "at port " + str(port) + " with latency of " + str(self.routing_table[packet.destination.name]['cost'])
                for p in self.neighbors:
                    if p != port:
                        self.send(basics.RoutePacket(packet.destination, self.neighbors[port] + packet.latency), p)
            else:
                if self.routing_table[packet.destination]['port'] != port:
                    min_cost = self.routing_table[packet.destination]['cost']
                else:
                    min_cost = self.neighbors[port] + packet.latency

                if packet.latency + self.neighbors[port] <= min_cost:
                    min_cost = packet.latency + self.neighbors[port]

                if min_cost != self.routing_table[packet.destination]['cost']:
                    self.routing_table[packet.destination] = {'port': port, 'cost' : min_cost, 'time' : current_time}

                for p in self.neighbors:
                    if p != port:
                        self.send(basics.RoutePacket(packet.destination, min_cost), p)

            
        # dapat na send ghap kita dd hin routepacket ha other neighbors na switch
        elif isinstance(packet, basics.HostDiscoveryPacket):
            # should monitor for these packets so it knows what hosts exist
            # and where they are attached.
            # should never send/forward these packets

            current_time = api.current_time()
            # get distance to include in route packet
            latency = self.neighbors[port]
            self.routing_table[packet.src.name] = {'port' : port, 'cost' : latency, 'time' : current_time}
            
            for p in self.neighbors:
                # do not send to the source of the discovery packet
                if p != port:
                    self.send(basics.RoutePacket(packet.src.name, latency), p)
        else:
            # Totally wrong behavior for the sake of demonstration only: send
            # the packet back to where it came from!
            # =====ping=====
            
            if packet.dst.name in self.routing_table:
                if packet.dst.name not in self.expired_routes:
                    self.send(packet, self.routing_table[packet.dst.name]['port'])

    def handle_timer(self):
        """
        Called periodically.

        When called, your router should send tables to neighbors.  It
        also might not be a bad place to check for whether any entries
        have expired.

        """
        # print self.routing_table
        for n in self.routing_table:
            if (api.current_time() - self.routing_table[n]['time']) > 15.0:
                # print "deleted: " + n
                self.expired_routes[n] = self.routing_table[n]['port']

        for n in self.expired_routes:
            self.routing_table.pop(n, "None")

        for n in self.neighbors:
            for d in self.routing_table:
                if n == self.routing_table[d]['port']:
                    self.send(basics.RoutePacket(d, self.routing_table[d]['cost']), n)

