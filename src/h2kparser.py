from time import sleep
import xmlschema


class ParseH2K:
    def __init__(self, h2k_file: str, schema_file: str) -> None:
        self.file = h2k_file
        self.schema_file = schema_file
        self.h2k_schema = xmlschema.XMLSchema(
            schema_file)
        assert self.h2k_schema.is_valid(self.file), "Not a valid h2k file"
        self.h2k_dict = self.h2k_schema.to_dict(h2k_file)

    def __str__(self) -> str:
        return f"H2K file is {self.file}"

    @staticmethod
    def slice_dict_by_key(input_dict: dict, keys_to_extract: list) -> dict:
        return {key: input_dict[key] for key in keys_to_extract}

    def get_version(self) -> dict:
        return self.slice_dict_by_key(self.h2k_dict['Application']['Version'], ['@major', '@minor'])

    def get_file_id(self) -> str:
        return self.h2k_dict['ProgramInformation']['File']['Identification']

    def get_climate_Prov(self) -> str:
        return self.h2k_dict['ProgramInformation']['Weather']['Region']['English']

    def get_climate_city(self) -> str:
        return self.h2k_dict['ProgramInformation']['Weather']['Location']['English']

    def get_hdd_frostdepth(self) -> dict:
        return self.slice_dict_by_key(self.h2k_dict['ProgramInformation']['Weather'], ['@depthOfFrost', '@heatingDegreeDay'])

    def get_house_type(self) -> dict:
        return self.slice_dict_by_key(self.h2k_dict['House']['Specifications']['HouseType'], ['English', '@code'])

    def get_plan_type(self) -> dict:
        return self.slice_dict_by_key(self.h2k_dict['House']['Specifications']['PlanShape'], ['English', '@code'])

    def get_n_storey(self) -> dict:
        return self.slice_dict_by_key(self.h2k_dict['House']['Specifications']['Storeys'], ['English', '@code'])

    def get_facing_direction(self) -> dict:
        return self.slice_dict_by_key(self.h2k_dict['House']['Specifications']['FacingDirection'], ['English', '@code'])

    def get_thermal_mass(self) -> dict:
        return self.slice_dict_by_key(self.h2k_dict['House']['Specifications']['ThermalMass'], ['English', '@code'])

    def get_vintage(self) -> int:
        vintage_bins = {2: 1920, 3: 1925, 4: 1935, 5: 1945,
                        6: 1955, 7: 1965, 8: 1975, 9: 1985, 10: 1995, 11: 2005}
        vintage_code = self.h2k_dict['House']['Specifications']['YearBuilt']['@code']
        if vintage_code in vintage_bins.keys():
            vintage = vintage_bins[vintage_code]
        else:
            vintage = self.h2k_dict['House']['Specifications']['YearBuilt']['@value']
        return vintage

    def get_heated_area(self) -> dict:
        return self.slice_dict_by_key(self.h2k_dict['House']['Specifications']['HeatedFloorArea'], ['@aboveGrade', '@belowGrade'])

    def get_roofcavity_spec(self) -> dict:
        return self.slice_dict_by_key(self.h2k_dict['House']['Specifications']['RoofCavity'], ['@ventilationRate', '@volume'])

    def get_gableend_area(self) -> float:
        return float(self.h2k_dict['House']['Specifications']['RoofCavity']['GableEnds']['@area'])

    def get_gableend_sheating(self) -> dict:
        return self.slice_dict_by_key(self.h2k_dict['House']['Specifications']['RoofCavity']['GableEnds']['SheatingMaterial'],
                                      ['@code', '@value'])

    def get_gableend_exteriormaterial(self) -> dict:
        return self.slice_dict_by_key(self.h2k_dict['House']['Specifications']['RoofCavity']['GableEnds']['ExteriorMaterial'],
                                      ['@code', '@value'])

    def get_maintemp_setpoint(self) -> dict:
        return self.slice_dict_by_key(self.h2k_dict['House']['Temperatures']['MainFloors'],
                                      ['@daytimeHeatingSetPoint', '@nighttimeHeatingSetPoint', '@nighttimeSetbackDuration', '@coolingSetPoint'])

    def get_mainallowed_temp_rise(self) -> float:
        AllowedTempRise = {1: 0, 2: 2.8, 3: 5.5}
        return AllowedTempRise[int(self.h2k_dict['House']['Temperatures']['MainFloors']['AllowableRise']['@code'])]

    def get_basement_temp_setpoint(self) -> dict:
        return self.slice_dict_by_key(self.h2k_dict['House']['Temperatures']['Basement'],
                                      ['@heated', '@cooled', '@separateThermostat', '@basementUnit', '@heatingSetPoint'])

    def get_equipment_setpoint(self) -> dict:
        return self.slice_dict_by_key(self.h2k_dict['House']['Temperatures']['Equipment'], ['@heatingSetPoint', '@coolingSetPoint'])

    def get_crawlspace_setpoint(self) -> dict:
        return self.slice_dict_by_key(self.h2k_dict['House']['Temperatures']['Crawlspace'], ['@heated', '@heatingSetPoint'])

    def get_basement_fraction_internalgains(self) -> float:
        return float(self.h2k_dict['House']['BaseLoads']['@basementFractionOfInternalGains'])

    def get_occupancy_adult(self) -> dict:
        return self.slice_dict_by_key(self.h2k_dict['House']['BaseLoads']['Occupancy']['Adults'], ['@atHome', '@occupants'])

    def get_occupancy_children(self) -> dict:
        return self.slice_dict_by_key(self.h2k_dict['House']['BaseLoads']['Occupancy']['Children'], ['@atHome', '@occupants'])

    def get_occupancy_infants(self) -> dict:
        return self.slice_dict_by_key(self.h2k_dict['House']['BaseLoads']['Occupancy']['Infants'], ['@atHome', '@occupants'])

    def get_base_loads(self) -> dict:
        return self.slice_dict_by_key(self.h2k_dict['House']['BaseLoads']['Summary'],
                                      ['@electricalAppliances', '@exteriorUse', '@hotWaterLoad', '@lighting', '@otherElectric'])

    def get_house_volume(self) -> float:
        return float(self.h2k_dict['House']['NaturalAirInfiltration']['Specifications']['House']['@volume'])

    def get_infiltration(self) -> dict:
        return self.slice_dict_by_key(self.h2k_dict['House']['NaturalAirInfiltration']['Specifications']['BlowerTest'],
                                      ['@airChangeRate', '@leakageArea'])

    def get_site_terrain(self) -> dict:
        return self.slice_dict_by_key(self.h2k_dict['House']['NaturalAirInfiltration']['Specifications']['BuildingSite']['Terrain'],
                                      ['@code', 'English'])

    def get_walls_shielding(self) -> dict:
        return self.slice_dict_by_key(self.h2k_dict['House']['NaturalAirInfiltration']['Specifications']['LocalShielding']['Walls'],
                                      ['@code', 'English'])

    def get_flue_shielding(self) -> dict:
        return self.slice_dict_by_key(self.h2k_dict['House']['NaturalAirInfiltration']['Specifications']['LocalShielding']['Flue'],
                                      ['@code', 'English'])

    def get_n_rooms(self) -> dict:
        return self.slice_dict_by_key(self.h2k_dict['House']['Ventilation']['Rooms'],
                                      ['@bathrooms', '@bedrooms', '@living', '@otherHabitable', '@utility'])

    def get_vent_distribution_type(self) -> dict:
        return self.slice_dict_by_key(self.h2k_dict['House']['Ventilation']['WholeHouse']['AirDistributionType'], ['@code', 'English'])

    def get_vent_distribution_fan(self) -> dict:
        return self.slice_dict_by_key(self.h2k_dict['House']['Ventilation']['WholeHouse']['AirDistributionFanPower'], ['@code', 'English'])

    def get_vent_distribution_operation(self) -> dict:
        return self.slice_dict_by_key(self.h2k_dict['House']['Ventilation']['WholeHouse']['OperationSchedule'], ['@code', '@value'])

    def get_hrv(self):
        hrv_list = self.h2k_dict['House']['Ventilation']['WholeHouseVentilatorList']['Hrv']
        hrv_spec = []
        for hrv in hrv_list:
            hrv_eqipment = self.slice_dict_by_key(
                hrv, ['@supplyFlowrate', '@exhaustFlowrate', '@fanPower1', '@fanPower2', '@isDefaultFanpower', '@isEnergyStar',
                      '@isHomeVentilatingInstituteCertified', '@isSupplemental', '@temperatureCondition1', '@temperatureCondition2',
                      '@lowTempVentReduction', '@efficiency1', '@efficiency2', '@preheaterCapacity', '@lowTempVentReduction', '@coolingEfficiency'])

            supp_duct = self.slice_dict_by_key(hrv['ColdAirDucts']['Supply'], [
                                               '@length', '@diameter', '@insulation'])
            supp_duct.update({'seal': hrv['ColdAirDucts']['Supply']['Sealing']['English'], 'sealcode': hrv['ColdAirDucts']['Supply']['Sealing']['@code'],
                              'type': hrv['ColdAirDucts']['Supply']['Type']['English'], 'typecode': hrv['ColdAirDucts']['Supply']['Type']['@code']})

            supp_duct = {f"supply_{key}": val for key,
                         val in supp_duct.items()}
            hrv_eqipment.update(supp_duct)

            exh_duct = self.slice_dict_by_key(hrv['ColdAirDucts']['Exhaust'], [
                                              '@length', '@diameter', '@insulation'])
            exh_duct.update({'seal': hrv['ColdAirDucts']['Exhaust']['Sealing']['English'], 'sealcode': hrv['ColdAirDucts']['Exhaust']['Sealing']['@code'],
                             'type': hrv['ColdAirDucts']['Exhaust']['Type']['English'], 'typecode': hrv['ColdAirDucts']['Exhaust']['Type']['@code']})

            exh_duct = {f"exhaust_{key}": val for key, val in exh_duct.items()}
            hrv_eqipment.update(exh_duct)

            hrv_spec.append(hrv_eqipment)

        return hrv_spec

    def get_supplement_ventilation(self):
        vents = self.h2k_dict['House']['Ventilation']['SupplementalVentilatorList']
        vent_sepc = []
        for vent in vents:
            for system in vents[vent]:
                vent_sys = self.slice_dict_by_key(system, ['@supplyFlowrate', '@exhaustFlowrate', '@fanPower1', '@isDefaultFanpower',
                                                           '@isEnergyStar', '@isHomeVentilatingInstituteCertified', '@isSupplemental'])
                vent_sys.update({'ventilatortype': system['VentilatorType']['English'], 'ventilatortypecode': system['VentilatorType']['@code'],
                                 'operationschedule': system['OperationSchedule']['@value'], 'operationschedulecode': system['OperationSchedule']['@code']})

                vent_sepc.append(vent_sys)

        return vent_sepc

    def extract_this_window(self, window, parent_id, parent_label, parent_type):
        window_def = {
            'parent_type': parent_type, 'parent_id': parent_id, 'parent_label': parent_label}
        window_def.update(self.slice_dict_by_key(window, ['@id', 'Label', '@number', '@er', '@shgc', '@frameHeight', '@frameAreaFraction',
                                                          '@edgeOfGlassFraction', '@centreOfGlassFraction']))
        window_def.update(self.slice_dict_by_key(
            window['Construction'], ['@energyStar']))
        window_def.update(self.slice_dict_by_key(
            window['Construction']['Type'], ['@rValue', '@idref']))
        window_def.update(self.slice_dict_by_key(window['Measurements'], [
            '@height', '@width', '@headerHeight', '@overhangWidth']))
        window_def.update({'tiltValue': window['Measurements']['Tilt']['@value'],
                           'tiltCode': window['Measurements']['Tilt']['@code'],
                           'tiltText': window['Measurements']['Tilt']['English']})
        window_def.update(self.slice_dict_by_key(
            window['Shading'], ['@curtain', '@shutterRValue']))
        window_def.update({'facingDirection': window['FacingDirection']['English'],
                           'facingDirectionCode': window['FacingDirection']['@code']})

        return window_def

    def extract_this_door(self, door, parent_id, parent_label, parent_type):
        door_def = {
            'parent_type': parent_type, 'parent_id': parent_id, 'parent_label': parent_label}
        door_def.update(self.slice_dict_by_key(
            door, ['@id', 'Label', '@rValue']))
        door_def.update({'energystar': door['Construction']['@energyStar'],
                         'type': door['Construction']['Type']['English']})
        door_def.update(self.slice_dict_by_key(
            door['Measurements'], ['@height', '@width']))

        return door_def

    def extract_this_header(self, header, parent_id, parent_label, parent_type):
        header_def = {
            'parent_type': parent_type, 'parent_id': parent_id, 'parent_label': parent_label}
        header_def.update(self.slice_dict_by_key(
            header, ['@id', 'Label']))
        header_def.update(self.slice_dict_by_key(header['Construction']['Type'], [
            '@nominalInsulation', '@rValue', '@idref']))
        header_def.update(self.slice_dict_by_key(
            header['Measurements'], ['@height', '@perimeter']))

        return header_def

    def extract_this_basement(self, bsmt):
        bsmt_def = self.slice_dict_by_key(
            bsmt, ['@id', 'Label', '@isExposedSurface', '@exposedSurfacePerimeter'])
        bsmt_def.update(self.slice_dict_by_key(
            bsmt['Configuration'], ['@type', '@subtype', '@overlap']))
        bsmt_def.update({'openUpStrsCode': bsmt['OpeningUpstairs']['@code'],
                         'openUpStrsArea': bsmt['OpeningUpstairs']['@value'],
                         'roomTypeCode': bsmt['RoomType']['@code'],
                         'roomType': bsmt['RoomType']['English'],
                         'flrIsBelowFrost': bsmt['Floor']['Construction']['@isBelowFrostline'],
                         'flrHasIntFoot': bsmt['Floor']['Construction']['@hasIntegralFooting'],
                         'flrHeated': bsmt['Floor']['Construction']['@heatedFloor'],
                         'flrAddRSI': bsmt['Floor']['Construction']['AddedToSlab']['@rValue'],
                         'flrAddNomRSI': bsmt['Floor']['Construction']['AddedToSlab']['@nominalInsulation'],
                         'flrAbvRSI': bsmt['Floor']['Construction']['FloorsAbove']['@rValue'],
                         'flrAbvNomRSI': bsmt['Floor']['Construction']['FloorsAbove']['@nominalInsulation'],
                         'flrIsRect': bsmt['Floor']['Measurements']['@isRectangular'],
                         'wallHasPony': bsmt['Wall']['@hasPonyWall'],
                         'wallCorners': bsmt['Wall']['Construction']['@corners'],
                         'wallIntInsNom': 0,
                         'wallIntInsCompositeRSI': [],
                         'wallIntInsCompositePercentage': [],
                         'wallExtInsNom': bsmt['Wall']['Construction']['ExteriorAddedInsulation']['@nominalInsulation'],
                         'wallExtInsCompositeRSI': [],
                         'wallExtInsCompositePercentage': [],
                         'wallHeight': bsmt['Wall']['Measurements']['@height'],
                         'wallDepth': bsmt['Wall']['Measurements']['@depth'],
                         'wallPonyHeight': bsmt['Wall']['Measurements']['@ponyWallHeight']})

        if 'InteriorAddedInsulation' in bsmt['Wall']['Construction']:
            bsmt_def['wallIntInsNom'] = bsmt['Wall']['Construction']['InteriorAddedInsulation']['@nominalInsulation']
            n_sections_composite_construction = len(
                bsmt['Wall']['Construction']['InteriorAddedInsulation']['Composite']['Section'])
            for i in range(n_sections_composite_construction):
                bsmt_def['wallIntInsCompositeRSI'].append(
                    bsmt['Wall']['Construction']['InteriorAddedInsulation']['Composite']['Section'][i]['@rsi'])
                if n_sections_composite_construction == 1 or (n_sections_composite_construction > 1 and i < n_sections_composite_construction - 1):
                    bsmt_def['wallIntInsCompositePercentage'].append(
                        bsmt['Wall']['Construction']['InteriorAddedInsulation']['Composite']['Section'][i]['@percentage'])
                else:
                    bsmt_def['wallIntInsCompositePercentage'].append(100 -
                                                                     sum(bsmt_def['wallIntInsCompositePercentage']))

        if 'ExteriorAddedInsulation' in bsmt['Wall']['Construction']:
            bsmt_def['wallExtInsNom'] = bsmt['Wall']['Construction']['ExteriorAddedInsulation']['@nominalInsulation']
            n_sections_composite_construction = len(
                bsmt['Wall']['Construction']['ExteriorAddedInsulation']['Composite']['Section'])
            for i in range(n_sections_composite_construction):
                bsmt_def['wallExtInsCompositeRSI'].append(
                    bsmt['Wall']['Construction']['ExteriorAddedInsulation']['Composite']['Section'][i]['@rsi'])
                if n_sections_composite_construction == 1 or (n_sections_composite_construction > 1 and i < n_sections_composite_construction - 1):
                    bsmt_def['wallExtInsCompositePercentage'].append(
                        bsmt['Wall']['Construction']['ExteriorAddedInsulation']['Composite']['Section'][i]['@percentage'])
                else:
                    bsmt_def['wallExtInsCompositePercentage'].append(100 -
                                                                     sum(bsmt_def['wallExtInsCompositePercentage']))

        if bsmt_def['flrIsRect']:
            bsmt_def['flrLength'] = bsmt['Floor']['Measurements']['@length']
            bsmt_def['flrWidth'] = bsmt['Floor']['Measurements']['@width']
            bsmt_def['flrArea'] = bsmt_def['flrLength'] * \
                bsmt_def['flrWidth']
            bsmt_def['flrPerim'] = 2 * \
                (bsmt_def['flrLength'] + bsmt_def['flrWidth'])
        else:
            bsmt_def["flrArea"] = bsmt['Floor']['Measurements']['@area']
            bsmt_def["flrPerim"] = bsmt['Floor']['Measurements']['@perimeter']
            bsmt_def["flrLength"] = -1
            bsmt_def["flrWidth"] = -1

        if bsmt_def['wallHasPony']:
            bsmt_def['ponyInsNom'] = bsmt['Wall']['Construction']['PonyWallType']['Composite']['Section']['@nominalRsi']
            bsmt_def['ponyInsRSI'] = bsmt['Wall']['Construction']['PonyWallType']['Composite']['Section']['@rsi']
        else:
            bsmt_def['ponyInsNom'] = 0
            bsmt_def['ponyInsRSI'] = 0

        return bsmt_def

    def get_walls_spec(self):
        walls = self.h2k_dict['House']['Components']['Wall']
        walls_spec = []

        for wall in walls:
            wall_def = self.slice_dict_by_key(
                wall, ['@id', 'Label', '@adjacentEnclosedSpace'])
            wall_def.update(self.slice_dict_by_key(
                wall['Construction'], ['@corners', '@intersections']))
            wall_def.update(self.slice_dict_by_key(
                wall['Construction']['Type'], ['@nominalInsulation', '@rValue', '@idref']))
            wall_def.update(self.slice_dict_by_key(
                wall['Measurements'], ['@height', '@perimeter']))
            wall_def.update({'facingDirection': wall['FacingDirection']['English'],
                            'facingDirectionCode': wall['FacingDirection']['@code']})

            walls_spec.append(wall_def)

        return walls_spec

    def get_windows_spec(self):
        walls = self.h2k_dict['House']['Components']['Wall']
        windows_spec = []

        for wall in walls:
            if 'Window' in wall['Components']:
                windows = wall['Components']['Window']

                for window in windows:
                    window_def = self.extract_this_window(
                        window, wall['@id'], wall['Label'], 'wall')

                    windows_spec.append(window_def)
            else:
                continue

        return windows_spec

    def get_doors_spec(self):
        walls = self.h2k_dict['House']['Components']['Wall']
        doors_spec = []
        door_windows_spec = []

        for wall in walls:
            if 'Door' in wall['Components']:
                doors = wall['Components']['Door']

                for door in doors:
                    door_def = self.extract_this_door(
                        door, wall['@id'], wall['Label'], 'wall')

                    doors_spec.append(door_def)

                    if 'Components' in door:
                        door_windows = door['Components']['Window']

                        for window in door_windows:
                            win_door_def = self.extract_this_window(
                                window, door['@id'], door['Label'], 'door')

                            door_windows_spec.append(win_door_def)
                    else:
                        continue
            else:
                continue

        return doors_spec, door_windows_spec

    def get_floor_header(self):
        walls = self.h2k_dict['House']['Components']['Wall']
        headers_spec = []

        for wall in walls:
            if 'FloorHeader' in wall['Components']:
                headers = wall['Components']['FloorHeader']
                for header in headers:
                    header_def = self.extract_this_header(
                        header, wall['@id'], wall['Label'], 'wall')

                    headers_spec.append(header_def)
            else:
                continue

        return headers_spec

    def get_ceiling_spec(self):
        ceilings = self.h2k_dict['House']['Components']['Ceiling']
        ceiling_spec = []
        skylight_spec = []

        for ceiling in ceilings:
            ceiling_def = self.slice_dict_by_key(ceiling, ['@id', 'Label'])
            ceiling_def.update(
                {'type': ceiling['Construction']['Type']['English']})
            ceiling_def.update(self.slice_dict_by_key(ceiling['Construction']['CeilingType'], [
                               '@idref', '@nominalInsulation', '@rValue']))
            ceiling_def.update(self.slice_dict_by_key(ceiling['Measurements'], [
                               '@area', '@heelHeight', '@length']))
            ceiling_def.update({'slopeCode': ceiling['Measurements']['Slope']['@code'],
                                'slopeValue': ceiling['Measurements']['Slope']['@value']})

            ceiling_spec.append(ceiling_def)

            if 'Components' in ceiling:
                skylights = ceiling['Components']['Window']

                for window in skylights:
                    skylight_def = self.extract_this_window(
                        window, ceiling['@id'], ceiling['Label'], 'ceiling')

                    skylight_spec.append(skylight_def)
            else:
                continue

        return ceiling_spec, skylight_spec

    def get_exposed_floor(self):
        floors = self.h2k_dict['House']['Components']['Floor']
        floors_sepc = []

        for floor in floors:
            floor_def = self.slice_dict_by_key(floor, ['@id', 'Label'])
            floor_def.update(self.slice_dict_by_key(floor['Construction']['Type'], [
                             '@idref', '@nominalInsulation', '@rValue']))
            floor_def.update(self.slice_dict_by_key(
                floor['Measurements'], ['@area', '@length']))

            floors_sepc.append(floor_def)

        return floors_sepc

    def get_basement_spec(self):
        basement = self.h2k_dict['House']['Components']['Basement']
        basement_spec = []
        bsmt_windows_spec = []
        bsmt_headers_spec = []
        bsmt_doors_spec = []
        bsmt_door_windows_spec = []

        for bsmt in basement:
            bsmt_def = self.extract_this_basement(bsmt)
            basement_spec.append(bsmt_def)

            if 'Window' in bsmt['Components']:
                windows = bsmt['Components']['Window']

                for window in windows:
                    window_def = self.extract_this_window(
                        window, bsmt['@id'], bsmt['Label'], 'basement')

                    bsmt_windows_spec.append(window_def)

            if 'FloorHeader' in bsmt['Components']:
                headers = bsmt['Components']['FloorHeader']
                for header in headers:
                    header_def = self.extract_this_header(
                        header, bsmt['@id'], bsmt['Label'], 'basement')

                    bsmt_headers_spec.append(header_def)

            if 'Door' in bsmt['Components']:
                doors = bsmt['Components']['Door']

                for door in doors:
                    door_def = self.extract_this_door(
                        door, bsmt['@id'], bsmt['Label'], 'basement')

                    bsmt_doors_spec.append(door_def)

                    if 'Components' in door:
                        door_windows = door['Components']['Window']

                        for window in door_windows:
                            win_door_def = self.extract_this_window(
                                window, door['@id'], door['Label'], 'door')

                            bsmt_door_windows_spec.append(win_door_def)

        return basement_spec, bsmt_windows_spec, bsmt_headers_spec, bsmt_doors_spec, bsmt_door_windows_spec

    def get_hotwater_spec(self):
        hotwater = self.h2k_dict['House']['Components']['HotWater']
        dhw_order = ['Primary', 'Secondary']
        dhw_spec = []
        dwhr_spec = []

        for dhw in hotwater:
            for order in dhw_order:
                dhw_def = self.slice_dict_by_key(dhw, ['@id', 'Label'])
                if order in dhw:
                    dhw_def.update({'systemtype': order,
                                    'energysource': dhw[order]['EnergySource']['English'],
                                    'tanktype': dhw[order]['TankType']['English'],
                                    'tankvolume': dhw[order]['TankVolume']['@value'],
                                    'energyfactor': dhw[order]['EnergyFactor']['@value'],
                                    'tanklocation': dhw[order]['TankLocation']['English']})
                    dhw_spec.append(dhw_def)

                    if 'DrainWaterHeatRecovery' in dhw[order]:
                        dwhr_def = {
                            'parent_id': dhw['@id'], 'parent_label': dhw['Label'], 'parent_type': order}
                        dwhr_def.update(self.slice_dict_by_key(dhw[order]['DrainWaterHeatRecovery'], [
                            '@dailyShowers', '@effectivenessAt9.5', '@preheatShowerTank', '@showerLength', 'Efficiency']))
                        dwhr_def.update({'ShowerTemperature': dhw[order]['DrainWaterHeatRecovery']['ShowerTemperature']['English'],
                                         'ShowerHead': dhw[order]['DrainWaterHeatRecovery']['ShowerHead']['English']})

                        dwhr_spec.append(dwhr_def)

        return dhw_spec, dwhr_spec
