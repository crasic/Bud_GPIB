from ..base import gpib_base as lldriver


##List of known commnads for this device

WAVEFORM_READ='curve?'

##


class TDS540_Base:
    def __init__(self, name):
        self.driver=lldriver.GpibDevice(name)
    def readWaveform(self):
        self.driver.write(WAVEFORM_READ)
        return self.driver.read(5000)


        
