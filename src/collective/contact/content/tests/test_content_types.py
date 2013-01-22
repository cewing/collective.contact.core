# -*- coding: utf8 -*-

import unittest2 as unittest

import datetime

from ecreall.helpers.testing.base import BaseTest

from collective.contact.content.testing import INTEGRATION


class TestContentTypes(unittest.TestCase, BaseTest):
    """Base class to test new content types"""

    layer = INTEGRATION

    def setUp(self):
        super(TestContentTypes, self).setUp()
        self.portal = self.layer['portal']
        self.mydirectory = self.portal['mydirectory']
        self.degaulle = self.mydirectory['degaulle']
        self.pepper = self.mydirectory['pepper']
        self.armeedeterre = self.mydirectory['armeedeterre']
        self.corpsa = self.armeedeterre['corpsa']
        self.corpsb = self.armeedeterre['corpsb']
        self.divisionalpha = self.corpsa['divisionalpha']
        self.regimenth = self.divisionalpha['regimenth']
        self.brigadelh = self.regimenth['brigadelh']
        self.general_adt = self.armeedeterre['general_adt']
        self.adt = self.degaulle['adt']
        self.gadt = self.degaulle['gadt']
        self.sergent_pepper = self.pepper['sergent_pepper']


class TestDirectory(TestContentTypes):

    def test_directory(self):
        self.assertIn('mydirectory', self.portal)
        mydirectory = self.portal['mydirectory']
        self.assertEqual('Military directory', mydirectory.Title())
        self.assertIn({'name': 'Colonel', 'token': 'colonel'},
                      mydirectory.position_types)
        self.assertIn({'name': 'Air force', 'token': 'air_force'},
                      mydirectory.organization_types)
        self.assertIn({'name': 'Regiment', 'token': 'regiment'},
                      mydirectory.organization_levels)


class TestPerson(TestContentTypes):

    def test_person(self):
        self.assertIn('degaulle', self.mydirectory)
        degaulle = self.degaulle
        self.assertEqual('Général Charles De Gaulle', degaulle.Title())
        self.assertEqual('De Gaulle', degaulle.lastname)
        self.assertEqual('Charles', degaulle.firstname)
        self.assertEqual(datetime.date(1901, 11, 22), degaulle.birthday)

    def test_no_firstname(self):
        pepper = self.mydirectory['pepper']
        self.assertEqual('Sergent Pepper', pepper.Title())

    def test_no_person_title(self):
        rambo = self.mydirectory['rambo']
        self.assertEqual('John Rambo', rambo.Title())
        # we can't create persons in portal
        with self.assertRaises(ValueError):
            self.portal.invokeFactory('person', 'error',
                                      {'lastname': "Casper"})


class TestOrganization(TestContentTypes):

    def test_organization(self):
        armeedeterre = self.armeedeterre
        self.assertIn('armeedeterre', self.mydirectory)
        self.assertEqual(armeedeterre.Title(), "Armée de terre")
        self.assertIn('corpsa', armeedeterre)
        self.assertIn('corpsb', armeedeterre)
        self.assertIn('divisionalpha', self.corpsa)
        self.assertIn('divisionbeta', self.corpsa)
        self.assertIn('regimenth', self.divisionalpha)
        self.assertIn('brigadelh', self.regimenth)
        self.assertIn('armeedeterre',
                      self.divisionalpha.getPhysicalPath())
        self.assertIn('armeedeterre',
                      self.brigadelh.getPhysicalPath())

    def test_get_organizations_chain(self):
        armeedeterre = self.armeedeterre
        corpsa = self.corpsa
        divisionalpha = self.divisionalpha
        self.assertEqual([armeedeterre],
                         self.armeedeterre.get_organizations_chain())
        self.assertEqual([armeedeterre, corpsa, divisionalpha],
                         self.divisionalpha.get_organizations_chain())

    def test_get_root_organization(self):
        armeedeterre = self.armeedeterre
        organizations = [armeedeterre, self.corpsa, self.corpsb,
                         self.divisionalpha, self.regimenth, self.brigadelh]
        for org in organizations:
            self.assertEqual(armeedeterre,
                             org.get_root_organization())

    def test_get_organizations_titles(self):

        corpsa_titles = self.corpsa.get_organizations_titles()
        self.assertIn('Armée de terre', corpsa_titles)
        self.assertIn('Corps A', corpsa_titles)

        division_alpha_titles = self.divisionalpha.get_organizations_titles()
        self.assertIn('Armée de terre', division_alpha_titles)
        self.assertIn('Corps A', division_alpha_titles)
        self.assertIn('Division Alpha', division_alpha_titles)

        brigadelh_titles = self.brigadelh.get_organizations_titles()
        self.assertIn('Armée de terre', brigadelh_titles)
        self.assertIn('Corps A', brigadelh_titles)
        self.assertIn('Division Alpha', brigadelh_titles)
        self.assertIn('Régiment H', brigadelh_titles)
        self.assertIn('Brigade LH', brigadelh_titles)

    def test_get_full_title(self):
        self.assertEqual(self.armeedeterre.get_full_title(),
                         "Armée de terre")
        self.assertEqual(self.brigadelh.get_full_title(),
                         "Armée de terre / Corps A / Division Alpha / Régiment H / Brigade LH")


class TestPosition(TestContentTypes):

    def test_position(self):
        self.assertIn('general_adt', self.armeedeterre)
        general_adt = self.general_adt
        self.assertEqual(general_adt.Title(),
                         "Général de l'armée de terre")
        self.assertEqual(general_adt.position_type,
                         'general')

    def test_get_full_title(self):
        self.assertEqual(self.general_adt.get_full_title(),
                         "Général de l'armée de terre (Armée de terre)")


class TestHeldPosition(TestContentTypes):

    def test_held_position(self):
        degaulle = self.degaulle
        adt = self.adt
        gadt = self.gadt
        pepper = self.pepper
        sergent_pepper = self.sergent_pepper
        self.assertIn('adt', degaulle)
        self.assertEqual(adt.Title(),
                         "Armée de terre")
        self.assertIn('gadt', degaulle)
        self.assertEqual(gadt.Title(),
                         "Général de l'armée de terre")
        self.assertIn('sergent_pepper', pepper)
        self.assertEqual(sergent_pepper.Title(),
                         "Sergent de la brigade LH")

    def test_get_full_title(self):
        self.assertEqual(self.adt.get_full_title(),
                         "Général Charles De Gaulle (Armée de terre)")
        self.assertEqual(self.gadt.get_full_title(),
                         "Général Charles De Gaulle (Armée de terre - Général de l'armée de terre)")
        self.assertEqual(self.sergent_pepper.get_full_title(),
                         "Sergent Pepper (Armée de terre - Sergent de la brigade LH)")

    def test_get_person(self):
        pass

    def test_get_position(self):
        pass

    def test_get_organization(self):
        pass
