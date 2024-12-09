import pyudev
import subprocess

context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem='block')

for device in iter(monitor.poll, None):
    if device.action == 'add':
        print(device.device_node)
        if device.device_node[-1].isdigit():
            cmd = "mount "+device.device_node+" /mnt/usb"+device.device_node[-4:]
            mount_status = str(subprocess.check_output(cmd, shell = True ),'utf-8')
            print(mount_status)
    if device.action == 'remove':
        print(device.device_node)
        if device.device_node[-1].isdigit():
            cmd = "umount "+device.device_node
            umount_status = str(subprocess.check_output(cmd, shell = True ),'utf-8')
            print(umount_status)

