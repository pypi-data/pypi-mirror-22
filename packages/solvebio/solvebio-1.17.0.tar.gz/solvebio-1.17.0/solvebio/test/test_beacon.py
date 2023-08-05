from __future__ import absolute_import
from solvebio.resource import Dataset

from .helper import SolveBioTestCase


class BeaconTests(SolveBioTestCase):

    def test_beacon_request(self):
        """
        Check that current Clinvar/Variants returns correct
        fields for beacon
        """
        dataset = Dataset.retrieve('ClinVar/Variants')

        beacon = dataset.beacon(genome_build='GRCh37',
                                chromosome='6',
                                # coordinate=50432798,  # prod
                                coordinate=51612854,  # staging
                                allele='G')

        check_fields = ['query', 'exist', 'total']

        for f in check_fields:
            self.assertTrue(f in beacon)

        """
        Check that Clinvar/Variants version 3.7.0-2015-12-06
        returns true for specific case
        """

        dataset = Dataset.retrieve('ClinVar/3.7.0-2015-12-06/Variants')

        beacontwo = dataset.beacon(genome_build='GRCh37',
                                   chromosome='13',
                                   coordinate=113803460,
                                   allele='T')

        self.assertTrue(beacontwo['exist'])
        self.assertEqual(beacontwo['total'], 1)
