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
from __future__ import division

import argparse
import copy
import collections
import logging
import textwrap
import pandas as pd
import numpy as np

from crush import Crush

log = logging.getLogger(__name__)


class Analyze(object):

    def __init__(self, args, hooks):
        self.args = args
        self.hooks = hooks

    @staticmethod
    def get_parser():
        parser = argparse.ArgumentParser(
            add_help=False,
            conflict_handler='resolve',
        )
        replication_count = 3
        parser.add_argument(
            '--replication-count',
            help=('number of devices to map (default: %d)' % replication_count),
            type=int,
            default=replication_count)
        parser.add_argument(
            '--rule',
            help='the name of rule')
        parser.add_argument(
            '--type',
            help='override the type of bucket shown in the report')
        parser.add_argument(
            '--crushmap',
            help='path to the crushmap file')
        parser.add_argument(
            '-w', '--weights',
            help='path to the weights file')
        values_count = 100000
        parser.add_argument(
            '--values-count',
            help='repeat mapping (default: %d)' % values_count,
            type=int,
            default=values_count)
        return parser

    @staticmethod
    def set_parser(subparsers, arguments):
        parser = Analyze.get_parser()
        arguments(parser)
        subparsers.add_parser(
            'analyze',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=textwrap.dedent("""\
            Analyze a crushmap

            Map a number of objects (--values-count) to devices (three
            by default or --replication-count if specified) using a
            crush rule (--rule) from a given crushmap (--crushmap) and
            display a report comparing the expected and the actual
            object distribution.

            The format of the crushmap file specified with --crushmap
            can either be:

            - a JSON representation of a crushmap as documented in the
              Crush.parse_crushmap() method

            - a Ceph binary, text or JSON crushmap compatible with
              Luminuous and below

            The --type argument changes the item type displayed in the
            report. For instance --type device shows the individual
            OSDs and --type host shows the machines that contain
            them. If --type is not specified, it defaults to the
            "type" argument of the first "choose*" step of the rule
            selected by --rule.

            The first item in the report will be the first to become
            full. For instance if the report starts with:

                    ~id~  ~weight~  ~objects~  ~over/under used %~
            ~name~
            g9       -22  2.29             85                10.40

            it means that the bucket g9 with id -22 and weight 2.29
            will be the first bucket of its type to become full. The
            actual usage of the host will be 10.4% over the expected
            usage, i.e. if the g9 host is expected to be 70%
            full, it will actually be 80.40% full.

            The ~over/under used %~ is the variation between the
            expected item usage and the actual item usage. If it is
            positive the item is overused, if it is negative the item
            is underused. For more information about why this happens
            see http://tracker.ceph.com/issues/15653#detailed-explanation

            """),
            epilog=textwrap.dedent("""
            Examples:

            Display the first host that will become full.

            $ crush analyze --values-count 100 --rule data \\
                            --crushmap tests/sample-crushmap.json
                    ~id~  ~weight~  ~objects~  ~over/under used %~
            ~name~
            host2     -4       1.0         70                  5.0
            host0     -2       1.0         65                 -2.5
            host1     -3       1.0         65                 -2.5

            Display the first device that will become full.

            $ crush analyze --values-count 100 --rule data \\
                            --type device \\
                            --crushmap tests/sample-crushmap.json
                     ~id~  ~weight~  ~objects~  ~over/under used %~
            ~name~
            device0     0       1.0         28                26.00
            device4     4       1.0         24                 8.00
            device5     5       2.0         46                 3.50
            device3     3       2.0         44                -1.00
            device2     2       1.0         21                -5.50
            device1     1       2.0         37               -16.75
            """),
            help='Analyze crushmaps',
            parents=[parser],
        ).set_defaults(
            func=Analyze,
        )

    @staticmethod
    def collect_paths(children, path):
        children_info = []
        for child in children:
            child_path = copy.copy(path)
            child_path[child.get('type', 'device')] = child['name']
            children_info.append(child_path)
            if child.get('children'):
                children_info.extend(Analyze.collect_paths(child['children'], child_path))
        return children_info

    @staticmethod
    def collect_item2path(children):
        paths = Analyze.collect_paths(children, collections.OrderedDict())
        item2path = {}
        for path in paths:
            elements = list(path.values())
            item2path[elements[-1]] = elements
        return item2path

    @staticmethod
    def collect_dataframe(crush, child):
        paths = Analyze.collect_paths([child], collections.OrderedDict())
        #
        # verify all paths have bucket types in the same order in the hierarchy
        # i.e. always rack->host->device and not host->rack->device sometimes
        #
        key2pos = {}
        pos2key = {}
        for path in paths:
            keys = list(path.keys())
            for i in range(len(keys)):
                key = keys[i]
                if key in key2pos:
                    assert key2pos[key] == i
                else:
                    key2pos[key] = i
                    pos2key[i] = key
        columns = []
        for pos in sorted(pos2key.keys()):
            columns.append(pos2key[pos])
        rows = []
        for path in paths:
            row = []
            for column in columns:
                element = path.get(column, np.nan)
                row.append(element)
                if element is not np.nan:
                    item_name = element
            item = crush.get_item_by_name(item_name)
            rows.append([item['id'],
                         item_name,
                         item.get('weight', 1.0),
                         item.get('type', 'device')] + row)
        d = pd.DataFrame(rows, columns=['~id~', '~name~', '~weight~', '~type~'] + columns)
        return d.set_index('~name~')

    @staticmethod
    def collect_nweight(d):
        d['~nweight~'] = 0.0
        for type in d['~type~'].unique():
            tw = float(d.loc[d['~type~'] == type, ['~weight~']].sum())
            d.loc[d['~type~'] == type, ['~nweight~']] = d['~weight~'].apply(lambda w: w / tw)
        return d

    @staticmethod
    def collect_usage(d, total_objects):
        capacity = d['~nweight~'] * float(total_objects)
        d['~over/under used %~'] = 0.0
        for type in d['~type~'].unique():
            usage = d['~objects~'] / capacity - 1.0
            d.loc[d['~type~'] == type, ['~over/under used %~']] = usage * 100
        return d

    @staticmethod
    def find_take(children, item):
        for child in children:
            if child.get('name') == item:
                return child
            found = Analyze.find_take(child.get('children', []), item)
            if found:
                return found
        return None

    @staticmethod
    def analyze_rule(rule):
        take = None
        failure_domain = None
        for step in rule:
            if step[0] == 'take':
                assert take is None
                take = step[1]
            elif step[0].startswith('choose'):
                assert failure_domain is None
                (op, firstn_or_indep, num, _, failure_domain) = step
        return (take, failure_domain)

    def analyze(self):
        c = Crush(verbose=self.args.verbose,
                  backward_compatibility=self.args.backward_compatibility)
        c.parse(self.crushmap)

        if self.args.weights:
            with open(self.args.weights) as f_weights:
                weights = c.parse_weights_file(f_weights)
        else:
            weights = None

        crushmap = c.get_crushmap()
        trees = crushmap.get('trees', [])
        (take, failure_domain) = self.analyze_rule(crushmap['rules'][self.args.rule])
        if self.args.type:
            type = self.args.type
        else:
            type = failure_domain
        root = self.find_take(trees, take)
        log.debug("root = " + str(root))
        d = self.collect_dataframe(c, root)
        d = self.collect_nweight(d)

        replication_count = self.args.replication_count
        rule = self.args.rule
        device2count = collections.defaultdict(lambda: 0)
        values = self.hooks.hook_create_values()
        for (name, value) in values.items():
            m = c.map(rule, value, replication_count, weights)
            log.debug("{} == {} mapped to {}".format(name, value, m))
            for device in m:
                device2count[device] += 1

        item2path = self.collect_item2path([root])
        log.debug("item2path = " + str(item2path))
        d['~objects~'] = 0
        for (device, count) in device2count.items():
            for item in item2path[device]:
                d.at[item, '~objects~'] += count

        total_objects = replication_count * len(values)
        d = self.collect_usage(d, total_objects)

        s = (d['~type~'] == type) & (d['~weight~'] > 0)
        a = d.loc[s, ['~id~', '~weight~', '~objects~', '~over/under used %~']]
        pd.set_option('precision', 2)
        return a.sort_values(by='~over/under used %~', ascending=False)

    def run(self):
        if self.args.crushmap:
            self.crushmap = Crush._convert_to_crushmap(self.args.crushmap)
            return self.analyze()
