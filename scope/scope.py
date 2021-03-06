#######################################################################################
###### This file defines the scope interface, for the forthcoming             #########
###### Generic GPIB python library in development			      #########
###### 									      #########
###### Author:Andrey Shmakov						      #########
###### Email: ashmakov@berkeley.edu					      #########
#######################################################################################

from ..base.interface import *

class Scope:
    
    def setReadChannels(self, *args):
        """
        Implementations of this method should be open to any reasonable argument types

        i.e. setReadChannels('CH1,CH2,CH3') , setReadChannels('1,MATH1,3') , setReadChannels(1,2,3),
        setReadChannels('CH1','CH2','CH3','MATH1'), setReadChannels([1,2,3]), etc.
        
        must all result in proper setting of the channels
        """
        abstractMethod(self)

    def setTriggerChannel(self, *args):
        """
        Implementations of this method should be open to any reasonable argument types

        i.e. setTriggerChannel('CH1') , setReadChannels('1') , setReadChannels(1), etc.
        
        must all result in proper setting of the channel 
        """
        abstractMethod(self)

    def setTriggerLevel(self, *args):
        """
        Implementations of this method should be open to any reasonable argument types

        i.e. setTriggerLevel(.006) , setReadChannels('10E-3') , setReadChannels('5mv'), etc.
        
        must all result in proper setting of the trigger level 
        """
        abstractMethod(self)

    def setVerticalScale(self, *args):
        """
        Implementations of this method should be open to any reasonable argument types

        i.e. setVerticalScale('CH1 5mv') , setVerticalScale('CH1', '4E-3') , setVerticalScale('CH1', .006), etc.
        
        must all result in proper setting of the channel level 
        """

        abstractMethod(self)

    def setHorizontalScale(self, *args):
        """
        Implementations of this method should be open to any reasonable argument types

        i.e. setHorizontalScale(.05) , setHorizontalScale('5E-6') , setHorizontalScale('5mv'), etc.
        
        must all result in proper setting of the channel 
        """

        abstractMethod(self)

    def setVerticalLevel(self, *args):
        """
        Implementations of this method should be open to any reasonable argument types

        i.e. setVerticalLevel('CH1:500') , setVerticalLevel(1,5mv) , setVerticalLevel(), etc.
        
        must all result in proper setting of the channel 
        """

        abstractMethod(self)
    
    def setAcquireMode(self, *args):
        """
        Implementations of this method should be open to any reasonable argument types

        i.e. setAcquireMode('hires') , setVerticalLevel('average'), etc.
        
        must all result in proper setting of the read length
        """
        abstractMethod(self)
    
    def setReadLength(self, *args):
        """
        Implementations of this method should be open to any reasonable argument types

        i.e. setReadLength(500) , setVerticalLevel('500') etc.
        
        must all result in proper setting of the ReadLength
        """

        abstractMethod(self)
    
    
