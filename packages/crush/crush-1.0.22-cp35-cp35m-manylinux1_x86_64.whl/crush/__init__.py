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

import copy
import json
import logging
import re
import struct
from crush.libcrush import LibCrush

log = logging.getLogger(__name__)


class CephConverter(object):

    @staticmethod
    def weight_as_float(i):
        return i / 0x10000

    def convert_item(self, item, ceph):
        if item['id'] >= 0:
            return {
                "weight": self.weight_as_float(item['weight']),
                "id": item['id'],
                "name": ceph['id2name'][item['id']],
            }
        else:
            return {
                "weight": self.weight_as_float(item['weight']),
                "reference_id": item['id'],
            }

    def convert_bucket(self, bucket, ceph):
        b = {
            "weight": self.weight_as_float(bucket['weight']),
            "id": bucket['id'],
            "name": bucket['name'],
            "algorithm": bucket['alg'],
            "type": bucket['type_name'],
        }
        items = bucket.get('items', [])
        if items:
            children = []
            last_pos = -1
            for item in items:
                # the actual pos value does not change the mapping
                # when there is an empty item (we do not store pos)
                # but the order of the items is important and we
                # need to assert that the list is ordered
                assert last_pos < item['pos']
                last_pos = item['pos']
                children.append(self.convert_item(item, ceph))
            b['children'] = children
        return b

    def collect_items(self, children, ceph):
        for child in children:
            if 'id' in child:
                ceph['id2item'][child['id']] = child
            self.collect_items(child.get('children', []), ceph)

    def dereference(self, children, ceph):
        for i in range(len(children)):
            child = children[i]
            if 'reference_id' in child:
                id = child['reference_id']
                new_child = copy.copy(ceph['id2item'][id])
                new_child['weight'] = child['weight']
                ceph['is_child'].add(id)
                children[i] = new_child
            self.dereference(child.get('children', []), ceph)

    def convert_buckets(self, ceph):
        ceph['is_child'] = set()
        ceph['id2item'] = {}
        converted = [self.convert_bucket(r, ceph) for r in ceph['buckets']]
        self.collect_items(converted, ceph)
        self.dereference(converted, ceph)
        return list(filter(lambda c: c['id'] not in ceph['is_child'], converted))

    def convert_rule(self, ceph_rule, ceph):
        name = ceph_rule['rule_name']
        rule = []
        for ceph_step in ceph_rule['steps']:
            if 'opcode' in ceph_step:
                if ceph_step['opcode'] in (10, 11, 12, 13):
                    id2name = {
                        10: 'set_choose_local_tries',
                        11: 'set_choose_local_fallback_tries',
                        12: 'set_chooseleaf_vary_r',
                        13: 'set_chooseleaf_stable',
                    }
                    step = [id2name[ceph_step['opcode']], ceph_step['arg1']]
                else:
                    assert 0, "unexpected rule opcode " + str(ceph_step['opcode'])
            elif 'op' in ceph_step:
                if ceph_step['op'] == 'take':
                    step = [ceph_step['op'], ceph_step['item_name']]
                elif ceph_step['op'] in ('chooseleaf_firstn',
                                         'choose_firstn',
                                         'chooseleaf_indep',
                                         'choose_indep'):
                    (choose, how) = ceph_step['op'].split('_')
                    if ceph['type2id'][ceph_step['type']] == 0:
                        type = 0
                    else:
                        type = ceph_step['type']
                    step = [choose, how, ceph_step['num'], 'type', type]
                elif ceph_step['op'] in ('set_choose_local_tries',
                                         'set_choose_local_fallback_tries',
                                         'set_chooseleaf_vary_r',
                                         'set_chooseleaf_stable',
                                         'set_choose_tries',
                                         'set_chooseleaf_tries'):
                    step = [ceph_step['op'], ceph_step['num']]
                elif ceph_step['op'] == 'emit':
                    step = ['emit']
                elif ceph_step['op'] == 'noop':
                    pass
                else:
                    assert 0, "unexpected rule op " + str(ceph_step['op'])
            else:
                assert 0, "no op or opcode found"
            rule.append(step)
        return (name, rule)

    def convert_tunables(self, tunables):
        known = set([
            'choose_local_tries',
            'choose_local_fallback_tries',
            'chooseleaf_vary_r',
            'chooseleaf_stable',
            'chooseleaf_descend_once',
            'straw_calc_version',

            'choose_total_tries',
        ])
        out = {}
        for (k, v) in tunables.items():
            if k in known:
                out[k] = v
        return out

    def parse_ceph(self, ceph):
        ceph['id2name'] = {d['id']: d['name'] for d in ceph['devices']}
        ceph['type2id'] = {t['name']: t['type_id'] for t in ceph['types']}

        j = {
            'private': {},
        }

        j['types'] = ceph['types']

        j['trees'] = self.convert_buckets(ceph)

        j['rules'] = {}
        for ceph_rule in ceph['rules']:
            (name, rule) = self.convert_rule(ceph_rule, ceph)
            j['rules'][name] = rule
        j['private']['rules'] = ceph['rules']

        j['tunables'] = self.convert_tunables(ceph['tunables'])

        j['private']['tunables'] = ceph['tunables']

        if 'choose_args' in ceph:
            j['choose_args'] = ceph['choose_args']

        return j


class Crush(object):
    """Control object placement in a hierarchy.

    The algorithms optimize the placement so that:

    - the devices are filled according to their weight

    - the number of objects that move is proportional to the magnitude
      of the weight of the devices removed or added

    **Choose and chooseleaf retries**

    The "choose firstn" and "choose indep" rule step look for buckets
    of a given type, randomly selecting them. If they are unlucky and
    find the same bucket twice, they will try N+1 times (N being the
    value of the choose_total_tries tunable). If there is a previous
    "set_choose_tries" step in the same rule, it will try O times
    instead (O being the value of the argument of the
    "set_choose_tries" step).

    Note: the choose_total_tries tunable is the number of retry, not
    the number of tries. The number of tries is the number of retry +
    1. The "set_choose_tries" rule step sets the number of tries and
    does not need the + 1. This confusing difference is inherited from
    an off-by-one bug from years ago.

    The "chooseleaf firstn" and "chooseleaf indep" rule step do the same
    as "choose firstn" and "choose indep" but also recursively explore
    each bucket found, looking for a single device. The same device
    may be found in two different buckets because the crush map is not
    a strict hierarchy, it is a DAG. When such a collision happens,
    they will try again. The number of times they try to find a non
    colliding device is:

    - If "firstn" and there is no previous "set_chooseleaf_tries" rule step: try
      N + 1 times (N being the value of the choose_total_tries tunable)

    - If "firstn" and there is a previous "set_chooseleaf_tries" rule
      step: try P times (P being the value of the argument of the
      "set_chooseleaf_tries" rule step)

    - If "indep" and there is no previous "set_chooseleaf_tries" rule step: try
      1 time.

    - If "indep" and there is a previous "set_chooseleaf_tries" rule step:
      try P times (P being the value of the argument of the
      "set_chooseleaf_tries" rule step)

    **Backward compatibility**

    Some tunables and rule steps only exist for backward
    compatibility. Trying to use them will raise an exception, unless
    Crush is created with backward_compatibility=True. They are listed
    here for reference but they are documented in the libcrush api
    at http://doc.libcrush.org/master/group___a_p_i.html.

    In the crushmap::

            tunables = {
              "choose_local_tries": 0,
              "choose_local_fallback_tries": 0,
              "chooseleaf_vary_r": 1,
              "chooseleaf_stable": 1,
              "chooseleaf_descend_once": 1,
              "straw_calc_version": 1,
            }

    In a rule step::

            [ "set_choose_local_tries", <positive integer> ]
            [ "set_choose_local_fallback_tries", <positive integer> ]
            [ "set_chooseleaf_vary_r", 0 or 1 ]
            [ "set_chooseleaf_stable", 0 or 1 ]

    """

    def __init__(self, verbose=False, backward_compatibility=False):
        """Create a Crush.

        If the optional argument `verbose` is set to True, all methods
        will print debug information on stdout. It defaults to False.

        If the optional argument `backward_compatibility` is set to
        True, the tunables designed for backward_compatibility are
        allowed, otherwise trying to use them raises an exception. See
        **Backward compatibility** in the class documentation.

        """
        self.c = LibCrush(verbose=verbose and 1 or 0,
                          backward_compatibility=backward_compatibility and 1 or 0)

    def parse(self, something):
        """Validate and parse `something` which can be one of the
        following:

        - a crushmap dict as documented in the parse_crushmap() method

        - a path to a file containing a JSON representation of a
          crushmap as documented in the Crush.parse_crushmap() method

        - a path to a file containing a Ceph binary, text or JSON
          crushmap compatible with Luminuous and below

        The details of the validation and parsing are documented
        in the parse_crushmap() method.

        """
        return self.parse_crushmap(self._convert_to_crushmap(something))

    def parse_crushmap(self, crushmap):
        """Validate and parse the `crushmap` object.

        The `crushmap` is a hierarchical description of devices in
        which objects can be stored and rules to place the objects.
        It is verified to obey the specifications below. An exception
        is raised on the first error found.
        ::

            crushmap = {
              # optional (default: none)
              "trees": trees,

              # optional (default: none)
              "rules": rules,

              # optional (default: none)
              "choose_args": choose_arg_map,

              # optional (default: none)
              "tunables": tunables,
            }

        The "trees" are the roots of device hierarchies, the "rules" describe
        various object placement strategies for this device hierarchy.
        ::

            trees = [
              # optional (default: none)
              bucket or device or reference,
              bucket or device or reference,
              ...
            ]

        Each element can either be a device (i.e. no children and id >= 0),
        a bucket (i.e. id < 0) or a reference to a bucket or device.
        ::

            bucket = {
              # mandatory
              "type": <str>,

              # mandatory
              "name": <str>,

              # optional (default: first available id)
              "id": <negative int>,

              # optional (default: "straw2")
              "algorithm": "uniform" or "list" or "straw2",

              # optional (default: cumulated children weights or none)
              "weight": <postive float>,

              # optional (default: none)
              "children": children
            }

        The **type** is a user defined string that can be used by
        **rules** to select all buckets of the same type.

        The **name** is a user defined string that uniquely identifies
        the bucket.

        The **id** must either be set for all buckets or not at
        all. If the **id** is provided, it must be a unique negative
        number. If it is not provided, the first available id is
        used.

        The **weight** must either be set for all buckets or not at
        all. If not set, **weight** defaults to the cumulated weight
        of the immediate children bucket or devices or reference,
        recursively, bottom to top.

        Children within a bucket are chosen with one of three
        **algorithms** representing a tradeoff between performance
        and reorganization efficiency. If you are unsure, we recommend
        using **"straw2"**. The table summarizes how the speed of each
        option measures up against mapping stability when items are
        added or removed::

            Bucket Alg     Speed       Additions    Removals
            ------------------------------------------------
            "straw2"        O(n)       optimal      optimal
            "uniform"       O(1)       poor         poor
            "list"          O(n)       optimal      poor

        - **"straw2"**: List and tree buckets are structured such that
          a limited number of hash values need to be calculated and
          compared to weights in order to select a bucket child. In
          doing so, they divide and conquer in a way that either gives
          certain children precedence (e. g., those at the beginning
          of a list) or obviates the need to consider entire subtrees
          of children at all. That improves the performance of the
          replica placement process, but can also introduce suboptimal
          reorganization behavior when the contents of a bucket change
          due an addition, removal, or re-weighting of an child. The
          straw2 bucket type allows all children to fairly `compete`
          against each other for replica placement through a process
          analogous to a draw of straws. To place a replica, a straw
          of random length is drawn for each child in the bucket.  The
          child with the longest straw wins.  The length of each straw
          is initially a value in a fixed range.  Each straw length is
          scaled by a factor based on the child’s weight so that
          heavily weighted children are more likely to win the draw.
          Although this process is almost twice as slow (on average)
          than a list bucket and even slower than a tree bucket (which
          scales logarithmically), straw2 buckets result in optimal
          data movement between nested children when modified.

        - **"uniform"**: Devices are rarely added individually in a
          large system.  Instead, new storage is typically deployed in
          blocks of identical devices, often as an additional shelf in
          a server rack or perhaps an entire cabinet. Devices reaching
          their end of life are often similarly decommissioned as a
          set (individual failures aside), making it natural to treat
          them as a unit. Uniform buckets are used to represent an
          identical set of devices in such circumstances. The key
          advantage in doing so is performance related: Crush can map
          replicas into uniform buckets in constant time. In cases
          where the uniformity restrictions are not appropriate, other
          bucket types can be used. If the size of a uniform bucket
          changes, there is a complete reshuffling of data between
          devices, much like conventional hash-based distribution
          strategies.

        - **"list"**: List buckets structure their contents as a
          linked list, and can contain children with arbitrary
          weights.  To place a replica, Crush begins at the head of
          the list with the most recently added child and compares its
          weight to the sum of all remaining children’ weights.
          Depending on the value of the hash function, either the
          current child is chosen with the appropriate probability, or
          the process continues recursively down the list. This is a
          natural and intuitive choice for an expanding cluster:
          either an object is relocated to the newest device with some
          appropriate probability, or it remains on the older devices
          as before.  The result is optimal data migration when
          children are added to the bucket. Children removed from the
          middle or tail of the list, however, can result in a
          significant amount of unnecessary movement, making list
          buckets most suitable for circumstances in which they never
          (or very rarely) shrink.

        There also exists an older version of "straw2", known as **"straw"**.
        Given the choice, it is *always* better to use "straw2"; "straw" is
        therefore not allowed by default. If the crushmap being read is old
        and still uses "straw", setting `backward_compatibility=True` when
        creating the `Crush` object will allow it to be used.
        ::

            children = [
              # optional (default: none)
              bucket or device or reference,
              bucket or device or reference,
              ...
            ]

        Each element can either be a device (i.e. no children and id >= 0),
        a bucket (i.e. id < 0) or a reference to a bucket or device.
        ::

            reference = {
              # mandatory
              "reference_id": <int>,

              # optional (default: 1.0)
              "weight": <postive float>,
            }

        The **reference_id** must be equal to the **id** of a bucket or
        device defined in the hierarchy.

        If the **weight** is omitted, it default to 1.0. The
        **weight** must either be set for all references or not at
        all.
        ::

            device = {
              # mandatory
              "id": <positive int>,

              # mandatory
              "name": <str>,

              # optional (default: 1.0)
              "weight": <postive float>,
            }

        The **id** must be a unique positive number.

        The **name** is a user defined string that uniquely identifies
        the device.

        If the **weight** of a device A is lower than the
        **weight** of a device B, it will be less likely to be used.
        A common pattern is to set the **weight** to 2.0 for 2TB
        devices, 1.0 for 1TB devices, 0.5 for 500GB devices, etc.
        ::

            rules = {
              # optional (default: none)
              <rule name str>: rule,
              <rule name str>: rule,
              ...
            }

        A **rule** maps an object (see the map function) to a list
        of devices. There can be multiple rules depending on the
        mapping strategy.
        ::

            rule = [ step, step, ... ]

        The **rule** interprets each **step** in sequence and the last
        one must be **"emit"**.
        ::

            step = [ "take", <bucket name str> ]

        Select the **bucket name**.
        ::

            step = [
              "set_choose_tries" or "set_chooseleaf_tries",
              <positive integer>
            ]

        Overrides the default number of tries (set by the
        choose_total_tries tunables and defaulting to 50) when looking
        for a bucket (set_choose_tries) or a device
        (set_chooseleaf_tries). See **Choose and chooseleaf retries**
        in the class documentation for more information.
        ::

            step = [
              "choose"
              "firstn" or "indep",
              <replication count positive int>,
              "type"
              bucket type or device type
            ]

        Recursively explore each bucket currently selected, looking for
        **replication count** buckets of the required **bucket type**
        and select them.

        **firstn** is best suited when the order of the result does not matter,
        for instance to place object replicas. **indep** is best suited when
        the order of the result makes a difference, for instance to place parts
        of an erasure coded object.

        If **replication count** is zero, the number of buckets
        to select will be determined by the `replication_count` argument of
        the `map` method, i.e. **replication count** is set to
        match the desired number of replicas.
        ::

            bucket type = <str>

        The type field of a bucket definition is used in rule steps to
        designate all buckets with the same type.
        ::

            device type = 0

        The devices all have the same fixed type: 0.
        ::

            step = [
              "chooseleaf"
              "firstn" or "indep",
              <replication count positive int>,
              "type"
              <bucket type str>
            ]

        Recursively explore each bucket currently selected, looking for
        **replication count** devices within all buckets of
        the required **bucket type** and select them.

        **firstn** is best suited when the order of the result does not matter,
        for instance to place object replicas. **indep** is best suited when
        the order of the result makes a difference, for instance to place parts
        of an erasure coded object.

        If **replication count** is zero, the number of devices
        to select will be determined by the `replication_count` argument of
        the `map` method, i.e. **replication count** is set to
        match the desired number of replicas.
        ::

            step = [ "emit" ]

        Append the selection to the results and clear the selection
        ::

            choose_arg_map = {
              <name str>: choose_args,
              <name str>: choose_args,
              ...
            }

        A named collection of **choose_args** for **map()** to use for
        changing the weights of straw2 buckets or remap the items they
        contains to arbitrary values. See **map()** for more information.
        ::

            choose_args = [
              choose_args_bucket,
              choose_args_bucket,
              ...
            ]

        A list of **choose_args_bucket**, each modifying the weights
        or the ids of a **bucket**. There must be at most one
        **choose_args_bucket** for a given bucket in the crushmap.
        ::

            choose_args_bucket = {
              # mandatory
              "bucket_id": <negative int> or "bucket_name": <bucket name str>,
              # optional (default: none)
              "ids": choose_args_ids,
              # optional (default: none)
              "weight_set": choose_args_weight_set,
            }

        When calling **map()** with this **choose_args_bucket**,
        straw2 will use **choose_args_ids** instead of the items it
        contains. And instead of using the weights stored in the
        bucket, it will use one of **choose_args_weight_set**,
        depending on the position. See **map()** for more information.

        The bucket is uniquely identified by either **bucket_id**
        which must be a negative number or **bucket_name** which is
        the name of the bucket set in the **bucket** definition. The
        two are mutually exclusive.
        ::

            choose_args_ids = [ <int>, <int>, ... ]

        The first element of **choose_args_ids** will be used instead
        of the id of the first children and so on.

        The size of **choose_args_ids** must be exactly the same as
        the size of the **children** array of the corresponding
        **bucket**.
        ::

            choose_args_weight_set = [
               [ <positive float>, <positive float>, ... ], # position 0
               [ <positive float>, <positive float>, ... ], # position 1
               ...
            ]

        When **map()** chooses the frist replicas from the
        corresponding **bucket** it will use the weights at position 0
        instead of the weights stored in the **bucket**. When choosing
        the second replica it will use the weights at positon 1 and so
        on.

        The size of the array for each position must be exactly the
        same as the size of the **children** array of the corresponding
        **bucket**.

        If **choose_args_weight_set** does not contain a list of weights
        for a given position, the weights in the last available position
        will be used instead.
        ::

            tunables = {
              "choose_total_tries": 50
            }

        A tunable changes the behavior of the **map()** method and it
        will not return the same list of devices if it is changed.

        - **choose_total_tries** (optional positive integer, default:
          50) is the default number of retries on a collision.
          See **Choose and chooseleaf retries** in the class
          documentation for more information.

        """
        self.crushmap = copy.deepcopy(crushmap)
        self.c.parse(self.crushmap)
        self._update_info()
        return True

    def map(self, rule, value, replication_count, weights=None, choose_args=None):
        """Map an object to a list of devices.

        The **rule** is used to map the **value** (representing an
        object) to the desired number of devices
        (**replication_count**) and return them in a list. The
        probabilities for a given device to be selected can be
        modified by the **weights** dictionnary or by **choose_args**
        for straw2 buckets.

        If the mapping is successful, a list of device containing
        exactly **replication_count** devices is returned. If the
        mapping fails, the list may contains less devices or some
        names may be replaced by None. For instance, if asking
        for 3 replicas, the result of a failed mapping could be::

            [ "device1", "device5" ] # 2 instead of 3
            [ "device8", None, "device0" ] # second device is missing

        The dictionary of **weights** modifies the probabilities for
        the device names it contains. The value is a float in the
        range [0..1]. If the weight is 0, the device will never be
        selected.  If the weight is 1, the probability that the device
        is selected is not modified. If a device is not in the
        **weights** dictionary, its probability is not modified. For
        example::

            { "device0": 0.50, "device1": 0.75 }

        will multiply the probability of "device0" by 0.50 (i.e,
        reduce it by 50%) and "device1" by 0.75 (i.e, reduce it by
        25%).

        If the **choose_args** is a string, the corresponding list
        will be retrieved from **choose_arg_map** in the map. Each
        element in the **choose_args** list modifies the parameters of
        the choose function for the corresponding straw2 bucket. With
        a bucket containing two children::

            {
               "name": "bucket1":
               "children": [
                   { "name": "device1", "id": 1, "weight": 1.0 },
                   { "name": "device2", "id": 2, "weight": 2.0 },
               ]
            }

        If map(85) == [ 'device2' ], the result could be different
        by switching the weights with::

            map(85, choose_args=[
              { "bucket_name": "bucket1",
                "weight_set": [ [ 2.0, 1.0 ] ]
              }]) == [ 'device1' ]

        Similarly the result can be influenced by providing
        alternative ids. The id of each item is a parameter of the
        hash considered for placement. However, contrary to the
        weight, there is no way to guess how it will influence the
        result.::

            map(85, choose_args=[
              { "bucket_name": "bucket1",
                "ids": [ 100, 300 ]
              }]) == [ 'device1' ]

        - **rule**: the rule name (required string)

        - **value**: the number to map (required integer)

        - **replication_count**: the desired number of devices
            (required positive integer)

        - **weights**: map of name to weight float (optional, default to None)

        - **choose_args**: name to lookup in the map or a list (optional, default to None)

        Return a list of device names.

        """
        kwargs = {
            "rule": rule,
            "value": value,
            "replication_count": replication_count,
        }
        if weights:
            kwargs["weights"] = weights
        if choose_args:
            kwargs["choose_args"] = choose_args
        return self.c.map(**kwargs)

    @staticmethod
    def _is_ceph_file(something):
        fmt = "I"
        crush_magic = 0x00010000
        head = open(something, mode='rb').read(struct.calcsize(fmt))
        if struct.unpack(fmt, head)[0] == crush_magic:
            return True
        content = open(something).read()
        if (re.search("^device ", content, re.MULTILINE) and
                re.search("^type ", content, re.MULTILINE)):
            return True
        return False

    @staticmethod
    def _convert_from_file(something):
        if Crush._is_ceph_file(something):
            crushmap = LibCrush().ceph_read(something)
            return (json.loads(crushmap), 'ceph-json')
        else:
            with open(something) as f_json:
                crushmap = json.load(f_json)
                log.debug("_detect_file_format: valid json file")
                if 'devices' in crushmap:  # Ceph json format
                    return (crushmap, 'ceph-json')
                return (crushmap, 'python-crush-json')

    @staticmethod
    def _convert_to_dict(something):
        if type(something) is dict:
            if 'devices' in something:  # Ceph json format
                return (something, 'ceph-json')
            return (something, 'python-crush-json')
        else:
            return Crush._convert_from_file(something)

    @staticmethod
    def _convert_to_crushmap(something):
        (crushmap, format) = Crush._convert_to_dict(something)
        if format == 'ceph-json':
            crushmap = CephConverter().parse_ceph(crushmap)
        return crushmap

    def _collect_items(self, children):
        for child in children:
            if 'id' in child:
                self._name2item[child['name']] = child
                self._id2item[child['id']] = child
            self._collect_items(child.get('children', []))

    def _update_info(self):
        self._name2item = {}
        self._id2item = {}
        trees = self.crushmap.get('trees', [])
        self._collect_items(trees)

    def get_item_by_id(self, id):
        return self._id2item[id]

    def get_item_by_name(self, name):
        return self._name2item[name]

    def get_crushmap(self):
        """
        Return the original crushmap given to the parse() method.

        The returned crushmap does not contain any reference_id,
        they are replaced by a pointer to the actual bucket. This
        is convenient when exploring the crushmap. But it will
        fail to parse again because duplicated buckets will be
        found.
        """
        return self.crushmap

    @staticmethod
    def parse_weights_file(weights_file):
        """
        Parse a file containing information about devices weights.
        The file is expected to contain JSON data. It can either be:

         - a dictionary that maps weights (as floats between 0 and 1)
           to device names, e.g.::

            {"device0": 0.71, "device1": 0.212}

         - a JSON dump of a Ceph OSDMap, obtainable with the command::

            ceph osd dump --format json > osdmap.json

        :param weights_file: File object to the weights file
        :type weights_file: file
        :return: Parsed weights
        :rtype: dict[str, float]
        """

        f_name = weights_file.name

        # Load the JSON data
        try:
            raw_data = json.load(weights_file)
        except ValueError:
            raise AssertionError("{} is not valid JSON".format(f_name))

        # It should be an object (dict) and not an array (list)
        assert type(raw_data) is dict, "Expected {} to be a dict".format(f_name)

        osdmap_keys = {"epoch", "fsid", "osds", "pools"}  # And many more!
        if all(k in raw_data for k in osdmap_keys):
            # We're likely dealing with an OSDMap
            try:
                weights = dict(
                    ("osd.{}".format(osd["osd"]), osd["weight"])
                    for osd in raw_data["osds"])
            except:  # Many different exceptions can happen
                raise AssertionError("Failed to read Ceph OSDMap {}".format(f_name))
        else:
            weights = raw_data

        # Check the weight values
        assert all(type(v) is float and 0 <= v <= 1 for v in weights.values()), \
            "Weights must be floating-point values between 0 and 1"

        # Don't check that the keys are existing devices, LibCrush will do it
        # No need to check that keys are strings, it's enforced by JSON

        return weights
