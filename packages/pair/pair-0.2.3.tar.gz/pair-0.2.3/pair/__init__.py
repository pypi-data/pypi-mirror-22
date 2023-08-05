"""
pair
~~~~

A ladder/tournament pairing library using Kuhn-Munkres

"""

__version__ = '0.2.3'
__author__ = 'knyte'

from .match import pair_teams, pair_players, group_teams, group_players, assign_templates
