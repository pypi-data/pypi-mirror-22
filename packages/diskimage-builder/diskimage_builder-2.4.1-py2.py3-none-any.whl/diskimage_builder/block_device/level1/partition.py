# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging

from diskimage_builder.block_device.exception import \
    BlockDeviceSetupException
from diskimage_builder.block_device.tree_config import TreeConfig
from diskimage_builder.graph.digraph import Digraph


logger = logging.getLogger(__name__)


class PartitionTreeConfig(object):

    @staticmethod
    def config_tree_to_digraph(config_key, config_value, pconfig, dconfig,
                               base_name, plugin_manager):
        logger.debug("called [%s] [%s] [%s]"
                     % (config_key, config_value, base_name))
        assert config_key == Partition.type_string

        for partition in config_value:
            name = partition['name']
            nconfig = {
                'name': name,
                'base': base_name
            }
            for k, v in partition.items():
                if k not in plugin_manager:
                    nconfig[k] = v
                else:
                    plugin_manager[k].plugin \
                                     .tree_config.config_tree_to_digraph(
                                         k, v, dconfig, name, plugin_manager)
            pconfig.append(nconfig)

        logger.debug("finished [%s] [%s]" % (nconfig, dconfig))


class Partition(Digraph.Node):

    type_string = "partitions"
    tree_config = TreeConfig("partitions")

    flag_boot = 1
    flag_primary = 2

    def __init__(self, config, parent, prev_partition):
        if 'name' not in config:
            raise BlockDeviceSetupException(
                "Missing 'name' in partition config: %s" % config)
        self.name = config['name']

        Digraph.Node.__init__(self, self.name)

        self.base = config['base']
        self.partitioning = parent
        self.prev_partition = prev_partition

        self.flags = set()
        if 'flags' in config:
            for f in config['flags']:
                if f == 'boot':
                    self.flags.add(self.flag_boot)
                elif f == 'primary':
                    self.flags.add(self.flag_primary)
                else:
                    raise BlockDeviceSetupException("Unknown flag: %s" % f)

        if 'size' not in config:
            raise BlockDeviceSetupException("No size in partition" % self.name)
        self.size = config['size']

        self.ptype = int(config['type'], 16) if 'type' in config else 0x83

    def __repr__(self):
        return "<Partition [%s] on [%s] size [%s] prev [%s]>" \
            % (self.name, self.base, self.size,
               self.prev_partition.name if self.prev_partition else "UNSET")

    def get_flags(self):
        return self.flags

    def get_size(self):
        return self.size

    def get_type(self):
        return self.ptype

    def get_name(self):
        return self.name

    def insert_edges(self, dg):
        bnode = dg.find(self.base)
        assert bnode is not None
        dg.create_edge(bnode, self)
        if self.prev_partition is not None:
            logger.debug("Insert edge [%s]" % self)
            dg.create_edge(self.prev_partition, self)

    def create(self, result, rollback):
        self.partitioning.create(result, rollback)

    def umount(self, state):
        """Partition does not need any umount task."""
        pass

    def cleanup(self, state):
        """Partition does not need any cleanup."""
        pass

    def delete(self, state):
        """Partition does not need any cleanup."""
        pass
