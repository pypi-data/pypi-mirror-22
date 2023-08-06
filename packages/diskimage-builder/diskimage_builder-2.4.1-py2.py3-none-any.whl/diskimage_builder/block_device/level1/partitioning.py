# Copyright 2016 Andreas Florath (andreas@florath.net)
#
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
import os

from subprocess import CalledProcessError

from diskimage_builder.block_device.exception import \
    BlockDeviceSetupException
from diskimage_builder.block_device.level1.mbr import MBR
from diskimage_builder.block_device.level1.partition import \
    Partition
from diskimage_builder.block_device.level1.partition import \
    PartitionTreeConfig
from diskimage_builder.block_device.utils import exec_sudo
from diskimage_builder.block_device.utils import parse_abs_size_spec
from diskimage_builder.block_device.utils import parse_rel_size_spec
from diskimage_builder.graph.digraph import Digraph


logger = logging.getLogger(__name__)


class PartitioningTreeConfig(object):

    @staticmethod
    def config_tree_to_digraph(config_key, config_value, dconfig,
                               default_base_name, plugin_manager):
        logger.debug("called [%s] [%s] [%s]"
                     % (config_key, config_value, default_base_name))
        assert config_key == "partitioning"
        base_name = config_value['base'] if 'base' in config_value \
                    else default_base_name
        nconfig = {'base': base_name}
        for k, v in config_value.items():
            if k != 'partitions':
                nconfig[k] = v
            else:
                pconfig = []
                PartitionTreeConfig.config_tree_to_digraph(
                    k, v, pconfig, dconfig, base_name, plugin_manager)
                nconfig['partitions'] = pconfig

        dconfig.append({config_key: nconfig})
        logger.debug("finished new [%s] complete [%s]" % (nconfig, dconfig))


class Partitioning(Digraph.Node):

    tree_config = PartitioningTreeConfig()

    def __init__(self, config, default_config):
        logger.debug("Creating Partitioning object; config [%s]" % config)
        # Because using multiple partitions of one base is done
        # within one object, there is the need to store a flag if the
        # creation of the partitions was already done.
        self.already_created = False

        # Parameter check
        if 'base' not in config:
            raise BlockDeviceSetupException("Partitioning config needs 'base'")
        self.base = config['base']

        if 'partitions' not in config:
            raise BlockDeviceSetupException(
                "Partitioning config needs 'partitions'")

        if 'label' not in config:
            raise BlockDeviceSetupException(
                "Partitioning config needs 'label'")
        self.label = config['label']
        if self.label not in ("mbr", ):
            raise BlockDeviceSetupException("Label must be 'mbr'")

        # It is VERY important to get the alignment correct. If this
        # is not correct, the disk performance might be very poor.
        # Example: In some tests a 'off by one' leads to a write
        # performance of 30% compared to a correctly aligned
        # partition.
        # The problem for DIB is, that it cannot assume that the host
        # system uses the same IO sizes as the target system,
        # therefore here a fixed approach (as used in all modern
        # systems with large disks) is used.  The partitions are
        # aligned to 1MiB (which are about 2048 times 512 bytes
        # blocks)
        self.align = 1024 * 1024  # 1MiB as default
        if 'align' in config:
            self.align = parse_abs_size_spec(config['align'])

        self.partitions = []
        prev_partition = None

        for part_cfg in config['partitions']:
            np = Partition(part_cfg, self, prev_partition)
            self.partitions.append(np)
            prev_partition = np

    def _size_of_block_dev(self, dev):
        with open(dev, "r") as fd:
            fd.seek(0, 2)
            return fd.tell()

    def insert_nodes(self, dg):
        for part in self.partitions:
            logger.debug("Insert node [%s]" % part)
            dg.add_node(part)

    def _all_part_devices_exist(self, expected_part_devices):
        for part_device in expected_part_devices:
            logger.debug("Checking if partition device [%s] exists" %
                         part_device)
            if not os.path.exists(part_device):
                logger.info("Partition device [%s] does not exists"
                            % part_device)
                return False
            logger.debug("Partition already exists [%s]" % part_device)
        return True

    def _notify_os_of_partition_changes(self, device_path, partition_devices):
        """Notify of of partition table changes

        There is the need to call some programs to inform the operating
        system of partition tables changes.
        These calls are highly distribution and version specific. Here
        a couple of different methods are used to get the best result.
        """
        try:
            exec_sudo(["partprobe", device_path])
            exec_sudo(["udevadm", "settle"])
        except CalledProcessError as e:
            logger.info("Ignoring settling failure: %s" % e)
            pass

        if self._all_part_devices_exist(partition_devices):
            return
        # If running inside Docker, make our nodes manually, because udev
        # will not be working.
        if os.path.exists("/.dockerenv"):
            # kpartx cannot run in sync mode in docker.
            exec_sudo(["kpartx", "-av", device_path])
            exec_sudo(["dmsetup", "--noudevsync", "mknodes"])
            return

        exec_sudo(["kpartx", "-avs", device_path])

    def create(self, result, rollback):
        image_path = result['blockdev'][self.base]['image']
        device_path = result['blockdev'][self.base]['device']
        logger.info("Creating partition on [%s] [%s]" %
                    (self.base, image_path))

        if self.already_created:
            logger.info("Not creating the partitions a second time.")
            return

        assert self.label == 'mbr'

        partition_devices = set()
        disk_size = self._size_of_block_dev(image_path)
        with MBR(image_path, disk_size, self.align) as part_impl:
            for part_cfg in self.partitions:
                part_name = part_cfg.get_name()
                part_bootflag = Partition.flag_boot \
                                in part_cfg.get_flags()
                part_primary = Partition.flag_primary \
                               in part_cfg.get_flags()
                part_size = part_cfg.get_size()
                part_free = part_impl.free()
                part_type = part_cfg.get_type()
                logger.debug("Not partitioned space [%d]" % part_free)
                part_size = parse_rel_size_spec(part_size,
                                                part_free)[1]
                part_no \
                    = part_impl.add_partition(part_primary, part_bootflag,
                                              part_size, part_type)
                logger.debug("Create partition [%s] [%d]" %
                             (part_name, part_no))
                partition_device_name = device_path + "p%d" % part_no
                result['blockdev'][part_name] \
                    = {'device': partition_device_name}
                partition_devices.add(partition_device_name)

        self.already_created = True
        self._notify_os_of_partition_changes(device_path, partition_devices)
        return
