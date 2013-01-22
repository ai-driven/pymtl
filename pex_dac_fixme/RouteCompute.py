#=========================================================================
# RouteCompute
#=========================================================================
# This class implements the logic for route computation based on greedy
# routing algorithm. We assume a ring network with provided netmsg_params
# parameters, obtained from the net_msgs model, to calculate a route. We
# use each routers_id and route information to caculate the route.

from   pymtl import *
import pmlib

from   math import log,ceil,sqrt

import pmlib.net_msgs   as net_msgs
from   pmlib.TestVectorSimulator import TestVectorSimulator

class RouteCompute (Model):

  @capture_args
  def __init__( s, router_x_id, router_y_id, num_routers, netmsg_params ):

    # Local Constants

    s.netmsg_params = netmsg_params

    # Note: Currently, converting a linear router_id into the x and y
    # dimensions assumes square torus networks with the number of nodes to
    # be a power of 2**n
    # CHANGED: Assuming that we pass in the x,y mapping to the router and
    # preserve it once it has been statically elaborated

    s.dim_nbits      = int( sqrt( netmsg_params.srcdest_nbits ) )
    s.num_routers_1D = int( sqrt( num_routers ) )

    # Interface Ports

    s.dest          = InPort  ( netmsg_params.srcdest_nbits )
    s.route         = OutPort ( 3 )

    # Temporary Wires

    s.dist_east     = Wire    ( s.dim_nbits )
    s.dist_west     = Wire    ( s.dim_nbits )
    s.dist_north    = Wire    ( s.dim_nbits )
    s.dist_south    = Wire    ( s.dim_nbits )

    s.x_dest        = Wire    ( s.dim_nbits )
    s.y_dest        = Wire    ( s.dim_nbits )
    s.x_self        = Wire    ( s.dim_nbits )
    s.y_self        = Wire    ( s.dim_nbits )

    connect( s.x_self, router_x_id )
    connect( s.y_self, router_y_id )

    #connect( s.x_dest, s.dest[ 0           :   s.dim_nbits ] )
    #connect( s.y_dest, s.dest[ s.dim_nbits : 2*s.dim_nbits ] )

    # Route Constants

    s.north = 0
    s.east  = 1
    s.south = 2
    s.west  = 3
    s.term  = 4

  @combinational
  def comb( s ):

    # self coordinates

    #s.x_self.value = s.router_id & s.dim_mask
    #s.y_self.value = s.router_id >> s.dim_nbits

    # self coordinates

    s.x_dest.value = s.dest.value.uint % s.num_routers_1D
    s.y_dest.value = s.dest.value.uint / s.num_routers_1D

    # north, east, south & west dist calculations

    if ( s.y_dest.value < s.y_self.value ):
      s.dist_north.value = s.y_self.value - s.y_dest.value
    else:
      s.dist_north.value = \
        s.y_self.value + 1 + ~s.y_dest.value

    if ( s.y_dest.value > s.y_self.value ):
      s.dist_south.value = s.y_dest.value - s.y_self.value
    else:
      s.dist_south.value = \
        s.y_dest.value + 1 + ~s.y_self.value

    if ( s.x_dest.value < s.x_self.value ):
      s.dist_west.value = s.x_self.value - s.x_dest.value
    else:
      s.dist_west.value = \
        s.x_self.value + 1 + ~s.x_dest.value

    if ( s.x_dest.value > s.x_self.value ):
      s.dist_east.value = s.x_dest.value - s.x_self.value
    else:
      s.dist_east.value = \
        s.x_dest.value + 1 + ~s.x_self.value

    # route calculations

    if   (    ( s.x_dest.value == s.x_self.value )
          and ( s.y_dest.value == s.y_self.value ) ):
      s.route.value = s.term
    elif ( s.x_dest.value != s.x_self.value ):
      if ( s.dist_west.value < s.dist_east.value ):
        s.route.value = s.west
      else:
        s.route.value = s.east
    else:
      if ( s.dist_south.value < s. dist_north.value ):
        s.route.value = s.south
      else:
        s.route.value = s.north
