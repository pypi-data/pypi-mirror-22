"""A realm process sepecialization.

For further information goto http://wordpress.es-doc.org/cmip6-model-specializations.

"""
# --------------------------------------------------------------------
# INTERNAL (do not change)
# --------------------------------------------------------------------
from collections import OrderedDict

DETAILS = OrderedDict()
ENUMERATIONS = OrderedDict()

# --------------------------------------------------------------------
# CONTACT: Set to realm specialization co-ordinator.
# --------------------------------------------------------------------
CONTACT = 'David Hassell'

# --------------------------------------------------------------------
# AUTHORS: Set to realm specialization authors (comma delimited).
# --------------------------------------------------------------------
AUTHORS = 'David Hassell'

# --------------------------------------------------------------------
# QUALITY CONTROL STATUS: Set to 'draft' or 'complete'
# --------------------------------------------------------------------
QC_STATUS = 'draft'

# --------------------------------------------------------------------
# DESCRIPTION: Short description of the specialization.
# --------------------------------------------------------------------
DESCRIPTION = 'Land surface soil'

# --------------------------------------------------------------------
# PROCESS: top level properties
# --------------------------------------------------------------------

# --------------------------------------------------------------------
# SUB-PROCESS: Soil map
# --------------------------------------------------------------------
DETAILS['soil_map'] = {
    'description': 'Key properties of the land surface soil map',
    'properties': [
        ('description', 'str', '1.1',
             'General description of soil map'),
        ('structure', 'str', '1.1',
             'Describe the soil map structure'),
        ('texture', 'str', '1.1',
             'Describe the soil map texture'),
        ('albedo', 'str', '1.1',
             'Describe the soil map albedo'),
        ('water_table', 'str', '1.1',
             'Describe the soil map water_table'),
        ('soil_depth', 'str', '1.1',
             'Describe the soil map total soil depth'),
    ],
}

# --------------------------------------------------------------------
# SUB-PROCESS: Hydrology
# --------------------------------------------------------------------
DETAILS['hydrology'] = {
    'description': 'Key properties of the land surface soil hydrology',
    'properties': [
        ('description', 'str', '1.1',
             'General description of how soil hydrological properties are defined'),
        ('tiling', 'str', '0.1',
             'Describe the soil hydrology tiling, if any.'),
        ('number_of_ground_water_layers', 'int', '1.1',
             'The number of ground water levels used in the land surface scheme/model'),
        ('water_storage_method', 'ENUM:water_storage_method_types', '1.1',
             'Describe the method by which water is stored in the land surface scheme/model'),
    ],
    'detail_sets': [
        'freezing',
        'drainage'
        'runoff',
    ]
}

DETAILS['hydrology:freezing'] = {
    'description': 'TODO',
    'properties': [
        ('number_of_ground_ice_layers', 'int', '1.1',
            'How many ground ice layers are included in the land surface scheme'),
        ('ice_storage_method', 'str', '1.1',
            'Describe the method of ice storage'),
        ('permafrost', 'str', '1.1',
            'Describe the treatment of permafrost, if any, within the land surface scheme'),
        ]
    }

DETAILS['hydrology:drainage'] = {
    'description': 'TODO',
    'properties': [
        ('description', 'str', '1.1',
            'Describe how drainage is included in the land surface scheme'),
        ]
    }

DETAILS['hydrology:runoff'] = {
    'description': 'TODO',
    'properties': [
        ('description', 'str', '1.1',
            'Describe how runoff is included in the land surface scheme'),
        ]
    }

# --------------------------------------------------------------------
# SUB-PROCESS: Heat treatment
# --------------------------------------------------------------------
DETAILS['heat_treatment'] = {
    'description': 'TODO',
    'properties': [
        ('description', 'str', '1.1',
             'General description of how heat treatment properties are defined'),
        ('tiling', 'str', '0.1',
             'Describe the soil heat treatment tiling, if any.'),
        ('number_of_ground_heat_layers', 'int', '1.1',
            'How many ground heat layers are included in the land surface scheme'),
        ('vertical_discretisation', 'str' , '1.1',
             'Describe the typical vertical discretisation'),
        ('heat_storage', 'ENUM:heat_storage_types', '1.1',
             'Specify the method of heat storage'),
        ('processes', 'ENUM:heat_treatment_process_types', '1.N',
             'Describe processes included in the treatment of soil heat'),
    ],
}


# --------------------------------------------------------------------
# ENUMERATIONS
# --------------------------------------------------------------------
ENUMERATIONS['water_storage_method_types'] = {
    'description': 'Describe the method by which water is stored in the land surface scheme/model',
    'is_open': True,
    'members': [
        ('Bucket', None),
        ('Force-restore', None),
        ('Choisnel', None),
        ('Explicit diffusion', None),
        ]
    }

ENUMERATIONS['heat_storage_types'] = {
    'description': 'Method of heat storage',
    'is_open': True,
    'members': [
        ('Force-restore', None),
        ('Explicit diffusion', None),
        ]
    }

ENUMERATIONS['heat_treatment_process_types'] = {
    'description': 'Processes included in the treatment of soil heat',
    'is_open': True,
    'members': [
        ('soil moisture freeze-thaw', None),
        ('coupling with snow temperature', None),
        ]
    }
