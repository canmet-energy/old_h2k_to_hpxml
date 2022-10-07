from inspect import Parameter
import json

from h2kparser import ParseH2K


class BuildHPXML:
    def __init__(self, path_to_hpxml_template: str, path_to_h2k: str, path_to_h2k_schema: str) -> None:
        self.template_dict = self._read_json(path_to_hpxml_template)
        self.h2k_parameters = ParseH2K(path_to_h2k, path_to_h2k_schema)

    def _read_json(self, path: str) -> dict:
        with open(path, 'r') as json_file:
            json_dict = json.loads(json_file.read())
        return json_dict

    def update_run_directory(self, path_to_run_directory: str) -> None:
        self.template_dict['run_directory'] = path_to_run_directory

    def update_steps(self):
        for step in self.template_dict['steps']:
            if step['measure_dir_name'] == 'BuildResidentialHPXML':
                step['arguments'] = self.update_envelope_spec(
                    step['arguments'])
                step['arguments'] = self.update_systems_spec(step['arguments'])

            elif step['measure_dir_name'] == 'BuildResidentialScheduleFile':
                pass
            elif step['measure_dir_name'] == 'HPXMLtoOpenStudio':
                pass
            elif step['measure_dir_name'] == 'ReportSimulationOutput':
                pass
            elif step['measure_dir_name'] == 'ReportHPXMLOutput':
                pass
            elif step['measure_dir_name'] == 'ReportUtilityBills':
                pass
        return

    def update_envelope_spec(self, arguments: dict) -> dict:
        # Infiltration
        infiltration = self.h2k_parameters.get_infiltration()
        arguments['air_leakage_value'] = round(
            infiltration['@airChangeRate'], 1)

        # Rooms
        rooms = self.h2k_parameters.get_n_rooms()
        arguments['geometry_unit_num_bedrooms'] = rooms['@bedrooms']

        # Storeys
        storeys = self.h2k_parameters.get_n_storey()
        # keys are the codes used in H2K for the number of storeys (starts from 1 and incrementing by 0.5 storey)
        # code 6 and 7 refer to split levels
        map_h2k_storeys_to_hpxml = {'1': 1, '2': 1,
                                    '3': 2, '4': 2, '5': 3, '6': 1, '7': 1}
        arguments['geometry_unit_num_floors_above_grade'] = map_h2k_storeys_to_hpxml[storeys['@code']]

        # Conditioned Floor Area
        heated_area = self.h2k_parameters.get_heated_area()
        def m2_to_ft2(area): return round(float(area) * 10.764, 1)
        arguments['geometry_unit_cfa'] = m2_to_ft2(heated_area['@aboveGrade'] +
                                                   heated_area['@belowGrade'])

        # Ceiling Assembly
        # -- Ceiling Construction
        ceilings, _ = self.h2k_parameters.get_ceiling_spec()
        ua_val, area = 0, 0
        for ceiling in ceilings:
            area += ceiling['@area']
            ua_val += ceiling['@area'] / ceiling['@rValue']
        arguments['ceiling_assembly_r'] = round(
            area/ua_val, 1)
        # -- Ceiling Geometry
        roof_pitch = {'1': '', '2': '2:12', '3': '3:12',
                      '4': '4:12', '5': '5:12', '6': '6:12',
                      '7': '7:12'}
        # For now the first ceiling is used to determine the slope. we need to change the code to handle
        # multiple ceilings or a flat roof.
        arguments['geometry_roof_pitch'] = roof_pitch[ceilings[0]['slopeCode']]

        # Doors
        doors, _ = self.h2k_parameters.get_doors_spec()
        ua_val, area = 0, 0
        for door in doors:
            current = door['@height'] * door['@width']
            area += current
            ua_val += current / door['@rValue']
        arguments['door_area'] = area
        arguments['door_rvalue'] = round(
            area/ua_val, 2)

        # Direction
        direction = self.h2k_parameters.get_facing_direction()
        front_code = direction['@code']
        # HOT2000 direction code starts from South (code = 1) and progress
        # by 45 degrees counter-clockwise
        left_code = str((int(front_code) + 2) %
                        8) if front_code != '6' else '8'
        right_code = str((int(front_code) - 2) %
                         8) if front_code != '2' else '8'
        back_code = str((int(front_code) + 4) %
                        8) if front_code != '4' else '8'

        arguments['geometry_unit_orientation'] = (int(front_code) - 1) * 45

        # Windows
        windows = self.h2k_parameters.get_windows_spec()
        win_area = {front_code: 0, right_code: 0, left_code: 0, back_code: 0}
        for window in windows:
            win_area[window['facingDirectionCode']
                     ] += round(window['@height']/1000 * window['@width']/1000, 1)
            # HOT2000 uses milimeter for window dimension
        arguments['window_area_back'] = win_area[back_code]
        arguments['window_area_front'] = win_area[front_code]
        arguments['window_area_left'] = win_area[left_code]
        arguments['window_area_right'] = win_area[right_code]

        # Return updated dictionary
        return arguments

    def update_systems_spec(self, arguments: dict) -> dict:
        # Temperature setpoint
        setpoints = self.h2k_parameters.get_maintemp_setpoint()
        def celsius_to_farenheit(t): return str(round(9/5 * float(t) + 32, 1))
        arguments['hvac_control_heating_weekday_setpoint'] = celsius_to_farenheit(
            setpoints['@daytimeHeatingSetPoint'])
        arguments['hvac_control_heating_weekend_setpoint'] = celsius_to_farenheit(
            setpoints['@daytimeHeatingSetPoint'])
        arguments['hvac_control_cooling_weekday_setpoint'] = celsius_to_farenheit(
            setpoints['@coolingSetPoint'])
        arguments['hvac_control_cooling_weekend_setpoint'] = celsius_to_farenheit(
            setpoints['@coolingSetPoint'])

        # Cooling System
        cooling_systems = self.h2k_parameters.get_coolingsystem_spec()
        # keys are the codes for cooling systems in HOT2000
        map_h2k_to_hpxml_cooling_system_types = {'1': 'central air conditioner',
                                                 '2': 'packaged terminal air conditioner',
                                                 '3': 'mini-split'}

        def kw_to_btu_hr(capacity): return round(float(capacity) * 3412.142, 1)

        for cooling_system in cooling_systems:
            arguments['cooling_system_cooling_capacity'] = kw_to_btu_hr(
                cooling_system['capacity'])
            arguments['cooling_system_cooling_efficiency'] = cooling_system['efficiency']
            # Check the efficiency types and update if necessary
            arguments['cooling_system_cooling_efficiency_type'] = 'SEER' if not cooling_system['isCop'] else 'EER'
            arguments['cooling_system_type'] = map_h2k_to_hpxml_cooling_system_types[cooling_system['code']]

        # Hot Water Tank
        hot_water_systems = self.h2k_parameters.get_hotwater_spec()
        water_heaters = hot_water_systems[0]
        map_h2k_fuels_to_hpxml = {
            'Electricity': 'electricity',
            'Electric': 'electricity',
            'Natural gas': 'natural gas',
            'Oil': 'fuel oil',
            'Propane': 'propane',
            'Mixed Wood': 'wood',
            'Hardwood': 'wood',
            'Softwood': 'wood',
            'Wood Pellets': 'wood'
        }
        # keys are the hpxml water heater type
        # values are the h2k water heater type
        # Currently only include H2K electric water heating system types
        # Expand the lists for other fuel types
        map_hpxml_water_heater_type_to_h2k = {
            'storage water heater': ['Conventional tank', 'Conserver tank'],
            'instantaneous water heater': ['Instantenous'],
            'heat pump water heater': ['Tankless heat pump', 'Heat pump', 'Integrated heat pump'],
            'space-heating boiler with storage tank': [],
            'space-heating boiler with tankless coil': []
        }

        def litre_to_gal(volume): return round(float(volume) * 0.26413, 0)

        for water in water_heaters:
            # Only considering primary water heater
            if water['systemtype'] == 'Primary':
                arguments['water_heater_efficiency'] = water['energyfactor']
                arguments['water_heater_efficiency_type'] = 'EnergyFactor'
                arguments['water_heater_fuel_type'] = map_h2k_fuels_to_hpxml[water['energysource']]
                arguments['water_heater_tank_volume'] = litre_to_gal(
                    water['tankvolume'])
                for hpxml_type, h2k_type in map_hpxml_water_heater_type_to_h2k.items():
                    if water['tanktype'] in h2k_type:
                        arguments['water_heater_type'] = hpxml_type
                        break

        # Heating Systems
        primary_heating_system, backup_heating_system = self.h2k_parameters.get_heating_system_spec()
        if not backup_heating_system:
            # No heat pump system
            arguments['heating_system_fuel'] = map_h2k_fuels_to_hpxml[primary_heating_system[1]['fuel']]
            arguments['heating_system_heating_capacity'] = kw_to_btu_hr(
                primary_heating_system[1]['capacity'])
            arguments['heating_system_heating_efficiency'] = primary_heating_system[1]['efficiency']
            arguments['heating_system_type'] = primary_heating_system[0] if primary_heating_system[0] != 'Baseboard' else 'ElectricResistance'
        else:
            # A heat pump exist and should be added to the HPXML file using the 'heat_pump_type' measure
            # Check the HPXML documentation to confirm
            # ----> 1. if the backup heating system should be added to the file as heating system
            # ----> 2. if cooling should be updated if the heat pump is providing cooling
            #       (There are few measures for 'heat_pump_cooling' in the measure.xml file).
            pass

        # Return updated dictionary
        return arguments
