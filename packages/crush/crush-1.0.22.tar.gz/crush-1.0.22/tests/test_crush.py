# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2017 <contact@redhat.com>
#
# Author: Loic Dachary <loic@dachary.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import logging
import pytest # noqa needed for caplog

from crush import Crush

logging.getLogger('crush').setLevel(logging.DEBUG)


class TestCrush(object):

    def build_crushmap(self):
        crushmap = {
            "trees": [
                {
                    "type": "root",
                    "id": -1,
                    "name": "dc1",
                    "children": [],
                }
            ],
            "rules": {
                "data": [
                    ["take", "dc1"],
                    ["chooseleaf", "firstn", 0, "type", "host"],
                    ["emit"]
                ],
            }
        }
        crushmap['trees'][0]['children'].extend([
            {
                "type": "host",
                "id": -(i + 2),
                "name": "host%d" % i,
                "children": [
                    {"id": (2 * i), "name": "device%02d" % (2 * i), "weight": 1.0},
                    {"id": (2 * i + 1), "name": "device%02d" % (2 * i + 1), "weight": 2.0},
                ],
            } for i in range(0, 10)
        ])
        return crushmap

    def test_map(self):
        crushmap = self.build_crushmap()
        c = Crush(verbose=1)
        assert c.parse(crushmap)
        assert len(c.map(rule="data", value=1234, replication_count=1,
                         weights={}, choose_args=[])) == 1

    def test_get_item_by_(self):
        crushmap = self.build_crushmap()
        c = Crush(verbose=1)
        assert c.parse(crushmap)
        assert c.get_item_by_id(-2)['name'] == 'host0'
        assert c.get_item_by_name('host0')['id'] == -2

    def test_convert_to_crushmap(self, caplog):
        crushmap = {}
        assert crushmap == Crush._convert_to_crushmap(crushmap)
        crushmap = Crush._convert_to_crushmap("tests/sample-crushmap.json")
        assert 'trees' in crushmap
        crushmap = Crush._convert_to_crushmap("tests/sample-ceph-crushmap.txt")
        assert 'trees' in crushmap
        crushmap = Crush._convert_to_crushmap("tests/sample-ceph-crushmap.crush")
        assert 'trees' in crushmap
        crushmap = Crush._convert_to_crushmap("tests/sample-ceph-crushmap.json")
        assert 'trees' in crushmap
        with pytest.raises(ValueError) as e:
            crushmap = Crush._convert_to_crushmap("tests/sample-bugous-crushmap.json")
        assert "Expecting property name" in str(e.value)

    def test_parse_weights_file(self):

        # Test Simple weights file
        weights = Crush.parse_weights_file(open("tests/ceph/weights.json"))
        assert weights == {"osd.0": 0.0, "osd.2": 0.5}

        # Test OSDMap
        weights = Crush.parse_weights_file(open("tests/ceph/osdmap.json"))
        assert weights == {"osd.0": 1.0, "osd.1": 0.95, "osd.2": 1.0}

        with pytest.raises(AssertionError):
            Crush.parse_weights_file(open("tests/ceph/weights-notfloat.json"))
        with pytest.raises(AssertionError):
            Crush.parse_weights_file(open("tests/ceph/osdmap-invalid.json"))
        with pytest.raises(AssertionError):
            Crush.parse_weights_file(open("tests/sample-ceph-crushmap.txt"))

# Local Variables:
# compile-command: "cd .. ; tox -e py27 -- -s -vv tests/test_crush.py"
# End:
