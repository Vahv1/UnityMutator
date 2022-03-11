import typing
from dataclasses import dataclass

@dataclass
class MutationOperator:
    """Class for mutation operator data"""
    name: str
    syntax: [str]
    # TODO this should use function class instead of str, find out how
    function: typing.Any

