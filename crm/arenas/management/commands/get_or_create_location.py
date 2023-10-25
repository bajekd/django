from typing import List, Tuple, Union

from django.core.management import BaseCommand

from arenas.models import Location
import pdb


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('identifier', type=str)
    
    def _get_or_create_location(self, locations: List[str]) -> Tuple[Location, bool]:
        if not locations:
            return Location.objects.get_or_create(parent=None, identifier='root')

        identifier: Union[List[str], str] = list(map(lambda elem: '{' + elem + '}', locations)) # f"{({elem})}" without parentheses don't work, but with parentheses produce {'PL'}.{'Mazowieckie'}
        identifier = '.'.join(identifier)

        if len(locations) == 1:
            parent, _ = Location.objects.get_or_create(parent=None, identifier='root')
        else:
            parent, _ = self._get_or_create_location(locations[:-1])
        
        return Location.objects.get_or_create(parent=parent, identifier=identifier)

    def handle(self, *args, **kwargs):
        identifier: str = kwargs['identifier']
        locations: List[str] = identifier.split()
           
        self._get_or_create_location(locations)
        
        




