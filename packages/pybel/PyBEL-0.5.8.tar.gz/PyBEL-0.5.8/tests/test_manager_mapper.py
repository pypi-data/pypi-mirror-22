# -*- coding: utf-8 -*-

import os
import unittest
from pathlib import Path

from pybel.manager import models
from tests.constants import FleetingTemporaryCacheMixin
from tests.constants import test_eq_1, test_eq_2, belns_dir_path
from tests.mocks import mock_bel_resources

ns1 = Path(os.path.join(belns_dir_path, 'disease-ontology.belns')).as_uri()
ns1_eq = Path(test_eq_1).as_uri()
ns1_url = 'http://resources.openbel.org/belframework/20150611/namespace/disease-ontology-ids.belns'

ns2 = Path(os.path.join(belns_dir_path, 'mesh-diseases.belns')).as_uri()
ns2_eq = Path(test_eq_2).as_uri()
ns2_url = 'http://resources.openbel.org/belframework/20150611/namespace/mesh-diseases.belns'


@unittest.skip('Need to fix cascades and deleting for foreign keys')
class TestMapperManager(FleetingTemporaryCacheMixin):
    def tearDown(self):
        self.manager.drop_equivalences()

        super(TestMapperManager, self).tearDown()

    @mock_bel_resources
    def test_make_eq_class(self, mock_get):
        cl = self.manager.ensure_equivalence_class('XXXX')
        self.assertIsInstance(cl, models.NamespaceEntryEquivalence)
        self.assertEqual('XXXX', cl.label)

    @mock_bel_resources
    def test_insert(self, mock_get):
        self.manager.ensure_namespace(ns1)

        ns = self.manager.session.query(models.Namespace).filter_by(url=ns1).one()
        self.assertFalse(ns.has_equivalences)

        self.manager.insert_equivalences(Path(test_eq_1).as_uri(), ns1)

        ns = self.manager.session.query(models.Namespace).filter_by(url=ns1).one()
        self.assertTrue(ns.has_equivalences)

    @mock_bel_resources
    def test_ensure_twice(self, mock_get):
        """No errors should get thrown when ensuring twice"""
        self.manager.ensure_equivalences(ns1_eq, ns1)

    @mock_bel_resources
    def test_disease_equivalence(self, mock_get):
        """Tests that the disease label and ID map to the same equivalence class"""
        alz_eq_class = '0b20937b-5eb4-4c04-8033-63b981decce7'

        self.manager.ensure_equivalences(ns1_eq, ns1)
        x = self.manager.get_equivalence_by_entry(ns1, "Alzheimer's disease")
        self.assertEqual(alz_eq_class, x.label)

        self.manager.ensure_equivalences(ns2_eq, ns2)
        y = self.manager.get_equivalence_by_entry(ns2, "Alzheimer Disease")
        self.assertEqual(alz_eq_class, y.label)

        members = self.manager.get_equivalence_members(alz_eq_class)

        self.assertEqual({
            ns1: "Alzheimer's disease",
            ns2: "Alzheimer Disease"
        }, {member.namespace.url: member.name for member in members})


if __name__ == '__main__':
    unittest.main()
