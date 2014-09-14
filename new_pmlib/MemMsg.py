#=========================================================================
# NetMsg
#=========================================================================
# TODO DESCRIPTION

from new_pymtl import *

import math

#-------------------------------------------------------------------------
# MemReqMsg
#-------------------------------------------------------------------------
# BitStruct designed to create memory request messages.
class MemReqMsg( BitStructDefinition ):

  def __init__( s, addr_nbits, data_nbits):

    s.type_nbits = 1
    s.addr_nbits = addr_nbits
    s.len_nbits  = int( math.ceil( math.log( data_nbits/8, 2) ) )
    s.data_nbits = data_nbits

    s.type = BitField( s.type_nbits )
    s.addr = BitField( s.addr_nbits )
    s.len  = BitField( s.len_nbits  )
    s.data = BitField( s.data_nbits )

  def mk_msg( s, type_, addr, len_, data):

    msg      = s()
    msg.type = type_
    msg.addr = addr
    msg.len  = len_
    msg.data = data

    return msg


#-------------------------------------------------------------------------
# MemReqMsg
#-------------------------------------------------------------------------
# BitStruct designed to create memory response messages.
class MemRespMsg ( BitStructDefinition ):

  def __init__( s, data_nbits):

    s.type_nbits = 1
    s.len_nbits  = int( math.ceil( math.log( data_nbits/8, 2 ) ) )
    s.data_nbits = data_nbits

    s.type = BitField( s.type_nbits )
    s.len  = BitField( s.len_nbits  )
    s.data = BitField( s.data_nbits )

    #TODO mk_msg
    
  
