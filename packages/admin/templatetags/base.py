from inspect import getfullargspec

from django.template.library import InclusionNode, parse_bits

class InclusionAdminNode(InclusionNode):
    