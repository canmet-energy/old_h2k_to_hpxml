from h2kparser import h2kparser as H2K
class translateTRNBld:
    def __init__(self,file):
        self.filename = file
        self.file = H2K(file)

    def translateFile(self,sOutput):
        print(f"H2K file is {self.file.getFileID()}")
        print(f"Climate is {self.file.getClimateCity()}")
        print(f"House type is {self.file.getHouseType()}")
        print(f"House plan shape is {self.file.getPlanShape()}")
        print(f"Output file is {sOutput}")
        return 0
        # TODOD
        # pass

##########################################################################################################
#   PRIVATE METHODS
##########################################################################################################