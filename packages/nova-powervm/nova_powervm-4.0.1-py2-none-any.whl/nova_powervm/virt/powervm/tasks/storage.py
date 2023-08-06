# Copyright 2015 IBM Corp.
#
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import six

from pypowervm.tasks import scsi_mapper as pvm_smap

from oslo_log import log as logging
from taskflow.types import failure as task_fail

from nova_powervm.virt.powervm.disk import driver as disk_driver
from nova_powervm.virt.powervm import exception as npvmex
from nova_powervm.virt.powervm.i18n import _LI
from nova_powervm.virt.powervm.i18n import _LW
from nova_powervm.virt.powervm import media
from nova_powervm.virt.powervm import mgmt
from nova_powervm.virt.powervm.tasks import base as pvm_task

LOG = logging.getLogger(__name__)


class ConnectVolume(pvm_task.PowerVMTask):

    """The task to connect a volume to an instance."""

    def __init__(self, vol_drv, slot_mgr):
        """Create the task.

        :param vol_drv: The volume driver (see volume folder).  Ties the
                        storage to a connection type (ex. vSCSI or NPIV).
        :param slot_mgr: A NovaSlotManager.  Used to store/retrieve the client
                         slots used when a volume is attached to the VM
        """
        self.vol_drv = vol_drv
        self.vol_id = self.vol_drv.connection_info['data']['volume_id']
        self.slot_mgr = slot_mgr

        super(ConnectVolume, self).__init__(
            self.vol_drv.instance, 'connect_vol_%s' % self.vol_id)

    def execute_impl(self):
        LOG.info(_LI('Connecting volume %(vol)s to instance %(inst)s'),
                 {'vol': self.vol_id, 'inst': self.vol_drv.instance.name})
        self.vol_drv.connect_volume(self.slot_mgr)

    def revert_impl(self, result, flow_failures):
        # The parameters have to match the execute method, plus the response +
        # failures even if only a subset are used.
        LOG.warning(_LW('Volume %(vol)s for instance %(inst)s to be '
                        'disconnected'),
                    {'vol': self.vol_id, 'inst': self.vol_drv.instance.name})

        # Note that the rollback is *instant*.  Resetting the FeedTask ensures
        # immediate rollback.
        self.vol_drv.reset_stg_ftsk()
        try:
            # We attempt to disconnect in case we 'partially connected'.  In
            # the connect scenario, perhaps one of the Virtual I/O Servers
            # was connected.  This attempts to clear anything out to make sure
            # the terminate connection runs smoothly.
            self.vol_drv.disconnect_volume(self.slot_mgr)
        except npvmex.VolumeDetachFailed as e:
            # Only log that the volume detach failed.  Should not be blocking
            # due to being in the revert flow.
            LOG.warning(_LW("Unable to disconnect volume for %(inst)s during "
                            "rollback.  Error was: %(error)s"),
                        {'inst': self.vol_drv.instance.name,
                         'error': e.message})


class DisconnectVolume(pvm_task.PowerVMTask):

    """The task to disconnect a volume from an instance."""

    def __init__(self, vol_drv, slot_mgr):
        """Create the task.

        :param vol_drv: The volume driver (see volume folder).  Ties the
                        storage to a connection type (ex. vSCSI or NPIV).
        :param slot_mgr: A NovaSlotManager.  Used to store/retrieve the client
                         slots used when a volume is detached from the VM
        """
        self.vol_drv = vol_drv
        self.vol_id = self.vol_drv.connection_info['data']['volume_id']
        self.slot_mgr = slot_mgr
        super(DisconnectVolume, self).__init__(
            self.vol_drv.instance, 'disconnect_vol_%s' % self.vol_id)

    def execute_impl(self):
        LOG.info(_LI('Disconnecting volume %(vol)s from instance %(inst)s'),
                 {'vol': self.vol_id, 'inst': self.vol_drv.instance.name})
        self.vol_drv.disconnect_volume(self.slot_mgr)

    def revert_impl(self, result, flow_failures):
        # The parameters have to match the execute method, plus the response +
        # failures even if only a subset are used.
        LOG.warning(_LW('Volume %(vol)s for instance %(inst)s to be '
                        're-connected'),
                    {'vol': self.vol_id, 'inst': self.vol_drv.instance.name})

        # Note that the rollback is *instant*.  Resetting the FeedTask ensures
        # immediate rollback.
        self.vol_drv.reset_stg_ftsk()
        try:
            # We try to reconnect the volume here so that it maintains its
            # linkage (in the hypervisor) to the VM.  This makes it easier for
            # operators to understand the linkage between the VMs and volumes
            # in error scenarios.  This is simply useful for debug purposes
            # if there is an operational error.
            self.vol_drv.connect_volume(self.slot_mgr)
        except npvmex.VolumeAttachFailed as e:
            # Only log that the volume attach failed.  Should not be blocking
            # due to being in the revert flow.  See comment above.
            LOG.warning(_LW("Unable to re-connect volume for %(inst)s during "
                            "rollback.  Error was: %(error)s"),
                        {'inst': self.vol_drv.instance.name,
                         'error': e.message})


class CreateDiskForImg(pvm_task.PowerVMTask):

    """The Task to create the disk from an image in the storage."""

    def __init__(self, disk_dvr, context, instance, image_meta, disk_size=0,
                 image_type=disk_driver.DiskType.BOOT):
        """Create the Task.

        Provides the 'disk_dev_info' for other tasks.  Comes from the disk_dvr
        create_disk_from_image method.

        :param disk_dvr: The storage driver.
        :param context: The context passed into the driver method.
        :param instance: The nova instance.
        :param nova.objects.ImageMeta image_meta:
            The metadata of the image of the instance.
        :param disk_size: The size of disk to create. If the size is smaller
                          than the image, the image size will be used.
        :param image_type: The image type. See disk/driver.py
        """
        super(CreateDiskForImg, self).__init__(
            instance, 'crt_disk_from_img', provides='disk_dev_info')
        self.disk_dvr = disk_dvr
        self.context = context
        self.image_meta = image_meta
        self.disk_size = disk_size
        self.image_type = image_type

    def execute_impl(self):
        return self.disk_dvr.create_disk_from_image(
            self.context, self.instance, self.image_meta, self.disk_size,
            image_type=self.image_type)

    def revert_impl(self, result, flow_failures):
        # If there is no result, or its a direct failure, then there isn't
        # anything to delete.
        if result is None or isinstance(result, task_fail.Failure):
            return

        # Run the delete.  The result is a single disk.  Wrap into list
        # as the method works with plural disks.
        self.disk_dvr.delete_disks(self.context, self.instance, [result])


class ConnectDisk(pvm_task.PowerVMTask):

    """The task to connect the disk to the instance."""

    def __init__(self, disk_dvr, context, instance, stg_ftsk=None):
        """Create the Task for the connect disk to instance method.

        Requires LPAR info through requirement of lpar_wrap.

        Requires disk info through requirement of disk_dev_info (provided by
        crt_disk_from_img)

        :param disk_dvr: The disk driver.
        :param context: The context passed into the spawn method.
        :param instance: The nova instance.
        :param stg_ftsk: (Optional) The pypowervm transaction FeedTask for the
                         I/O Operations.  If provided, the Virtual I/O Server
                         mapping updates will be added to the FeedTask.  This
                         defers the updates to some later point in time.  If
                         the FeedTask is not provided, the updates will be run
                         immediately when the respective method is executed.
        """
        super(ConnectDisk, self).__init__(
            instance, 'connect_disk', requires=['disk_dev_info'])
        self.disk_dvr = disk_dvr
        self.context = context
        self.stg_ftsk = stg_ftsk

    def execute_impl(self, disk_dev_info,):
        self.disk_dvr.connect_disk(self.context, self.instance, disk_dev_info,
                                   stg_ftsk=self.stg_ftsk)

    def revert_impl(self, disk_dev_info, result, flow_failures):
        # Note that the FeedTask is None - to force instant disconnect.
        self.disk_dvr.disconnect_image_disk(self.context, self.instance)


class InstanceDiskToMgmt(pvm_task.PowerVMTask):

    """Connect an instance's disk to the management partition, discover it.

    We do these two pieces together because their reversion doesn't happen in
    the opposite order.
    """

    def __init__(self, disk_dvr, instance):
        """Create the Task for connecting boot disk to mgmt partition.

        Provides:
        stg_elem: The storage element wrapper (pypowervm LU, PV, etc.) that was
                  connected.
        vios_wrap: The Virtual I/O Server wrapper
                   (pypowervm.wrappers.virtual_io_server.VIOS) from which the
                   storage element was mapped.
        disk_path: The local path to the mapped-and-discovered device, e.g.
                   '/dev/sde'

        :param disk_dvr: The disk driver.
        :param instance: The nova instance whose boot disk is to be connected.
        """
        super(InstanceDiskToMgmt, self).__init__(
            instance, 'connect_and_discover_instance_disk_to_mgmt',
            provides=['stg_elem', 'vios_wrap', 'disk_path'])
        self.disk_dvr = disk_dvr
        self.stg_elem = None
        self.vios_wrap = None
        self.disk_path = None

    def execute_impl(self):
        """Map the instance's boot disk and discover it."""

        # Search for boot disk on the Novalink partition
        if self.disk_dvr.mp_uuid in self.disk_dvr.vios_uuids:
            dev_name = self.disk_dvr.boot_disk_path_for_instance(
                self.instance, self.disk_dvr.mp_uuid)
            if dev_name is not None:
                return None, None, dev_name

        self.stg_elem, self.vios_wrap = (
            self.disk_dvr.connect_instance_disk_to_mgmt(self.instance))
        new_maps = pvm_smap.find_maps(
            self.vios_wrap.scsi_mappings, client_lpar_id=self.disk_dvr.mp_uuid,
            stg_elem=self.stg_elem)
        if not new_maps:
            raise npvmex.NewMgmtMappingNotFoundException(
                stg_name=self.stg_elem.name, vios_name=self.vios_wrap.name)

        # new_maps should be length 1, but even if it's not - i.e. we somehow
        # matched more than one mapping of the same dev to the management
        # partition from the same VIOS - it is safe to use the first one.
        the_map = new_maps[0]
        # Scan the SCSI bus, discover the disk, find its canonical path.
        LOG.info(_LI("Discovering device and path for mapping of %(dev_name)s "
                     "on the management partition."),
                 {'dev_name': self.stg_elem.name})
        self.disk_path = mgmt.discover_vscsi_disk(the_map)
        return self.stg_elem, self.vios_wrap, self.disk_path

    def revert_impl(self, result, flow_failures):
        """Unmap the disk and then remove it from the management partition.

        We use this order to avoid rediscovering the device in case some other
        thread scans the SCSI bus between when we remove and when we unmap.
        """
        if self.vios_wrap is None or self.stg_elem is None:
            # We never even got connected - nothing to do
            return
        LOG.warning(_LW("Unmapping boot disk %(disk_name)s of instance "
                        "%(instance_name)s from management partition via "
                        "Virtual I/O Server %(vios_name)s."),
                    {'disk_name': self.stg_elem.name,
                     'instance_name': self.instance.name,
                     'vios_name': self.vios_wrap.name})
        self.disk_dvr.disconnect_disk_from_mgmt(self.vios_wrap.uuid,
                                                self.stg_elem.name)

        if self.disk_path is None:
            # We did not discover the disk - nothing else to do.
            return
        LOG.warning(_LW("Removing disk %(disk_path)s from the management "
                        "partition."), {'disk_path': self.disk_path})
        mgmt.remove_block_dev(self.disk_path)


class RemoveInstanceDiskFromMgmt(pvm_task.PowerVMTask):

    """Unmap and remove an instance's boot disk from the mgmt partition."""

    def __init__(self, disk_dvr, instance):
        """Unmap and remove an instance's boot disk from the mgmt partition.

        Requires (from InstanceDiskToMgmt):
        stg_elem: The storage element wrapper (pypowervm LU, PV, etc.) that was
                  connected.
        vios_wrap: The Virtual I/O Server wrapper
                   (pypowervm.wrappers.virtual_io_server.VIOS) from which the
                   storage element was mapped.
        disk_path: The local path to the mapped-and-discovered device, e.g.
                   '/dev/sde'

        :param disk_dvr: The disk driver.
        :param instance: The nova instance whose boot disk is to be connected.
        """
        self.disk_dvr = disk_dvr
        super(RemoveInstanceDiskFromMgmt, self).__init__(
            instance, 'remove_inst_disk_from_mgmt',
            requires=['stg_elem', 'vios_wrap', 'disk_path'])

    def execute_impl(self, stg_elem, vios_wrap, disk_path):
        """Unmap and remove an instance's boot disk from the mgmt partition.

        Input parameters ('requires') provided by InstanceDiskToMgmt task.

        :param stg_elem: The storage element wrapper (pypowervm LU, PV, etc.)
                         to be disconnected.
        :param vios_wrap: The Virtual I/O Server wrapper from which the
                          mapping is to be removed.
        :param disk_path: The local path to the disk device to be removed, e.g.
                          '/dev/sde'
        """
        # stg_elem is None if boot disk was not mapped to management partition
        if stg_elem is None:
            return
        LOG.info(_LI("Unmapping boot disk %(disk_name)s of instance "
                     "%(instance_name)s from management partition via Virtual "
                     "I/O Server %(vios_name)s."),
                 {'disk_name': stg_elem.name,
                  'instance_name': self.instance.name,
                  'vios_name': vios_wrap.name})
        self.disk_dvr.disconnect_disk_from_mgmt(vios_wrap.uuid, stg_elem.name)
        LOG.info(_LI("Removing disk %(disk_path)s from the management "
                     "partition."), {'disk_path': disk_path})
        mgmt.remove_block_dev(disk_path)


class CreateAndConnectCfgDrive(pvm_task.PowerVMTask):

    """The task to create the configuration drive."""

    def __init__(self, adapter, host_uuid, instance, injected_files,
                 network_info, admin_pass, stg_ftsk=None):
        """Create the Task that create and connect the config drive.

        Requires the 'lpar_wrap' and 'mgmt_cna'
        Provides the 'cfg_drv_vscsi_map' which is an element to later map
        the vscsi drive.

        :param adapter: The adapter for the pypowervm API
        :param host_uuid: The host UUID of the system.
        :param instance: The nova instance
        :param injected_files: A list of file paths that will be injected into
                               the ISO.
        :param network_info: The network_info from the nova spawn method.
        :param admin_pass: Optional password to inject for the VM.
        :param stg_ftsk: (Optional) The pypowervm transaction FeedTask for the
                         I/O Operations.  If provided, the Virtual I/O Server
                         mapping updates will be added to the FeedTask.  This
                         defers the updates to some later point in time.  If
                         the FeedTask is not provided, the updates will be run
                         immediately when the respective method is executed.
        """
        super(CreateAndConnectCfgDrive, self).__init__(
            instance, 'cfg_drive', requires=['lpar_wrap', 'mgmt_cna'])
        self.adapter = adapter
        self.host_uuid = host_uuid
        self.injected_files = injected_files
        self.network_info = network_info
        self.ad_pass = admin_pass
        self.mb = None
        self.stg_ftsk = stg_ftsk

    def execute_impl(self, lpar_wrap, mgmt_cna):
        self.mb = media.ConfigDrivePowerVM(self.adapter, self.host_uuid)
        self.mb.create_cfg_drv_vopt(self.instance, self.injected_files,
                                    self.network_info, lpar_wrap.uuid,
                                    admin_pass=self.ad_pass,
                                    mgmt_cna=mgmt_cna, stg_ftsk=self.stg_ftsk)

    def revert_impl(self, lpar_wrap, mgmt_cna, result, flow_failures):
        # The parameters have to match the execute method, plus the response +
        # failures even if only a subset are used.

        # No media builder, nothing to do
        if self.mb is None:
            return

        # Delete the virtual optical media. If it fails we don't care.
        try:
            self.mb.dlt_vopt(lpar_wrap.uuid)
        except Exception as e:
            LOG.warning(_LW('Vopt removal as part of spawn reversion failed '
                            'with: %(exc)s'), {'exc': six.text_type(e)},
                        instance=self.instance)


class DeleteVOpt(pvm_task.PowerVMTask):

    """The task to delete the virtual optical."""

    def __init__(self, adapter, host_uuid, instance, lpar_uuid,
                 stg_ftsk=None):
        """Creates the Task to delete the instances virtual optical media.

        :param adapter: The adapter for the pypowervm API
        :param host_uuid: The host UUID of the system.
        :param instance: The nova instance.
        :param lpar_uuid: The UUID of the lpar that has media.
        :param stg_ftsk: (Optional) The pypowervm transaction FeedTask for the
                         I/O Operations.  If provided, the Virtual I/O Server
                         mapping updates will be added to the FeedTask.  This
                         defers the updates to some later point in time.  If
                         the FeedTask is not provided, the updates will be run
                         immediately when the respective method is executed.
        """
        super(DeleteVOpt, self).__init__(instance, 'vopt_delete')
        self.adapter = adapter
        self.host_uuid = host_uuid
        self.lpar_uuid = lpar_uuid
        self.stg_ftsk = stg_ftsk

    def execute_impl(self):
        media_builder = media.ConfigDrivePowerVM(self.adapter, self.host_uuid)
        media_builder.dlt_vopt(self.lpar_uuid, stg_ftsk=self.stg_ftsk)


class DetachDisk(pvm_task.PowerVMTask):

    """The task to detach the disk storage from the instance."""

    def __init__(self, disk_dvr, context, instance, stg_ftsk=None,
                 disk_type=None):
        """Creates the Task to detach the storage adapters.

        Provides the stor_adpt_mappings.  A list of pypowervm
        VSCSIMappings or VFCMappings (depending on the storage adapter).

        :param disk_dvr: The DiskAdapter for the VM.
        :param context: The nova context.
        :param instance: The nova instance.
        :param stg_ftsk: (Optional) The pypowervm transaction FeedTask for the
                         I/O Operations.  If provided, the Virtual I/O Server
                         mapping updates will be added to the FeedTask.  This
                         defers the updates to some later point in time.  If
                         the FeedTask is not provided, the updates will be run
                         immediately when the respective method is executed.
        :param disk_type: List of disk types to detach. None means detach all.
        """
        super(DetachDisk, self).__init__(
            instance, 'detach_storage', provides='stor_adpt_mappings')
        self.disk_dvr = disk_dvr
        self.context = context
        self.stg_ftsk = stg_ftsk
        self.disk_type = disk_type

    def execute_impl(self):
        return self.disk_dvr.disconnect_image_disk(
            self.context, self.instance, stg_ftsk=self.stg_ftsk,
            disk_type=self.disk_type)


class DeleteDisk(pvm_task.PowerVMTask):

    """The task to delete the backing storage."""

    def __init__(self, disk_dvr, context, instance):
        """Creates the Task to delete the disk storage from the system.

        Requires the stor_adpt_mappings.

        :param disk_dvr: The DiskAdapter for the VM.
        :param context: The nova context.
        :param instance: The nova instance.
        """
        req = ['stor_adpt_mappings']
        super(DeleteDisk, self).__init__(instance, 'dlt_storage', requires=req)
        self.disk_dvr = disk_dvr
        self.context = context

    def execute_impl(self, stor_adpt_mappings):
        self.disk_dvr.delete_disks(self.context, self.instance,
                                   stor_adpt_mappings)


class SaveBDM(pvm_task.PowerVMTask):

    """Task to save an updated block device mapping."""

    def __init__(self, bdm, instance):
        """Creates the Task to save an updated block device mapping.

        :param bdm: The updated bdm.
        :param instance: The nova instance
        """
        self.bdm = bdm
        super(SaveBDM, self).__init__(
            instance, 'save_bdm_%s' % self.bdm.volume_id)

    def execute_impl(self):
        LOG.info(_LI('Saving block device mapping for volume id %(vol_id)s '
                     'on instance %(inst)s.'),
                 {'vol_id': self.bdm.volume_id, 'inst': self.instance.name})
        self.bdm.save()


class FindDisk(pvm_task.PowerVMTask):

    """The Task to find a disk and provide information to downstream tasks."""

    def __init__(self, disk_dvr, context, instance, disk_type):
        """Create the Task.

        Provides the 'disk_dev_info' for other tasks.  Comes from the disk_dvr
        create_disk_from_image method.

        :param disk_dvr: The storage driver.
        :param context: The context passed into the driver method.
        :param instance: The nova instance.
        :param disk_type: One of the DiskType enum values.
        """
        super(FindDisk, self).__init__(
            instance, 'find_disk', provides='disk_dev_info')
        self.disk_dvr = disk_dvr
        self.context = context
        self.disk_type = disk_type

    def execute_impl(self):
        disk = self.disk_dvr.get_disk_ref(self.instance, self.disk_type)
        if not disk:
            LOG.warning(_LW('Disk not found: %(disk_name)s'),
                        {'disk_name':
                            self.disk_dvr._get_disk_name(self.disk_type,
                                                         self.instance),
                         }, instance=self.instance)
        return disk


class ExtendDisk(pvm_task.PowerVMTask):

    """Task to extend a disk."""

    def __init__(self, disk_dvr, context, instance, disk_info, size):
        """Creates the Task to extend a disk.

        :param disk_dvr: The storage driver.
        :param context: nova context for operation.
        :param instance: instance to extend the disk for.
        :param disk_info: dictionary with disk info.
        :param size: the new size in gb.
        """
        self.disk_dvr = disk_dvr
        self.context = context
        self.disk_info = disk_info
        self.size = size
        super(ExtendDisk, self).__init__(
            instance, 'extend_disk_%s' % disk_info['type'])

    def execute_impl(self):
        LOG.info(_LI('Extending disk size of disk: %(disk)s size: %(size)s.'),
                 {'disk': self.disk_info['type'], 'size': self.size})
        self.disk_dvr.extend_disk(self.context, self.instance, self.disk_info,
                                  self.size)
