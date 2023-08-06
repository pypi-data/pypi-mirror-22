Ceph pool optimization
======================

How to rebalance an empty pool
------------------------------

Rebalancing a pool may move a lot of PGs around and slow down the
cluster if they contain a lot of objects. This is not a concern when
the pool was just created and is empty.

Get the report from the ceph cluster: it contains the crushmap, the
osdmap and the information about all pools::

    $ ceph report > report.json

Run the optimization for a given pool with::

    $ crush optimize --crushmap report.json --out-path optimized.crush --pool 3

Upload the crushmap to the ceph cluster with::

    $ ceph osd setcrushmap -i optimized.crush

How to rebalance a pool step by step
------------------------------------

When a pool contains objects, rebalancing can be done in small
increments (as specified by --step) to limit the number of PGs being
moved.

Get the report from the ceph cluster: it contains the crushmap, the
osdmap and the information about all pools::

    $ ceph report > report.json

Run the optimization for a given pool and move as few PGs as possible
with::

    $ crush optimize \
            --step 1 \
            --crushmap report.json --out-path optimized.crush \
            --pool 3

Upload the crushmap to the ceph cluster with::

    $ ceph osd setcrushmap -i optimized.crush

Repeat until it cannot be optimized further.

Compare the crushmaps
---------------------

To verify which OSD are going to get or give PGs, the `crush compare`
command can be used::

    $ crush compare --origin report.json \
                    --destination optimized.crush \
                    --pool 3

Adding and removing OSDs
------------------------

When an OSD is added to the crushmap, its weight set should be set to
zero so that `crush optimize` can increase it step by step.

When an OSD is removed, it's target weight should be set to zero so
that `crush optimize` can decrease it step by step.

Requirements
------------

- All buckets in the pool must use the straw2 algorithm.
- The OSDs must all have the default primary affinity.
- The cluster must be HEALTH_OK

Backward compatibility
----------------------

For clusters before Luminous, a pool can be rebalanced provided it is
the sole user of the crush rule. If two pools use the same crush rule,
rebalancing one of them will have an impact on the other.

The first optimization step saves the item weights by creating a
shadow tree in the crushmap, duplicating all buckets and appending
`-target-weight` to their name. For instance::

     root root {
     	id -4
     	# weight 4.000
     	alg straw2
     	hash 0	# rjenkins1
     	item rack0 weight 4.000
     }
     
     root root-target-weight {
     	id -6
     	# weight 4.000
     	alg straw2
     	hash 0	# rjenkins1
     	item rack0-target-weight weight 4.000
     }

Commands such as `ceph df` will display the weights modified by `crush
optimize` and will no longer show relevant values for the deviation
between the expected distribution and the actual OSD usage.

Compare the crushmap created after the first optimization step with::

    $ crush compare --origin report.json \
                    --destination optimized.crush --destination-choose-args 0 \
                    --pool 3

Compare the next crushmaps::

    $ crush compare --origin report.json \
                    --destination optimized.crush --choose-args 0 \
                    --pool 3

The difference is that the shadow tree (`-target-weight`) does not
exist the first time and the `--choose-args` flag only makes sense for
the destination crushmap, not the original ceph report. Also note that
the `--choose-args` must be set to zero instead of the pool number.
