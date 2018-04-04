"""Your awesome Distance Vector router for CS 168."""

import sim.api as api
import sim.basics as basics

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
        self.routing_table = {} # {device : {'port':port, 'cost':cost, 'time':time}}
        self.expired_routes = {} # {device : port}
        self.neighbors = {} # {port : latency}
        self.all_routes = {} # {device : {'port':port, 'cost':cost, 'time':time}}
        self.start_timer()  # Starts calling handle_timer() at correct rate

    def handle_link_up(self, port, latency):
        """
        Called by the framework when a link attached to this Entity goes up.

        The port attached to the link and the link latency are passed
        in.

        """
        # store distance of neighbors
        self.neighbors[port] = latency
        # print "switch " + self.name + " has a neighbor in port " + str(port) + " with latency of " + str(latency)
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
            
            latency = packet.latency + self.neighbors[port]
            current_time = api.current_time()
            self.all_routes[packet.destination] = {'port' : port, 'cost' : latency, 'time' : current_time}
            # print "switch " + self.name + " received a route from " + packet.src.name + " at port " + str(port) + " with latency " + str(latency) + " with destination " + packet.destination

            if packet.destination not in self.routing_table:
                self.routing_table[packet.destination] = {'port' : port, 'cost' : latency, 'time' : current_time }
                # print "added to routing table: " + packet.destination.name + "at port " + str(port) + " with latency of " + str(self.routing_table[packet.destination.name]['cost'])
                for p in self.neighbors:
                    if p != port:
                        self.send(basics.RoutePacket(packet.destination, self.neighbors[port] + packet.latency), p)
                    else:
                        if self.POISON_MODE:
                            self.send(basics.RoutePacket(packet.destination, INFINITY), p)
            else:
                old_latency = self.routing_table[packet.destination]['cost']
                # print "switch " + self.name + " found a new route from " + packet.src.name + " at port " + str(port) + " with latency " + str(latency) + " with destination " + packet.destination
                if old_latency > latency:
                    self.routing_table[packet_destination]['cost'] = latency
                    self.routing_table[packet_destination]['port'] = port
                    # print "switch " + self.name + " updated its routing table." + " route to " + packet.destination + " is from " + packet.src.name + " at port " + str(self.routing_table[packet_destination]['port'])
                    for n in self.neighbors:
                        if n != port:
                            self.send(basics.RoutePacket(packet.destination, latency), n)                        
            
        # dapat na send ghap kita dd hin routepacket ha other neighbors na switch
        elif isinstance(packet, basics.HostDiscoveryPacket):
            # should monitor for these packets so it knows what hosts exist
            # and where they are attached.
            # should never send/forward these packets
 
            # get distance to include in route packet
            if self.neighbors.has_key(port):
                latency = self.neighbors[port]
                # print "switch: " + self.name + " is connected to " + packet.src.name + " at port " + str(port) + " with latency " + str(latency)
                self.neighbors.pop(port, None)
                current_time = api.current_time()
                self.all_routes[packet.src.name] = {'port' : port, 'cost' : latency, 'time' : current_time}
                self.routing_table[packet.src.name] = {'port' : port, 'cost' : latency, 'time' : current_time}
            
                for p in self.neighbors:
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
                self.expired_routes[n] = self.routing_table[n]['port']

        for n in self.expired_routes:
            self.routing_table.pop(n, None)

        print "switch " + self.name + "'s routes"
        print self.all_routes
        # for n in self.neighbors:
        #     if n == self.routing_table[d]['port']:          
        #         self.send(basics.RoutePacket(d, self.routing_table[d]['cost']), self.routing_table[d]['port'])

        # print "expired rotes: " + self.expired_routes
        self.expired_routes.clear()
        # print "expired rotes new: " + self.expired_routes

        # for n in self.neighbors:
        #     for d in self.routing_table:
        #         if n == self.routing_table[d]['port']:
        #             self.send(basics.RoutePacket(d, self.routing_table[d]['cost']), n)