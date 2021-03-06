#######################################################################################
###### Driver for the TDS540 series of scopes, made to follow the forthcoming #########
###### Generic GPIB python library in development			      #########
###### 									      #########
###### Author:Andrey Shmakov						      #########
###### Email: ashmakov@berkeley.edu					      #########
#######################################################################################


# import the generic gpib driver from the "base" package
from ..base import gpib_base as lldriver
from struct import unpack


#######################List of known commnads for this device#########################

#-----Waveform extract commands---
WAVEFORM_READ='curve?'		# |
#---------------------------------


#-----Acquisition mode commands -------------------------------------
SET_ACQUIRE_MODE='acquire:mode ' #generic			   # |
								   # |
QUERY_ACQUIRE_MODE='acquire:mode?'				   # |
								   # |
SET_ACQUIRE_MODE_SAMPLE='acquire:mode sample' #set mode to sample  # |
SET_ACQUIRE_MODE_HIRES='acquire:mode hires' #set mode to hires     # |
SET_ACQUIRE_MODE_AVERAGE='acquire:mode average'			   # |
SET_ACQUIRE_MODE_PEAKDETECT='acquire:mode peakdetect' 		   # |
SET_ACQUIRE_MODE_ENVELOPE='acquire:mode envelope'		   # |
								   # |
ACQUIRE_MODE_SAMPLE='SAM\n'						   # |
ACQUIRE_MODE_HIRES='HIR\n'						   # |
ACQUIRE_MODE_AVERAGE='AVE\n'						   # |
ACQUIRE_MODE_PEAKDETECT='PEAK\n'					   # |
ACQUIRE_MODE_ENVELOPE='ENVE\n'					   # |
#--------------------------------------------------------------------


#-----Channel Source commands------
SET_DATA_SOURCE='data:source '   # |
				 # |
QUERY_DATA_SOURCE='data:source?' # |
				 # |
DATA_SOURCE_CH1='CH1,'			 # |
DATA_SOURCE_CH2='CH2,'			 # |
DATA_SOURCE_CH3='CH3,'			 # |
DATA_SOURCE_CH4='CH4,'			 # |
				 # |
DATA_SOURCE_MATH1='MATH1,'		 # |
DATA_SOURCE_MATH2='MATH2,'		 # |
DATA_SOURCE_MATH3='MATH3,'		 # |
				 # |
DATA_SOURCE_REF1='REF1,'		 # |
DATA_SOURCE_REF2='REF2,'		 # |
DATA_SOURCE_REF3='REF3,'		 # |
DATA_SOURCE_REF4='REF4,'		 # |
#----------------------------------

#------Data Encoding command----------------
SET_DATA_ENCODING='data:encdg '		 #  |
SET_DATA_ENCODING_ASCII='data:encdg ascii'# |
SET_DATA_ENCODING_BINARY='data:encdg ribinary'#|
					 #  |
QUERY_DATA_ENCODING='data:encdg?'	 #  |

					 #  |
DATA_ENCODING_ASCII='ASCI\n'		 #  |
DATA_ENCODING_RIB='RIB\n'		 #  |
DATA_ENCODING_RPB='RPB\n'		 #  |
DATA_ENCODING_SRI='SRI\n'		 #  |
DATA_ENCODING_SRP='SRP\n'            #  |
DATA_ENCODING_BINARY = DATA_ENCODING_RIB

					 #  |
SET_DATA_START='data:start '		 #  |
SET_DATA_STOP='data:stop '		 #  |
QUERY_DATA_START='data:start?'
QUERY_DATA_STOP='data:stop?'


					 #  |
SET_DATA_WIDTH='data:width '		 #  |
SET_DATA_WIDTH_8BIT='data:width 1'       #  |
SET_DATA_WIDTH_16BIT='data:width 2'      #  |

DATA_WIDTH_8BIT = '1\n'					 #  |
DATA_WIDTH_16BIT= '2\n'

#-------------------------------------------

#----------Trigger commands--------------------------------------
SET_TRIGGER_SOURCE='trigger:main:edge:source '

QUERY_TRIGGER_SOURCE='trigger:main:edge:source?'

SET_TRIGGER_SOURCE_CH1='trigger:main:edge:source ch1'
SET_TRIGGER_SOURCE_CH2='trigger:main:edge:source ch2'
SET_TRIGGER_SOURCE_CH3='trigger:main:edge:source ch3'
SET_TRIGGER_SOURCE_CH4='trigger:main:edge:source ch4'
SET_TRIGGER_SOURCE_LINE='trigger:main:edge:source line'
SET_TRIGGER_SOURCE_AUX='trigger:main:edge:source auxiliary'

TRIGGER_SOURCE_CH1='CH1\n'
TRIGGER_SOURCE_CH2='CH2\n'
TRIGGER_SOURCE_CH3='CH3\n'
TRIGGER_SOURCE_CH4='CH4\n'
TRIGGER_SOURCE_LINE='LINE\n'
TRIGGER_SOURCE_AUX='AUX\n'

SET_TRIGGER_LEVEL='trigger:main:level '
QUERY_TRIGGER_LEVEL='trigger:main:level?'			


SET_TRIGGER_TYPE='trigger:main:type '
QUERY_TRIGGER_TYPE='trigger:main:type?'

SET_TRIGGER_TYPE_EDGE='trigger:main:type edge'
SET_TRIGGER_TYPE_LOGIC='trigger:main:type logic'
SET_TRIGGER_TYPE_PULSE='trigger:main:type pulse'
SET_TRIGGER_TYPE_COMM='trigger:main:type communication'
SET_TRIGGER_TYPE_VIDEO='trigger:main:type video'

TRIGGER_TYPE_EDGE='EDGE\n'
TRIGGER_TYPE_LOGIC='LOGI\n'
TRIGGER_TYPE_PULSE='PUL\n'
TRIGGER_TYPE_COMM='COMM\n'
TRIGGER_TYPE_VIDEO='VID\n'

#----------------------------------------------------------------


#--------Horizontal scale commands------------------------
SET_HORIZONTAL_POSITION='horizontal:position '
QUERY_HORIZONTAL_POSITION='horizontal:position?' 

SET_HORIZONTAL_SCALE='horizontal:main:scale '
QUERY_HORIZONTAL_SCALE='horizontal:main:scale?'

SET_HORIZONTAL_RECORDLENGTH = 'horizontal:recordlength '
QUERY_HORIZONTAL_RECORDLENGTH = 'horizontal:recordlength?'
#---------------------------------------------------------

#--------------------Acquisition amount commands----------
SET_HORIZONTAL_RECORDLENGTH='horizontal:recordlength '
QUERY_HORIZONTAL_RECORDLENGTH='horizontal:recordlength?'
#---------------------------------------------------------


#--------Vertical scale
SET_VERTICAL_SCALE=':scale '
QUERY_VERTICAL_SCALE=':scale?'

VERTICAL_CH1='CH1'
VERTICAL_CH2='CH2'
VERTICAL_CH3='CH3'
VERTICAL_CH4='CH4'

#-------Vertical Position
SET_VERTICAL_POSITION=':position '
QUERY_VERTICAL_POSITION=':position?'


QUERY_WAVEFORM_PREAMBLE='wfmpre:'


##Misc Constants related to GPIB queries
BINARY_DATA_END_INDICATOR = '\n' # just newline
BINARY_DATA_MORE_INDICATOR = ',' #a comma
BINARY_DATA_WAVEFORM_START = '#' 

ASCII_DATA_END_INDICATOR = '\n' #just another newline

## Various python constants that come in handy
STRUCT_SIGNED_BYTE = 'b'
STRUCT_SIGNED_SHORT = 'h'

STRUCT_BIG_ENDIAN = '>'
##


class TDS540_Base:
    channels_vertical_scale = { VERTICAL_CH1 : '0', VERTICAL_CH2 : '0',
                                VERTICAL_CH3 : '0', VERTICAL_CH4 : '0'}

    channels_vertical_position = {VERTICAL_CH1 : '0', VERTICAL_CH2 : '0',
                                  VERTICAL_CH3 : '0', VERTICAL_CH4 : '0'}
    def __init__(self, name):
        """
        Initialize the TDS540 Scope

        Physical (on scope) controls have precedence over driver set controls
        Intitialization modifies no settings on the scope an instead syncs the driver
        with the settings on the scope
        """
        self.driver=lldriver.GpibDevice(name)    #initialize a generic GPIB device
        
        self.data_mode = self.queryDataMode()
        self.acquire_mode = self.queryAcquireMode()
        self.data_width = self.queryDataWidth()
        self.horizontal_scale = self.queryHorizontalScale()
        self.record_length = self.queryRecordLength()
        self.num_of_data_points = self.queryReadLength()
        self.start_point, self.stop_point = self.queryReadStartStopPoints()
        self.data_source = self.queryReadChannels()
        self.verifyAllVerticalScales()
        self.verifyAllVerticalPositions()
        self.horizontal_position = self.queryHorizontalPosition()
        self.trigger_channel = self.queryTriggerChannel()
        self.trigger_level = self.queryTriggerLevel()
        self.trigger_type = self.queryTriggerType()
        """
        self.data_mode = DATA_ENCODING_RIB #set the data to ascii
        self.driver.write(SET_DATA_ENCODING + self.data_mode) #inform the scope
        
        self.data_source = DATA_SOURCE_CH3 # select the channel to read from
        self.number_of_channels = 1
        self.driver.write(SET_DATA_SOURCE + self.data_source) #inform the scope
        
        self.acquire_mode = ACQUIRE_MODE_SAMPLE
        self.driver.write(SET_ACQUIRE_MODE + self.acquire_mode)
        
        self.data_width = DATA_WIDTH_8BIT
        self.driver.write(SET_DATA_WIDTH + self.data_width)

        self.driver.write(QUERY_HORIZONTAL_RECORDLENGTH)
        self.acquire_points = self.driver.read(100) # obtain the number of
               #points the scope is sending

        #snap the data size to the whole waveform
        self.start_point = '0\n'
        self.stop_point=self.acquire_points
        self.num_of_data_points = int(self.stop_point) - int(self.start_point)
        self.driver.write(SET_DATA_START + self.start_point)
        self.driver.write(SET_DATA_STOP + self.stop_point)
        """
        
    def verifyAllFields(self):
        self.verifyDataMode()
        self.verifyAcquireMode()
        self.verifyDataWidth()
        self.verifyHorizontalScale()
        self.verifyRecordLength()
        self.verifyReadLength()
        self.verifyReadChannels()
        self.verifyAllVerticalScales()
        self.verifyAllVerticalPositions()
        self.verifyHorizontalPosition()
        self.verifyTriggerChannel()
        self.verifyTriggerLevel()
        self.verifyTriggerType()

    def readWaveform(self):
        """
        Probably the command that will be used the most
        Query the scope to send the waveform and
        invoke the proper method (readAscii or readBinary) in order to
        interpret the data the correct way.
        """
         #self.driver.write(WAVEFORM_READ)
        if data_mode == DATA_ENCODING_ASCII:
            return self.readAsciiWaveformData()
        elif data_mode == DATA_ENCODING_RIB:
            return self.readBinaryData()
        else:
            return
    
    def readAsciiWaveformData(self):
        """Reads whatever is in the scope buffer as a string
        and returns it as such, not a really great way to extract data
        but can be useful for diagnosing problems or quickly looking
        at numerical data
        """
        if self.data_mode != DATA_ENCODING_ASCII:
            self.driver.write(SET_DATA_ENCODING_ASCII)
            self.data_mode = DATA_ENCODING_ASCII
        self.driver.write(WAVEFORM_READ)
        ret_string=''
        while True:
            ret_string=ret_string+self.driver.read(1000)
            if (ret_string[-1]==ASCII_DATA_END_INDICATOR):
                break
        return ret_string

    def readBinaryWaveformData(self):
        """This method sets the read mode to Binary (read from the scope as signed bigendian bytes)
           and then reads the waveform data from the scope and returns
           a list of tuples, wich each tuple representing the data of one channel/source
           """
        if self.data_mode != DATA_ENCODING_RIB:
            self.driver.write(SET_DATA_ENCODING_BINARY)
            self.data_mode = DATA_ENCODING_RIB

        count = 0
        results_list = list()
        self.verifyDataWidth()
        pattern_char = STRUCT_SIGNED_BYTE # default pattern to read all bytes seperately
        if self.data_width == DATA_WIDTH_16BIT:
            pattern_char = STRUCT_SIGNED_SHORT
        self.driver.write(WAVEFORM_READ)
        while True:
            """
            Pattern for binary waveform data = '#y<xxx><data>'  where y is the number
            of chars for <xxx> and <xxx> is the number of bytes in <data>
            """
            beginning_char = self.driver.readBinary(1)
            print beginning_char
            if beginning_char != BINARY_DATA_WAVEFORM_START:
                print "WAVEFORM OUT OF SYNC, DO NOT TRUST THIS DATA"
                #make an error - out of synch message
            
            y_length = int(self.driver.readBinary(1))
            num_of_bytes = int(self.driver.readBinary(y_length))
            print y_length
            print num_of_bytes
            points = self.driver.readBinary(num_of_bytes)

            pattern_length = num_of_bytes/int(self.data_width)
            
            print pattern_length
            print pattern_char
            pattern = STRUCT_BIG_ENDIAN + pattern_char*pattern_length
            
            results_list.append(unpack(pattern, points))

            end_byte = (self.driver.readBinary(1))
            print end_byte
            if end_byte == BINARY_DATA_END_INDICATOR:
                break
            elif end_byte == BINARY_DATA_MORE_INDICATOR:
                continue
            else :
                print "WAVEFORM OUT OF SYNC DO NOT TRUST THIS DATA"
                print "BAD INDICATOR BYTE = " + str(end_byte)
            count = count +1
        
        #check to make sure the number of channels matches
        #if self.number_of_channels != count:
        #    print "NUMBER OF CHANNELS READ DOES NOT MATCH NUMBER OF CHANNELS EXPECTED"
        return results_list

    """
    The following methods are used to set the data send mode on the cope
    The intent is that only the specific setDataModeZZZ methods are used
    """
    def setDataMode(self,mode):
        self.data_mode = mode
        self.driver.write(SET_DATA_ENCODING + mode)
        return self.verifyDataMode()
    
    def setDataModeAscii(self):
        return self.setDataMode(DATA_ENCODING_ASCII)

    def setDataModeBinary(self):
        return self.setDataMode(DATA_ENCODING_BINARY)

    def queryDataMode(self):
        self.driver.write(QUERY_DATA_ENCODING)
        return self.driver.read(10)

    def verifyDataMode(self):
        """
        Verifies that the scope is set to the same data mode that this driver is set to
        if not, it updates the driver to match the scope settings
        , physical controls have higher precedence than driver set
        controls. A false result means that the driver had to be synced
        """
        real_data_mode = self.queryDataMode()
        if real_data_mode  == self.data_mode:
            return True
        self.data_mode = real_data_mode
        return False
        
    
    """
    The following methods are used to set the acquire mode on the scope
    The intent is that only the specific setAcquireModeZZZ methods are used.
    """
    def setAcquireMode(self,mode):
        """
        This method is used to set the acquire mode
        Unless you know a secret acquire mode that this 
        driver doesnt implement, this method should only
        be invoked indirectly through the setAcquireModeZZZ methods
        """
        self.acquire_mode=mode
        self.driver.write(SET_ACQUIRE_MODE + mode)
        return self.verifyAcquireMode() # make sure that the scope accepted our request
    
    def setAcquireModeSample(self):
        """Set the acquire mode to sample"""
        return self.setAcquireMode(ACQUIRE_MODE_SAMPLE)
    
    def setAcquireModeHires(self):
        """Set the acquire mode to hires"""
        return self.setAcquireMode(ACQUIRE_MODE_HIRES)
    
    def setAcquireModeAverage(self):
        """Set the acquire mode to average"""
        return self.setAcquireMode(ACQUIRE_MODE_AVERAGE)
    
    def setAcquireModeEnvelope(self):
        """Set the acquire mode to envelope"""
        return self.setAcquireMode(ACQUIRE_MODE_ENVELOPE)
    
    def setAcquireModePeakdetect(self):
        """Set the acquire mode to peakdetect"""
        return self.setAcquireMode(ACQUIRE_MODE_PEAKDETECT)
        
    def queryAcquireMode(self):
        """
        Get the value of the acquire mode from the scope
        """
        self.driver.write(QUERY_ACQUIRE_MODE)
        return self.driver.read(10)

    def verifyAcquireMode(self):

        """
        Verifies that the scope is set to the same mode that this driver is set to
        if not, it updates the driver to match the scope settings
        , physical controls have higher precedence than driver set
        controls. A false result means that the driver had to be synced
        """
        real_acquire_mode = self.queryAcquireMode()
        if real_acquire_mode == self.acquire_mode:
            return True
        self.acquire_mode = real_acquire_mode
        return False
         

    """
    The following methods relate to setting the width of the point data
    The intent is that only the specific setDataWidthZZZ methods are used.
    """
    def setDataWidth(self, width):
        """
        This method is used to set the data width
        Unless you have a good reason to use this method
        directly, it is intended to be invoked indirectly through
        the setDataWidthZZZ methods.
        """
        self.data_width = width
        self.driver.write(SET_DATA_WIDTH + width)
        return self.verifyDataWidth()
    
    def setDataWidth8Bit(self):
        return self.setDataWidth(DATA_WIDTH_8BIT)
    
    def setDataWidth16Bit(self):
        return self.setDataWidth(DATA_WIDTH_16BIT)

    def queryDataWidth(self):
        self.driver.write('data:width?')
        return self.driver.read(10)
    
    def verifyDataWidth(self):
        """
        Verifies that the scope is set to the same data width that this driver is set to
        if not, it updates the driver to match the scope settings
        , physical controls have higher precedence than driver set
        controls. A false result means that the driver had to be synced
        """
        real_datawidth = self.queryDataWidth()
        if real_datawidth == self.data_width:
            return True
        self.data_width = real_datawidth
        return False
    

    """
    The Following Methods are used to set the horizontal scale commands
    """

    def setHorizontalScale(self, scale):
        """
        Set the horizontal scale, verifies that the scope accepted the scale.
        Returns false if the scope snapped to a different value then the one 
        asked for
        """
        self.horizontal_scale = scale+'\n'
        self.driver.write(SET_HORIZONTAL_SCALE + scale)
        return self.verifyHorizontalScale()
    
    def queryHorizontalScale(self):
        self.driver.write(QUERY_HORIZONTAL_SCALE)
        return self.driver.read(15)
    
    def verifyHorizontalScale(self):
        """
        Verifies that the scope is set to the same horizontal that this driver is set to
        if not, it updates the driver to match the scope settings
        , physical controls have higher precedence than driver set
        controls. A false result means that the driver had to be synced
        """
        real_horiz_scale = self.queryHorizontalScale()
        if real_horiz_scale == self.horizontal_scale:
            return True
        self.horizontal_scale = real_horiz_scale
        return False

    
    """
    The Following methods are used to set the horizontal acquire length
    """

    def setRecordLength(self,length) :
        self.record_length = str(length) + '\n'
        self.driver.write(SET_HORIZONTAL_RECORDLENGTH + str(length))
        return self.verifyRecordLength()
    
    def queryRecordLength(self) : 
        self.driver.write(QUERY_HORIZONTAL_RECORDLENGTH)
        return self.driver.read(15)

    def verifyRecordLength(self) :
        real_record_length = self.queryRecordLength()
        if real_record_length == self.record_length:
            return True
        self.record_length = real_record_length
        return False

    """
    The Following methods are used to set the data read length
    """
        
    def setReadLength(self, length):
        return self.setReadLengthPoints(1, int(length) )

    def setReadLengthPoints(self, start, stop):
        self.start_point = str(start) + '\n'
        self.stop_point = str(stop) + '\n'
        self.num_of_data_points = int(stop) - int(start) + 1 # +1 because the scope sends x->y inclusive
        self.driver.write(SET_DATA_START + self.start_point)
        self.driver.write(SET_DATA_STOP + self.stop_point)
        return self.verifyReadLength()
    
    def queryReadStartStopPoints(self):
        self.driver.write(QUERY_DATA_START)
        tmpstart = self.driver.read(20)
        self.driver.write(QUERY_DATA_STOP)
        tmpstop = self.driver.read(30)
        return tmpstart,tmpstop
    
    def queryReadLength(self):
        st,sp = self.queryReadStartStopPoints()
        len = int(sp) - int(st) + 1 # since it read x-y inclusive 
        return len
    
    def verifyReadLength(self):
        """
        Verifies that the scope is set to the same source read length that this driver is set to
        if not, it updates the driver to match the scope settings
        , physical controls have higher precedence than driver set
        controls. A false result means that the driver had to be synced
        """
        st,sp = self.queryReadStartStopPoints()
        len = self.queryReadLength()
        if st == self.start_point and sp == self.stop_point and int(len) == self.num_of_data_points:
            return True
        self.start_point = st
        self.stop_point = sp
        self.num_of_data_points = int(len)
        return False

    """
    The following methods are used to set the channels that will be read
    """

    def setReadChannels(self, channels):
        channel_arg = ''
        for i in range(len(channels)):
            channel_arg = channel_arg + channels[i]
        
        if channel_arg[-1] == ',': # as it should be
            channel_arg = channel_arg[:-1]
        channel_arg = channel_arg+'\n'
        self.data_source = channel_arg
        self.driver.write(SET_DATA_SOURCE + self.data_source)
        return self.verifyReadChannels()

    def queryReadChannels(self):
        self.driver.write(QUERY_DATA_SOURCE)
        return self.driver.read(50)
    
    def verifyReadChannels(self):
        """
        Verifies that the scope is set to read from the same channels that this driver is set to
        if not, it updates the driver to match the scope settings
        , physical controls have higher precedence than driver set
        controls. A false result means that the driver had to be synced
        """
        real_channels = self.queryReadChannels()
        if real_channels == self.data_source:
            return True
        self.data_source = real_channels
        return False


    """
    The following methods are used to set the vertical scale

    """
    
    def setVerticalScale(self,channel,scale):
        """
        The lowlevel set vertical scale command
        The intent is to use the specific setZZZVerticalScale method,
        where ZZZ is the channel to be set
        """
        self.driver.write(channel + SET_VERTICAL_SCALE + scale)
        self.channels_vertical_scale[channel] = scale + '\n'
        return self.verifyVerticalScale(channel)
    
    def setCH1VerticalScale(self,scale):
        return self.setVerticalScale(VERTICAL_CH1,scale)
    
    def setCH2VerticalScale(self,scale):
        return self.setVerticalScale(VERTICAL_CH2,scale)
    
    def setCH3VerticalScale(self,scale):
        return self.setVerticalScale(VERTICAL_CH3,scale)
    
    def setCH4VerticalScale(self,scale):
        return self.setVerticalScale(VERTICAL_CH4,scale)

    def queryVerticalScale(self,channel):
        self.driver.write(channel + QUERY_VERTICAL_SCALE)
        return self.driver.read(20)

    def verifyVerticalScale(self,channel):
        """
        Verifies that the scope is set to the same vertical scale that this driver is set to
        if not, it updates the driver to match the scope settings
        , physical controls have higher precedence than driver set
        controls. A false result means that the driver had to be synced
        """
        real_vertical_scale = self.queryVerticalScale(channel)
        if real_vertical_scale == self.channels_vertical_scale[channel]:
            return True
        
        self.channels_vertical_scale[channel] = real_vertical_scale        
        return False
    def verifyAllVerticalScales(self):
        ch1 = self.verifyVerticalScale(VERTICAL_CH1) # This is done because if you just place
        ch2 = self.verifyVerticalScale(VERTICAL_CH2) # these statements in an and statement
        ch3 = self.verifyVerticalScale(VERTICAL_CH3) # then python will stop at the first 
        ch4 = self.verifyVerticalScale(VERTICAL_CH4) # false statement, but we want to update
                                                     # all the channels and then return T/F   

        return (ch1 and ch2 and ch3 and ch4)
        

    """
    The following methods set the Horizontal position
    """
    
    def setHorizontalPosition(self,position):
        self.horizontal_position = str(position)
        self.driver.write(SET_HORIZONTAL_POSITION + position + '\n')
        
        return self.verifyHorizontalPosition()

    def queryHorizontalPosition(self):
        self.driver.write(QUERY_HORIZONTAL_POSITION)
        return self.driver.read(20)
    
    def verifyHorizontalPosition(self):
        """
        Verifies that the scope is set to the same horizontal pos that this driver is set to
        if not, it updates the driver to match the scope settings
        , physical controls have higher precedence than driver set
        controls. A false result means that the driver had to be synced
        """
        real_position = self.queryHorizontalPosition()
        if real_position == self.horizontal_position:
            return True
        self.horizontal_position = real_position
        return False


    """
    The following methods set the vertical position of each channel
    """
    def setVerticalPosition(self,channel,position):
        channels_vertical_position[channel] = position + '\n'
        self.driver.write(channel + SET_VERTICAL_POSITION + position)
        return self.verifyVerticalPosition(channel)

    def setCH1VerticalPosition(self,position):
        return self.setVerticalPosition(VERTICAL_CH1,position)
    
    def setCH2VerticalPosition(self,position):
        return self.setVerticalPosition(VERTICAL_CH2,position)

    def setCH3VerticalPosition(self,position):
        return self.setVerticalPosition(VERTICAL_CH3,position)

    def setCH4VerticalPosition(self,position):
        return self.setVerticalPosition(VERTICAL_CH4,position)

    def queryVerticalPosition(self,channel):
        self.driver.write(channel + QUERY_VERTICAL_POSITION)
        return self.driver.read(20)

    def verifyVerticalPosition(self,channel):
        """
        Verifies that the scope is set to the same Vertical pos that this driver is set to
        if not, it updates the driver to match the scope settings
        , physical controls have higher precedence than driver set
        controls. A false result means that the driver had to be synced
        """
        real_vert_position = self.queryVerticalPosition(channel)
        if real_vert_position == self.channels_vertical_position[channel]:
            return True
        self.channels_vertical_position[channel] = real_vert_position
        return False

    def verifyAllVerticalPositions(self):
        ch1 = self.verifyVerticalPosition(VERTICAL_CH1) # This is done because if you just place
        ch2 = self.verifyVerticalPosition(VERTICAL_CH2) # these statements in an and statement
        ch3 = self.verifyVerticalPosition(VERTICAL_CH3) # then python will stop at the first 
        ch4 = self.verifyVerticalPosition(VERTICAL_CH4) # false statement, but we want to update
                                                     # all the channels and then return T/F   

        
        return (ch1 and ch2 and ch3 and ch4)

        
    """
    The following methods set the trigger channel on the scope
    """

    def setTriggerChannel(self,channel):
        self.trigger_channel = channel
        if self.trigger_channel[-1] != '\n':
            self.trigger_channel = self.trigger_channel + '\n'
        self.driver.write(SET_TRIGGER_SOURCE + channel)
        return self.verifyTriggerChannel()

    def setTriggerToChannel1(self):
        return self.setTriggerChannel(TRIGGER_SOURCE_CH1)

    def setTriggerToChannel2(self):
        return self.setTriggerChannel(TRIGGER_SOURCE_CH2)
    
    def setTriggerToChannel3(self):
        return self.setTriggerChannel(TRIGGER_SOURCE_CH3)
    
    def setTriggerToChannel4(self):
        return self.setTriggerChannel(TRIGGER_SOURCE_CH4)

    def setTriggerToAux(self):
        return self.setTriggerChannel(TRIGGER_SOURCE_AUX)
   
    def setTriggerToLine(self):
        return self.setTriggerChannel(TRIGGER_SOURCE_LINE)

    def queryTriggerChannel(self):
        self.driver.write(QUERY_TRIGGER_SOURCE)
        return self.driver.read(30)

    def verifyTriggerChannel(self):
        """
        Verifies that the scope is set to the same trigger channel that this driver is set to
        if not, it updates the driver to match the scope settings
        , physical controls have higher precedence than driver set
        controls. A false result means that the driver had to be synced
        """
        real_trigger_channel = self.queryTriggerChannel()
        if real_trigger_channel == self.trigger_channel:
            return True
        self.trigger_channel = real_trigger_channel
        return False
    


    
    """ 
    The Following Methods set the trigger level on the scope
    """
    
    def setTriggerLevel(self,level):
        self.trigger_level = level
        if self.trigger_level[-1] != '\n':
            self.trigger_level = self.trigger_level + '\n'
        self.driver.write(SET_TRIGGER_LEVEL + level)
        return self.verifyTriggerLevel()

    def queryTriggerLevel(self):
        self.driver.write(QUERY_TRIGGER_LEVEL)
        return self.driver.read(15)

    def verifyTriggerLevel(self):
        """
        Verifies that the scope is set to the same trigger level that this driver is set to
        if not, it updates the driver to match the scope settings
        , physical controls have higher precedence than driver set
        controls. A false result means that the driver had to be synced
        """
        real_trigger_level = self.queryTriggerLevel()
        if real_trigger_level == self.trigger_level:
            return True
        self.trigger_level = real_trigger_level
        return False


    """
    The Following Methods set the trigger type on the scope
    """

    def setTriggerType(self,type):
        self.trigger_type = type
        if self.trigger_type[-1] != '\n':
            self.trigger_type = self.trigger_type + '\n'
        self.driver.write(SET_TRIGGER_TYPE + type)
        return self.verifyTriggerType()

    def setTriggerTypeEdge(self):
        return self.setTriggerType(TRIGGER_TYPE_EDGE)

    def setTriggerTypeLogic(self):
        return self.setTriggerType(TRIGGER_TYPE_LOGIC)

    def setTriggerTypePulse(self):
        return self.setTriggerType(TRIGGER_TYPE_PULSE)

    def setTriggerTypeComm(self):
        return self.setTriggerType(TRIGGER_TYPE_COMM)

    def setTriggerTypeVideo(self):
        return self.setTriggerType(TRIGGER_TYPE_VIDEO)

    def queryTriggerType(self):
        self.driver.write(QUERY_TRIGGER_TYPE)
        return self.driver.read(20)

    def verifyTriggerType(self):
        """
        Verifies that the scope is set to the same trigger type that this driver is set to
        if not, it updates the driver to match the scope settings
        , physical controls have higher precedence than driver set
        controls. A false result means that the driver had to be synced
        """
        real_trigger_type = self.queryTriggerType()
        if real_trigger_type == self.trigger_type:
            return True
        self.trigger_type = real_trigger_type
        return False


    def queryWaveformPreamble(self, channel):
        self.driver.write(QUERY_WAVEFORM_PREAMBLE + channel + '?')
        return self.driver.read(200)


    
