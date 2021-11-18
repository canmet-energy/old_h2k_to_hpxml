# Python class to parse HOT2000 v11 files
import xml.etree.ElementTree as ET
class h2kparser:
    def __init__(self, file):
        self.file = file
        self.mytree = ET.parse(file)
        self.myroot = self.mytree.getroot()
        
        # Initialize class data structures
        self.__setWalls() # Also initializes Doors, Windows, and floor headers lists
        self.__setCeilings()
        self.__setHRVs()
        self.__setWholeHseVnt()
        self.__setSuppVnt()
        self.__setBasements()
        
    def __str__(self):
        return f"H2K file is {self.file}"

##########################################################################################################
#   H2K Model Identification
##########################################################################################################

    def getVersion(self):
        return self.myroot.find("./Application/Version/Labels/English").text

    def getFileID(self):
        return self.myroot.find("./ProgramInformation/File/Identification").text

##########################################################################################################
#   H2K Climate
##########################################################################################################

    def getClimateProvince(self):
        return self.myroot.find("./ProgramInformation/Weather/Region/English").text

    def getClimateCity(self):
        return self.myroot.find("./ProgramInformation/Weather/Location/English").text

    def getDepthOfFrost(self):
        return float(self.myroot.find("./ProgramInformation/Weather").attrib["depthOfFrost"])

    def getHDD(self):
        return int(self.myroot.find("./ProgramInformation/Weather").attrib["heatingDegreeDay"])

##########################################################################################################
#   H2K Specifications
##########################################################################################################

    def getHouseType(self):
        return self.myroot.find("./House/Specifications/HouseType/English").text

    def getHouseTypeCode(self):
        return int(self.myroot.find("./House/Specifications/HouseType").attrib["code"])

    def getPlanShape(self):
        return self.myroot.find("./House/Specifications/PlanShape/English").text

    def getPlanShapeCode(self):
        return int(self.myroot.find("./House/Specifications/PlanShape").attrib["code"])

    def getStoreys(self):
        return self.myroot.find("./House/Specifications/Storeys/English").text

    def getStoreysCode(self):
        return int(self.myroot.find("./House/Specifications/Storeys").attrib["code"])

    def getFacingDir(self):
        return self.myroot.find("./House/Specifications/FacingDirection/English").text

    def getFacingDirCode(self):
        return int(self.myroot.find("./House/Specifications/FacingDirection").attrib["code"])

    def getThermalMass(self):
        return self.myroot.find("./House/Specifications/ThermalMass/English").text

    def getThermalMassCode(self):
        return int(self.myroot.find("./House/Specifications/ThermalMass").attrib["code"])

    def getVintage(self):
        code = self.myroot.find("./House/Specifications/YearBuilt").attrib["code"]
        if int(code) == 2:
            return 1920
        elif int(code) == 3:
            return 1925
        elif int(code) == 4:
            return 1935
        elif int(code) == 5:
            return 1945
        elif int(code) == 6:
            return 1955
        elif int(code) == 7:
            return 1965
        elif int(code) == 8:
            return 1975
        elif int(code) == 9:
            return 1985
        elif int(code) == 10:
            return 1995
        elif int(code) == 11:
            return 2005
        elif int(code) == 1:
            return int(self.myroot.find("./House/Specifications/YearBuilt").attrib["value"])
        else:
            raise SystemExit("Vintage code {} is not valid.".format(code))
    
    def getWallSolAbs(self):
        return float(self.myroot.find("./House/Specifications/WallColour").attrib["value"])

    def getRoofSolAbs(self):
        return float(self.myroot.find("./House/Specifications/RoofColour").attrib["value"])

    def getWaterLevel(self):
        return self.myroot.find("./House/Specifications/WaterLevel/English").text

    def getWaterLevelCode(self):
        return int(self.myroot.find("./House/Specifications/WaterLevel").attrib["code"])

    def getAboveGradeHeatedArea(self):
        return float(self.myroot.find("./House/Specifications/HeatedFloorArea").attrib["aboveGrade"])

    def getBelowGradeHeatedArea(self):
        return float(self.myroot.find("./House/Specifications/HeatedFloorArea").attrib["belowGrade"])

    def getRoofCavityVolume(self):
        return float(self.myroot.find("./House/Specifications/RoofCavity").attrib["volume"])

    def getRoofCavityACH(self):
        return float(self.myroot.find("./House/Specifications/RoofCavity").attrib["ventilationRate"])

    def getGableEndArea(self):
        return float(self.myroot.find("./House/Specifications/RoofCavity/GableEnds").attrib["area"])

    def getGableEndSheathingCode(self):
        return int(self.myroot.find("./House/Specifications/RoofCavity/GableEnds/SheatingMaterial").attrib["code"])

    def getGableEndSheathingRSI(self):
        return float(self.myroot.find("./House/Specifications/RoofCavity/GableEnds/SheatingMaterial").attrib["value"])

    def getGableEndExteriorCode(self):
        return int(self.myroot.find("./House/Specifications/RoofCavity/GableEnds/ExteriorMaterial").attrib["code"])

    def getGableEndExteriorRSI(self):
        return float(self.myroot.find("./House/Specifications/RoofCavity/GableEnds/ExteriorMaterial").attrib["value"])

    def getSlopedRoofArea(self):
        return float(self.myroot.find("./House/Specifications/RoofCavity/SlopedRoof").attrib["area"])

    def getSlopedRoofSheathingCode(self):
        return int(self.myroot.find("./House/Specifications/RoofCavity/SlopedRoof/SheatingMaterial").attrib["code"])

    def getSlopedRoofSheathingRSI(self):
        return float(self.myroot.find("./House/Specifications/RoofCavity/SlopedRoof/SheatingMaterial").attrib["value"])

    def getSlopedRoofExteriorCode(self):
        return int(self.myroot.find("./House/Specifications/RoofCavity/SlopedRoof/ExteriorMaterial").attrib["code"])

    def getSlopedRoofExteriorRSI(self):
        return float(self.myroot.find("./House/Specifications/RoofCavity/SlopedRoof/ExteriorMaterial").attrib["value"])
     
##########################################################################################################
#   H2K Temperatures
##########################################################################################################

    def getDayHeatingSetpoint(self):
        return float(self.myroot.find("./House/Temperatures/MainFloors").attrib["daytimeHeatingSetPoint"])

    def getNightHeatingSetpoint(self):
        return float(self.myroot.find("./House/Temperatures/MainFloors").attrib["nighttimeHeatingSetPoint"])

    def getNightSetbackDur(self):
        return float(self.myroot.find("./House/Temperatures/MainFloors").attrib["nighttimeSetbackDuration"])

    def getCoolingSetpoint(self):
        return float(self.myroot.find("./House/Temperatures/MainFloors").attrib["coolingSetPoint"])

    def getAllowTempRise(self):
        code = self.myroot.find("./House/Temperatures/MainFloors/AllowableRise").attrib["code"]
        if int(code) == 1:
            return 0
        elif int(code) == 2:
            return 2.8
        elif int(code) == 3:
            return 5.5
        else:
            raise SystemExit("ERROR: Allowable rise code {} is not valid.".format(code))

    def getIsBasementHeated(self):
        return self.myroot.find("./House/Temperatures/Basement").attrib["heated"]

    def getIsBasementCooled(self):
        return self.myroot.find("./House/Temperatures/Basement").attrib["cooled"]

    def getIsBasementSepThermo(self):
        return float(self.myroot.find("./House/Temperatures/Basement").attrib["separateThermostat"])

    def getBasementHeatSetpoint(self):
        return float(self.myroot.find("./House/Temperatures/Basement").attrib["heatingSetPoint"])

    def getIsBasementAUnit(self):
        return self.myroot.find("./House/Temperatures/Basement").attrib["basementUnit"]

    def getEquipmentHeatSetpoint(self):
        return float(self.myroot.find("./House/Temperatures/Equipment").attrib["heatingSetPoint"])

    def getEquipmentCoolSetpoint(self):
        return float(self.myroot.find("./House/Temperatures/Equipment").attrib["coolingSetPoint"])

##########################################################################################################
#   H2K Baseloads
##########################################################################################################

    def getIsOccupied(self):
        return self.myroot.find("./House/BaseLoads/Occupancy").attrib["isOccupied"]

    def getNumAdults(self):
        return int(self.myroot.find("./House/BaseLoads/Occupancy/Adults").attrib["occupants"])

    def getFracAdultHome(self):
        return float(self.myroot.find("./House/BaseLoads/Occupancy/Adults").attrib["atHome"])

    def getNumKids(self):
        return int(self.myroot.find("./House/BaseLoads/Occupancy/Children").attrib["occupants"])

    def getFracKidHome(self):
        return float(self.myroot.find("./House/BaseLoads/Occupancy/Children").attrib["atHome"])

    def getNumInfants(self):
        return int(self.myroot.find("./House/BaseLoads/Occupancy/Infants").attrib["occupants"])

    def getFracInfantHome(self):
        return float(self.myroot.find("./House/BaseLoads/Occupancy/Infantss").attrib["atHome"])

    def getElectricalAppLoad(self):
        return float(self.myroot.find("./House/BaseLoads/Summary").attrib["electricalAppliances"])

    def getLightingLoad(self):
        return float(self.myroot.find("./House/BaseLoads/Summary").attrib["lighting"])

    def getOtherElecLoad(self):
        return float(self.myroot.find("./House/BaseLoads/Summary").attrib["otherElectric"])

    def getExtElecLoad(self):
        return float(self.myroot.find("./House/BaseLoads/Summary").attrib["exteriorUse"])

    def getDHWLoad(self):
        return float(self.myroot.find("./House/BaseLoads/Summary").attrib["hotWaterLoad"])

##########################################################################################################
#   H2K Infiltration
##########################################################################################################

    def getHeatedVolume(self):
        return float(self.myroot.find("./House/NaturalAirInfiltration/Specifications/House").attrib["volume"])

    def getIsCrawlVolInc(self):
        return self.myroot.find("./House/NaturalAirInfiltration/Specifications/House").attrib["includeCrawlspaceVolume"]

    def getACH50(self):
        return float(self.myroot.find("./House/NaturalAirInfiltration/Specifications/BlowerTest").attrib["airChangeRate"])

    def getELA10(self):
        return float(self.myroot.find("./House/NaturalAirInfiltration/Specifications/BlowerTest").attrib["leakageArea"])

    def getSiteTerrain(self):
        return self.myroot.find("./House/NaturalAirInfiltration/Specifications/BuildingSite/Terrain/English").text

    def getSiteTerrainCode(self):
        return int(self.myroot.find("./House/NaturalAirInfiltration/Specifications/BuildingSite/Terrain").attrib["code"])

    def getWallShielding(self):
        return self.myroot.find("./House/NaturalAirInfiltration/Specifications/LocalShielding/Walls/English").text

    def getWallShieldingCode(self):
        return int(self.myroot.find("./House/NaturalAirInfiltration/Specifications/LocalShielding/Walls").attrib["code"])

    def getFlueShielding(self):
        return self.myroot.find("./House/NaturalAirInfiltration/Specifications/LocalShielding/Flue/English").text

    def getFlueShieldingCode(self):
        return int(self.myroot.find("./House/NaturalAirInfiltration/Specifications/LocalShielding/Flue").attrib["code"])

##########################################################################################################
#   H2K Ventilation
##########################################################################################################

    def getNumLivingRooms(self):
        return int(self.myroot.find("./House/Ventilation/Rooms").attrib["living"])

    def getNumBedrooms(self):
        return int(self.myroot.find("./House/Ventilation/Rooms").attrib["bedrooms"])

    def getNumBathrooms(self):
        return int(self.myroot.find("./House/Ventilation/Rooms").attrib["bathrooms"])

    def getNumUtilRooms(self):
        return int(self.myroot.find("./House/Ventilation/Rooms").attrib["utility"])

    def getNumOtherRooms(self):
        return int(self.myroot.find("./House/Ventilation/Rooms").attrib["otherHabitable"])

    def getVentDistType(self):
        return self.myroot.find("./House/Ventilation/WholeHouse/AirDistributionType/English").text

    def getVentDistTypeCode(self):
        return int(self.myroot.find("./House/Ventilation/WholeHouse/AirDistributionType").attrib["code"])

    def getVentDistFanPow(self):
        return self.myroot.find("./House/Ventilation/WholeHouse/AirDistributionFanPower/English").text

    def getVentDistFanPowCode(self):
        return int(self.myroot.find("./House/Ventilation/WholeHouse/AirDistributionFanPower").attrib["code"])

    def getVentOpSchedMin(self):
        return int(self.myroot.find("./House/Ventilation/WholeHouse/OperationSchedule").attrib["value"])

    def getVentOpSchedCode(self):
        return int(self.myroot.find("./House/Ventilation/WholeHouse/OperationSchedule").attrib["code"])

    def __setHRVs(self):
        self.hrvs=[]
#   Find all the hrvs
        for hrv in self.myroot.findall("./House/Ventilation/WholeHouseVentilatorList/Hrv"):
            dict = {
                "supflowrate": hrv.attrib["supplyFlowrate"],
                "exhflowrate": hrv.attrib["exhaustFlowrate"],
                "fanPower1": hrv.attrib["fanPower1"],
                "isDefFanPow": hrv.attrib["isDefaultFanpower"],
                "isEnergyStar": hrv.attrib["isEnergyStar"],
                "isHVICert": hrv.attrib["isHomeVentilatingInstituteCertified"],
                "isSupplemental": hrv.attrib["isSupplemental"],
                "tempCond1": hrv.attrib["temperatureCondition1"],
                "tempCond2": hrv.attrib["temperatureCondition2"],
                "fanPower2": hrv.attrib["fanPower2"],
                "eff1": hrv.attrib["efficiency1"],
                "eff2": hrv.attrib["efficiency2"],
                "preheaterCap": hrv.attrib["preheaterCapacity"],
                "lowTempVentRed": hrv.attrib["lowTempVentReduction"],
                "coolingEff": hrv.attrib["coolingEfficiency"],
                "supductlength": hrv.find("ColdAirDucts/Supply").attrib["length"],
                "supductdia": hrv.find("ColdAirDucts/Supply").attrib["diameter"],
                "supductRSI": hrv.find("ColdAirDucts/Supply").attrib["insulation"],
                "supductLocCode": hrv.find("ColdAirDucts/Supply/Location").attrib["code"],
                "supductLoc": hrv.find("ColdAirDucts/Supply/Location/English").text,
                "supductTypCode": hrv.find("ColdAirDucts/Supply/Type").attrib["code"],
                "supductTyp": hrv.find("ColdAirDucts/Supply/Type/English").text,
                "supductSealCode": hrv.find("ColdAirDucts/Supply/Sealing").attrib["code"],
                "supductSeal": hrv.find("ColdAirDucts/Supply/Sealing/English").text,
                "exhductlength": hrv.find("ColdAirDucts/Exhaust").attrib["length"],
                "exhductdia": hrv.find("ColdAirDucts/Exhaust").attrib["diameter"],
                "exhductRSI": hrv.find("ColdAirDucts/Exhaust").attrib["insulation"],
                "exhductLocCode": hrv.find("ColdAirDucts/Exhaust/Location").attrib["code"],
                "exhductLoc": hrv.find("ColdAirDucts/Exhaust/Location/English").text,
                "exhductTypCode": hrv.find("ColdAirDucts/Exhaust/Type").attrib["code"],
                "exhductTyp": hrv.find("ColdAirDucts/Exhaust/Type/English").text,
                "exhductSealCode": hrv.find("ColdAirDucts/Exhaust/Sealing").attrib["code"],
                "exhductSeal": hrv.find("ColdAirDucts/Exhaust/Sealing/English").text,
            }
            self.hrvs.append(dict)

    def getHRVs(self):
        return self.hrvs

    def __setWholeHseVnt(self):
        self.wholehsevnt = []
#   Find all the base ventilators
        for vnt in self.myroot.findall("./House/Ventilation/WholeHouseVentilatorList/BaseVentilator"):
            dict = {
                "supflowrate": vnt.attrib["supplyFlowrate"],
                "exhflowrate": vnt.attrib["exhaustFlowrate"],
                "fanPower1": vnt.attrib["fanPower1"],
                "isDefFanPow": vnt.attrib["isDefaultFanpower"],
                "isEnergyStar": vnt.attrib["isEnergyStar"],
                "isHVICert": vnt.attrib["isHomeVentilatingInstituteCertified"],
                "isSupplemental": vnt.attrib["isSupplemental"],
                "vntTypeCode": vnt.find("VentilatorType").attrib["code"],
                "vntType": vnt.find("VentilatorType/English").text
            }
            self.wholehsevnt.append(dict)

    def getWholeHseVnt(self):
        return self.wholehsevnt

    def __setSuppVnt(self):
        self.suppvnt = []
#   Find all the supplementary ventilators
        for vnt in self.myroot.findall("./House/Ventilation/SupplementalVentilatorList/BaseVentilator"):
            dict = {
                "supflowrate": vnt.attrib["supplyFlowrate"],
                "exhflowrate": vnt.attrib["exhaustFlowrate"],
                "fanPower1": vnt.attrib["fanPower1"],
                "isDefFanPow": vnt.attrib["isDefaultFanpower"],
                "isEnergyStar": vnt.attrib["isEnergyStar"],
                "isHVICert": vnt.attrib["isHomeVentilatingInstituteCertified"],
                "isSupplemental": vnt.attrib["isSupplemental"],
                "vntTypeCode": vnt.find("VentilatorType").attrib["code"],
                "vntType": vnt.find("VentilatorType/English").text,
                "opSchedMin": vnt.find("OperationSchedule").attrib["value"],
                "opSchedCode": vnt.find("OperationSchedule").attrib["code"]
            }
            self.suppvnt.append(dict)
        for vnt in self.myroot.findall("./House/Ventilation/SupplementalVentilatorList/Dryer"):
            dict = {
                "supflowrate": vnt.attrib["supplyFlowrate"],
                "exhflowrate": vnt.attrib["exhaustFlowrate"],
                "fanPower1": vnt.attrib["fanPower1"],
                "isDefFanPow": vnt.attrib["isDefaultFanpower"],
                "isEnergyStar": vnt.attrib["isEnergyStar"],
                "isHVICert": vnt.attrib["isHomeVentilatingInstituteCertified"],
                "isSupplemental": vnt.attrib["isSupplemental"],
                "vntTypeCode": vnt.find("VentilatorType").attrib["code"],
                "vntType": vnt.find("VentilatorType/English").text,
                "opSchedMin": vnt.find("OperationSchedule").attrib["value"],
                "opSchedCode": vnt.find("OperationSchedule").attrib["code"],
                "exh": vnt.find("Exhaust/English").text,
                "exhCode": vnt.find("Exhaust").attrib["code"]
            }
            self.suppvnt.append(dict)

    def getSuppVnt(self):
        return self.suppvnt

##########################################################################################################
#   H2K Initialize Walls and child components
##########################################################################################################

    def __setWalls(self):
        self.walls=[]
        self.windows=[]
        self.doors=[]
        self.headers=[]
#   Find all the walls
        for wall in self.myroot.findall("./House/Components/Wall"):
            id = wall.attrib["id"]
            dict = {
                "adjEncSpace": wall.attrib["adjacentEnclosedSpace"],
                "id": id,
                "label": wall.find("Label").text,
                "corners": wall.find("Construction").attrib["corners"],
                "Intersects": wall.find("Construction").attrib["intersections"],
                "rValue": wall.find("Construction/Type").attrib["rValue"],
                "nominalIns": wall.find("Construction/Type").attrib["nominalInsulation"],
                "idref": wall.find("Construction/Type").attrib["idref"],
                "height": wall.find("Measurements").attrib["height"],
                "perimeter": wall.find("Measurements").attrib["perimeter"],
                "faceDirCode": wall.find("FacingDirection").attrib["code"],
                "faceDirTxt": wall.find("FacingDirection/English").text
            }
            self.walls.append(dict)

#       Find all the windows in this wall
            for window in wall.findall("Components/Window"):
                dictWin = self.__getThisWindow(window,id,"wall")
                self.windows.append(dictWin)
#       Find all the doors in this wall
            for door in wall.findall("Components/Door"):
                door_id = door.attrib["id"]
                dictDoor = self.__getThisDoor(door,id,"wall")
                self.doors.append(dictDoor)
#           Find all the windows in this door
                for window in door.findall("Components/Window"):
                    dictWin = self.__getThisWindow(window,door_id,"door")
                    self.windows.append(dictWin)
#       Find all the floor headers in this wall
            for header in wall.findall("Components/FloorHeader"):
                dictFH = self.__getThisFH(header,id,"wall")
                self.headers.append(dictFH)

##########################################################################################################
#   H2K Walls
##########################################################################################################

    def getWalls(self):        
        return self.walls

##########################################################################################################
#   H2K Windows
##########################################################################################################

    def getWindows(self):
        return self.windows

    def __getThisWindow(self,node,parent_id,parent_txt):
        dict = {
            "parent_id": parent_id,
            "parent_type": parent_txt,
            "number": node.attrib["number"],
            "er": node.attrib["er"],
            "shgc": node.attrib["shgc"],
            "frameHeight": node.attrib["frameHeight"],
            "frameAreaFrac": node.attrib["frameAreaFraction"],
            "edgeOfGlassFrac": node.attrib["edgeOfGlassFraction"],
            "centreOfGlassFrac": node.attrib["centreOfGlassFraction"],
            "adjEncSpace": node.attrib["adjacentEnclosedSpace"],
            "id": node.attrib["id"],
            "label": node.find("Label").text,
            "estar": node.find("Construction").attrib["energyStar"],
            "rValue": node.find("Construction/Type").attrib["rValue"],
            "idref": node.find("Construction/Type").attrib["idref"],
            "height": node.find("Measurements").attrib["height"],
            "width": node.find("Measurements").attrib["width"],
            "headerHeight": node.find("Measurements").attrib["headerHeight"],
            "overhangWidth": node.find("Measurements").attrib["overhangWidth"],
            "tiltCode": node.find("Measurements/Tilt").attrib["code"],
            "tiltVal": node.find("Measurements/Tilt").attrib["value"],
            "tiltTxt": node.find("Measurements/Tilt/English").text,
            "curtain": node.find("Shading").attrib["curtain"],
            "shutterRVal": node.find("Shading").attrib["shutterRValue"],
            "faceDirCode": node.find("FacingDirection").attrib["code"],
            "faceDirTxt": node.find("FacingDirection/English").text
        }
        return dict
        

##########################################################################################################
#   H2K Doors
##########################################################################################################

    def getDoors(self):
        return self.doors

    def __getThisDoor(self,node,parent_id,parent_txt):
        dictDoor = {
            "parent_id": parent_id,
            "parent_type": parent_txt,
            "id": node.attrib["id"],
            "rValue": node.attrib["rValue"],
            "adjEncSpace": node.attrib["adjacentEnclosedSpace"],
            "estar": node.find("Construction").attrib["energyStar"],
            "height": node.find("Measurements").attrib["height"],
            "width": node.find("Measurements").attrib["width"]
        }
        return dictDoor

##########################################################################################################
#   H2K Floor Headers
##########################################################################################################

    def getFloorHeaders(self):
        return self.headers

    def __getThisFH(self,node,parent_id,parent_txt):
        dict = {
            "adjEncSpace": node.attrib["adjacentEnclosedSpace"],
            "id": node.attrib["id"],
            "parent_id": parent_id,
            "parent_type": parent_txt,
            "rValue": node.find("Construction/Type").attrib["rValue"],
            "nominalIns": node.find("Construction/Type").attrib["nominalInsulation"],
            "idref": node.find("Construction/Type").attrib["idref"],
            "height": node.find("Measurements").attrib["height"],
            "perimeter": node.find("Measurements").attrib["perimeter"],
            "faceDirCode": node.find("FacingDirection").attrib["code"],
            "faceDirTxt": node.find("FacingDirection/English").text
        }
        return dict

##########################################################################################################
#   H2K Ceilings and child components
##########################################################################################################

    def getCeilings(self):
        return self.ceilings

    def __setCeilings(self):
        self.ceilings=[]
        #   Find all the ceilings
        for ceil in self.myroot.findall("./House/Components/Ceiling"):
            id = ceil.attrib["id"]
            dict = {
                "id": id,
                "typeCode": ceil.find("Construction/Type").attrib["code"],
                "typeTxt": ceil.find("Construction/Type/English").text,
                "rValue": ceil.find("Construction/CeilingType").attrib["rValue"],
                "nominalIns": ceil.find("Construction/CeilingType").attrib["nominalInsulation"],
                "length": ceil.find("Measurements").attrib["length"],
                "area": ceil.find("Measurements").attrib["area"],
                "heelHeight": ceil.find("Measurements").attrib["heelHeight"],
                "slopeCode": ceil.find("Measurements/Slope").attrib["code"],
                "slopeVal": ceil.find("Measurements/Slope").attrib["value"],
            }
            self.ceilings.append(dict)
         # Add any skylights to list
            for window in ceil.findall("Components/Window"):
                dictWin = self.__getThisWindow(window,id,"ceil")
                self.windows.append(dictWin)

##########################################################################################################
#   H2K Basements
##########################################################################################################

    def getBasements(self):
        return self.bsmts

    def __setBasements(self):
        self.bsmts=[]
#   Find all the basements (and check for windows, doors, and floor headers)
        for bsmt in self.myroot.findall("./House/Components/Basement"):
            id = bsmt.attrib["id"]
            dict = {
                "id": id,
                "isExposed": bsmt.attrib["isExposedSurface"],
                "expSurfPerim": bsmt.attrib["exposedSurfacePerimeter"],
                "label": bsmt.find("Label").text,
                "cfgType": bsmt.find("Configuration").attrib["type"],
                "subType": bsmt.find("Configuration").attrib["subtype"],
                "overlap": bsmt.find("Configuration").attrib["overlap"],
                "openUpStrsCode": bsmt.find("OpeningUpstairs").attrib["code"],
                "openUpStrsArea": bsmt.find("OpeningUpstairs").attrib["value"],
                "roomType": bsmt.find("RoomType/English").text,
                "roomType": bsmt.find("RoomType").attrib["code"],
                "flrIsBelowFrost": bsmt.find("Floor/Construction").attrib["isBelowFrostline"],
                "flrHasIntFoot": bsmt.find("Floor/Construction").attrib["hasIntegralFooting"],
                "flrHeated": bsmt.find("Floor/Construction").attrib["heatedFloor"],
                "flrAddRSI": bsmt.find("Floor/Construction/AddedToSlab").attrib["rValue"],
                "flrAddNomRSI": bsmt.find("Floor/Construction/AddedToSlab").attrib["nominalInsulation"],
                "flrAbvRSI": bsmt.find("Floor/Construction/FloorsAbove").attrib["rValue"],
                "flrAbvNomRSI": bsmt.find("Floor/Construction/FloorsAbove").attrib["nominalInsulation"],
                "flrIsRect": bsmt.find("Floor/Measurements").attrib["isRectangular"],
                "wallHasPony": bsmt.find("Wall").attrib["hasPonyWall"],
                "wallCorners": bsmt.find("Wall/Construction").attrib["corners"],
                "wallIntInsNom": bsmt.find("Wall/Construction/InteriorAddedInsulation").attrib["nominalInsulation"],
                "wallIntInsRSI": bsmt.find("Wall/Construction/InteriorAddedInsulation/Composite/Section").attrib["rsi"],
                "wallHeight": bsmt.find("Wall/Measurements").attrib["height"],
                "wallDepth": bsmt.find("Wall/Measurements").attrib["depth"],
                "wallPonyHeight": bsmt.find("Wall/Measurements").attrib["ponyWallHeight"]                
            }
            if  dict["flrIsRect"] == "true":
                dict["flrLength"] = bsmt.find("Floor/Measurements").attrib["length"]
                dict["flrWidth"] = bsmt.find("Floor/Measurements").attrib["length"]
                dict["flrArea"] = str(float(dict['length'])*float(dict['width']))
                dict["flrPerim"] = str(float(dict['length'])*float(dict['width']))
            else:
                dict["flrArea"] = bsmt.find("Floor/Measurements").attrib["area"]
                dict["flrPerim"] = bsmt.find("Floor/Measurements").attrib["perimeter"]
                dict["flrLength"] = "-1"
                dict["flrWidth"] = "-1"

            if dict["wallHasPony"] == "true":
                dict["ponyInsNom"] = bsmt.find("Wall/Construction/PonyWallType/Composite/Section").attrib["nominalRsi"]
                dict["ponyInsRSI"] = bsmt.find("Wall/Construction/PonyWallType/Composite/Section").attrib["rsi"]
            else:
                dict["ponyInsNom"] = "0"
                dict["ponyInsRSI"] = "0"
            
            self.bsmts.append(dict)
            # Find all windows in this basement
            for window in bsmt.findall("Components/Window"):
                dictWin = self.__getThisWindow(window,id,"bsmt")
                self.windows.append(dictWin)
            # Find all the doors in this basement
            for door in bsmt.findall("Components/Door"):
                door_id = door.attrib["id"]
                dictDoor = self.__getThisDoor(door,id,"bsmt")
                self.doors.append(dictDoor)
                # Find all the windows in this door
                for window in door.findall("Components/Window"):
                    dictWin = self.__getThisWindow(window,door_id,"door")
                    self.windows.append(dictWin)
            # Find all the floor headers in this basement
            for header in bsmt.findall("Components/FloorHeader"):
                dictFH = self.__getThisFH(header,id,"bsmt")
                self.headers.append(dictFH)