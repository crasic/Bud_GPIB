
##########################################################################################
###Basic Python does not have interfaces (completely abstract classes)                 ###
###mainly because it conflicts somewhat with its weakly-typed structure                ###
###as such, we have to jerry-rig an interface. To imitate abstract methods             ###
###we make methods that throw "unimplemented abstract method" exceptions when called   ###
###which should only happen when a deriving class does not implement all the methods   ###
###in this interface                                                                   ###
###                                                                                    ###
###This library seeks to use as little external packages as possible, even though      ###
###there are robust interface implementations in several python extensions,            ###
###the need of strict typing with more "proffesional" interfaces is not deemed         ###
###necessary                                                                           ###
###                                                                                    ###
###The Credit for the abstract methods goes to                                         ###
###Ned Batchelder from  nedbatchelder.com                                              ###
##########################################################################################



import sys

def _functionId(obj, nFramesUp):
    """ Create a string naming the function n frames up on the stak."""
    fr = sys.__getframe(nFramesUp+1)
    co = fr.f_code
    return "%s.%s" % (obj.__class__,co.co_name)

def abstractMethod(obj=None):
    """Use this to make a method abstract, it will throw an exception if 
    the method isnt implemented in a deriving class"""
    raise Exception("Unimplemented abstract method: %s" % _functionId(obj,1))
