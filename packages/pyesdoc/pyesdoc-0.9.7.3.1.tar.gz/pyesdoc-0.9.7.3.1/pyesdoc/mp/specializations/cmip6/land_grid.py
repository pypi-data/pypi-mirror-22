"""A realm grid sepecialization.

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
DESCRIPTION = 'Land surface grid'

# --------------------------------------------------------------------
# DISCRETISATION: Description of the numerics of the discretisation.
# --------------------------------------------------------------------
DETAILS['horizontal'] = {
    'description': 'The horizontal grid in the land surface',
    'properties': [
        ('description', 'str', '1.1',
             'Describe the general structure of the horizontal grid (not including any tiling)'),
        ('matches_atmosphere_grid', 'bool', '1.1',
             'Does the horizontal grid match the atmpsphere?'),
        ]
    }

DETAILS['vertical'] = {
    'description': 'The vertical grid in the soil',
    'properties': [
        ('description', 'str', '1.1',
             'Describe the general structure of the  vertical grid in the soil (not including any tiling)'),
        ('number_of_levels', 'int', '1.1',
             'The total number of vertical levels in the soil'),
        ]
    }

# --------------------------------------------------------------------
# ENUMERATIONS
# --------------------------------------------------------------------
