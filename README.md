# Note that this repository has been superceded by the h2k_hpxml project (link below) and exists only for reference purposes

Refer to the [h2k_hpxml](https://github.com/canmet-energy/h2k_hpxml) project.

# HOT2000 hourly model constructor using HPXML

This initiative aims to develop a workflow to generate hourly energy modeling results for H2K archetypes. EnergyPlus is selected as the hourly energy modeling software for this project. The proposed workflow involves scripts to parse H2K models, transform model parameters to e+ input format, generate e+ models, execute the hourly simulation, and return the hourly results. 
NREL’s HPXML tool will be adopted and adapted to build this workflow. OpenStudio-HPXML allows running residential EnergyPlus simulations using an HPXML file for the building description. OpenStudio-HPXML can accommodate a wide range of different building technologies and geometries. End-to-end simulations typically run in 3-10 seconds depending on complexity, computer platform, speed, etc.

Refer to the [HPXML GitHub repository](https://github.com/NREL/OpenStudio-HPXML) to learn more about the HPXML platform.

## Installation

It is recommended to create a [virtual environment](https://docs.python.org/3/tutorial/venv.html) to install the requirements and the hpxml package in the development mode. To create a virtual environment, decide upon a directory where you want to place it, and run the [`venv`](https://docs.python.org/3/library/venv.html#module-venv) module as a script with the directory path.

```powershell
git clone <git-repository-url>                     # Download the repository from GitHub
cd h2k_to_hpxml
python3 -m venv hpxml-env                          # Create empty virtual environment
pip install -r requirements.txt                    # Install packages listed in requirements.txt
pip install -e .                                   # Install the hpxml package in development mode
```

We can install the local hpxml package in [development mode](https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs); the option `-e`, standing for `--editable`, installs the package in [development mode](https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs), that is, [using a symlink](http://python-packaging.readthedocs.io/en/latest/minimal.html#creating-the-scaffolding) to the local hpxml folder so that package can be developed while it is installed. The `.` is used to indicate the folder where [`setup.py`](https://github.com/FilippoBovo/production-data-science/blob/master/tutorial/a-setup/setup.py) is.

The [`requirements.txt`](https://github.com/FilippoBovo/production-data-science/blob/master/tutorial/b-collaborate/requirements.txt) contains the list of packages in the virtual environment. The file can be updated when a new package is added to the environment using:

```
pip freeze | grep -v src > requirements.txt
```

The `grep -v src` command omits the local package to avoid errors when installing packages from the requirement file.

## Instruction

Two main modules are currently developed in this package:

1. ####  [h2kparser.py](https://github.com/canmet-energy/h2k_to_hpxml/blob/main/src/h2kparser.py)

The `h2kparser.py` module contains the `ParseH2K` class to parse H2K files, extract the data, and return the specifications of the H2K through its methods. The list of methods are shown below. 

```python
[('__init__',  <function __main__.ParseH2K.__init__(self, h2k_file: str, schema_file: str) -> None>),
 ('__str__', <function __main__.ParseH2K.__str__(self) -> str>),
 ('extract_this_basement', <function __main__.ParseH2K.extract_this_basement(self, bsmt)>),
 ('extract_this_door', <function __main__.ParseH2K.extract_this_door(self, door, parent_id, parent_label, parent_type)>),
 ('extract_this_header', <function __main__.ParseH2K.extract_this_header(self, header, parent_id, parent_label, parent_type)>),
 ('extract_this_window', <function __main__.ParseH2K.extract_this_window(self, window, parent_id, parent_label, parent_type)>),
 ('get_base_loads', <function __main__.ParseH2K.get_base_loads(self) -> dict>),
 ('get_basement_fraction_internalgains', <function __main__.ParseH2K.get_basement_fraction_internalgains(self) -> float>),
 ('get_basement_spec', <function __main__.ParseH2K.get_basement_spec(self)>),
 ('get_basement_temp_setpoint', <function __main__.ParseH2K.get_basement_temp_setpoint(self) -> dict>),
 ('get_ceiling_spec', <function __main__.ParseH2K.get_ceiling_spec(self)>),
 ('get_climate_Prov', <function __main__.ParseH2K.get_climate_Prov(self) -> str>),
 ('get_climate_city', <function __main__.ParseH2K.get_climate_city(self) -> str>),
 ('get_coolingsystem_spec', <function __main__.ParseH2K.get_coolingsystem_spec(self)>),
 ('get_crawlspace_setpoint', <function __main__.ParseH2K.get_crawlspace_setpoint(self) -> dict>),
 ('get_doors_spec', <function __main__.ParseH2K.get_doors_spec(self)>),
 ('get_equipment_setpoint', <function __main__.ParseH2K.get_equipment_setpoint(self) -> dict>),
 ('get_exposed_floor', <function __main__.ParseH2K.get_exposed_floor(self)>),
 ('get_facing_direction', <function __main__.ParseH2K.get_facing_direction(self) -> dict>),
 ('get_file_id', <function __main__.ParseH2K.get_file_id(self) -> str>),
 ('get_floor_header', <function __main__.ParseH2K.get_floor_header(self)>),
 ('get_flue_shielding', <function __main__.ParseH2K.get_flue_shielding(self) -> dict>),
 ('get_gableend_area', <function __main__.ParseH2K.get_gableend_area(self) -> float>),
 ('get_gableend_exteriormaterial', <function __main__.ParseH2K.get_gableend_exteriormaterial(self) -> dict>),
 ('get_gableend_sheating', <function __main__.ParseH2K.get_gableend_sheating(self) -> dict>),
 ('get_hdd_frostdepth', <function __main__.ParseH2K.get_hdd_frostdepth(self) -> dict>),
 ('get_heated_area', <function __main__.ParseH2K.get_heated_area(self) -> dict>),
 ('get_heating_system_spec', <function __main__.ParseH2K.get_heating_system_spec(self)>),
 ('get_heating_system_type1', <function __main__.ParseH2K.get_heating_system_type1(self, systems)>),
 ('get_heating_system_type2', <function __main__.ParseH2K.get_heating_system_type2(self, systems)>),
 ('get_hotwater_spec', <function __main__.ParseH2K.get_hotwater_spec(self)>),
 ('get_house_type', <function __main__.ParseH2K.get_house_type(self) -> dict>),
 ('get_house_volume', <function __main__.ParseH2K.get_house_volume(self) -> float>),
 ('get_hrv', <function __main__.ParseH2K.get_hrv(self)>),
 ('get_infiltration', <function __main__.ParseH2K.get_infiltration(self) -> dict>),
 ('get_mainallowed_temp_rise', <function __main__.ParseH2K.get_mainallowed_temp_rise(self) -> float>),
 ('get_maintemp_setpoint', <function __main__.ParseH2K.get_maintemp_setpoint(self) -> dict>),
 ('get_n_rooms', <function __main__.ParseH2K.get_n_rooms(self) -> dict>),
 ('get_n_storey', <function __main__.ParseH2K.get_n_storey(self) -> dict>),
 ('get_occupancy_adult', <function __main__.ParseH2K.get_occupancy_adult(self) -> dict>),
 ('get_occupancy_children', <function __main__.ParseH2K.get_occupancy_children(self) -> dict>),
 ('get_occupancy_infants', <function __main__.ParseH2K.get_occupancy_infants(self) -> dict>),
 ('get_plan_type', <function __main__.ParseH2K.get_plan_type(self) -> dict>),
 ('get_roofcavity_spec', <function __main__.ParseH2K.get_roofcavity_spec(self) -> dict>),
 ('get_site_terrain', <function __main__.ParseH2K.get_site_terrain(self) -> dict>),
 ('get_supplement_ventilation', <function __main__.ParseH2K.get_supplement_ventilation(self)>),
 ('get_thermal_mass', <function __main__.ParseH2K.get_thermal_mass(self) -> dict>),
 ('get_vent_distribution_fan', <function __main__.ParseH2K.get_vent_distribution_fan(self) -> dict>),
 ('get_vent_distribution_operation', <function __main__.ParseH2K.get_vent_distribution_operation(self) -> dict>),
 ('get_vent_distribution_type', <function __main__.ParseH2K.get_vent_distribution_type(self) -> dict>),
 ('get_version', <function __main__.ParseH2K.get_version(self) -> dict>),
 ('get_vintage', <function __main__.ParseH2K.get_vintage(self) -> int>),
 ('get_walls_shielding', <function __main__.ParseH2K.get_walls_shielding(self) -> dict>),
 ('get_walls_spec', <function __main__.ParseH2K.get_walls_spec(self)>),
 ('get_windows_spec', <function __main__.ParseH2K.get_windows_spec(self)>),
 ('slice_dict_by_key', <function __main__.ParseH2K.slice_dict_by_key(input_dict: dict, keys_to_extract: list) -> dict>)]
```

The class parameters include:

-  `h2k_file`: path to the h2k file
- `schema_file`: path to the `h2k schema.xsd` file

Note that the class instructor checks for the validity of schema and H2K file. If the files are not compatible it will raise an assertion error.



2. #### [hpxml_builder.py](https://github.com/canmet-energy/h2k_to_hpxml/blob/main/src/hpxml_builder.py)

The `BuildHPXML` class in this module is developed to create an hpxml workflow for each h2k file. The class parameters include:

-  `path_to_hpxml_template`: path to the hpxml workflow template; see [here](https://github.com/NREL/OpenStudio-HPXML/tree/master/workflow) for additional information
- `path_to_h2k`: path to the h2k file
- `path_to_h2k_schema`: path to the `h2k schema.xsd` file

```python
[('__init__', <function __main__.BuildHPXML.__init__(self, path_to_hpxml_template: str, path_to_h2k: str, path_to_h2k_schema: str) -> None>),
 ('_read_json', <function __main__.BuildHPXML._read_json(self, path: str) -> dict>),
 ('update_envelope_spec', <function __main__.BuildHPXML.update_envelope_spec(self, arguments: dict) -> dict>),
 ('update_run_directory', <function __main__.BuildHPXML.update_run_directory(self, path_to_run_directory: str) -> None>),
 ('update_steps', <function __main__.BuildHPXML.update_steps(self)>),
 ('update_systems_spec', <function __main__.BuildHPXML.update_systems_spec(self, arguments: dict) -> dict>)]
```

The class initiator creates an object of the ParseH2K class. This object will be used to get the specifications of the H2K file. The `update_steps` method updates the hpxml workflow file based on the H2K data. 



***Example:***

This example provides the code syntax and Python outputs of the `ParseH2K` class. Navigate to the `src` directory and launch interactive python in the PowerShell environment. 

```powershell
PS C:\h2k_to_hpxml\src> ipython
Python 3.7.0 (v3.7.0:1bf9cc5093, Jun 27 2018, 04:59:51) [MSC v.1914 64 bit (AMD64)]
Type 'copyright', 'credits' or 'license' for more information
IPython 7.28.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]:

```

Provide the path to an H2K file and corresponding schema file and initialize an object of the class:

```python
In [1]: %run h2kparser.py

In [2]: h2k_schema = f'C:\h2k_to_hpxml\schemas\h2k\H2k Schema.xsd'

In [3]: h2k_file = f'C:\h2k_to_hpxml\exploration\data\h2k\ERS-1032.H2K'

In [4]: parser = ParseH2K(h2k_file, h2k_schema)
    
In [5]: parser.get_heating_system_spec()
Out[5]:
(('Baseboards',
  defaultdict(None,
              {'efficiency': Decimal('1'),
               'capacity': Decimal('4.5'),
               'fuel': 'Electric',
               'equipment': 'Baseboard'})),
 None)

In [6]: parser.get_n_rooms()
Out[6]:
{'@bathrooms': 1,
 '@bedrooms': 2,
 '@living': 3,
 '@otherHabitable': 0,
 '@utility': 1}
```



## Structure

The project structure is briefly described below.

```
├── LICENSE
├── .github
│   ├── workflows      <- GitHub actions workflow
├── README.md          <- The top-level README for developers using this project.
├── exploration
│   ├── data           <- Data used for the development, mostly H2K files.
│   ├── notebooks      <- Jupyter notebooks used for testing new ideas.
│   └── transfer       <- legacy code transfered to this project.
│
├── schemas            <- A default Sphinx project; see sphinx-doc.org for details
│   ├── h2k            <- HOT2000 schema; The schema associated with the version 
│   │                     of HOT2000 used for creating the H2k files should be used.
│   │                     H2K schemas can be found in the Schemas directory in 
│   │                     Hot2000 installation directory.
│   └── hpxml          <- HPXML schema.
│
├── tests              <- PyTest files for the project
│
├── .gitignore         <- list of files to omit from remote branch
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
├── src                <- Source code for use in this project.
│   ├── __init__.py    <- Makes src a Python module
│   │
│   ├── h2kparser.py   <- Script to parse H2K files and collect the required data
│   └── hpxml_builder.py<- Scripts to generate the hpxml workflow file for each H2K file
│
└── setup.cfg          <- Confiuration file to tell Python to use PyTest for testing
```

# License

Unless otherwise noted, the source code of this project is covered under Crown Copyright, Government of Canada, and is distributed under the [GNU GPL v2 License](https://github.com/canmet-energy/h2k_to_hpxml/blob/main/LICENSE).
