from django.core.management import call_command
from django.test import TestCase

from arenas.models import Location


class CommandsTestCase(TestCase):
    def test_get_or_create_location_when_db_is_empty(self):
        args = ('PL Mazowieckie Warszawa',)
        call_command('get_or_create_location', *args)
        records_number = Location.objects.all().count()

        root_qs = Location.objects.filter(parent=None, identifier='root')
        country_qs = Location.objects.filter(identifier="{PL}")
        region_qs = Location.objects.filter(identifier="{PL}.{Mazowieckie}")
        city_qs = Location.objects.filter(identifier="{PL}.{Mazowieckie}.{Warszawa}")

        self.assertEqual(records_number, 4)
        self.assertTrue(root_qs.exists())
        self.assertTrue(country_qs.exists())
        self.assertTrue(region_qs.exists())
        self.assertTrue(city_qs.exists())
        self.assertEqual(root_qs.first().parent, None)
        self.assertEqual(country_qs.first().parent, root_qs.first())
        self.assertEqual(region_qs.first().parent, country_qs.first())
        self.assertEqual(city_qs.first().parent, region_qs.first())
    
    def test_create_location_from_empty_list(self):
        args = ('',)
        call_command('get_or_create_location', *args)
        records_number = Location.objects.all().count()

        self.assertEqual(records_number, 1)
        self.assertTrue(Location.objects.filter(parent=None, identifier='root').exists())
    
    def test_dont_create_duplicate_location(self):
        root = Location.objects.create(parent=None, identifier='root')
        country = Location.objects.create(parent=root, identifier='{PL}')
        region = Location.objects.create(parent=country, identifier='{PL}.{Pomorskie}')
        city = Location.objects.create(parent=region, identifier='{PL}.{Pomorskie}.{Gdańsk}')
        district = Location.objects.create(parent=city, identifier='{PL}.{Pomorskie}.{Gdańsk}.{Przymorze}')

        args = ('PL Pomorskie Gdańsk Przymorze Chłopska_34B/43',)
        call_command('get_or_create_location', *args)
        records_number = Location.objects.all().count()

        self.assertEqual(records_number, 6)
        self.assertTrue(Location.objects.filter(parent=district, identifier='{PL}.{Pomorskie}.{Gdańsk}.{Przymorze}.{Chłopska_34B/43}').exists())


