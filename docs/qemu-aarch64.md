# Deployment in qemu aarch64

This tutorial will presume your computer is based on a x86_64 architecture and is not presented in the README because it could be harder to get into.

## Pre-requisites

This tutorial require the following packages/commands to be installed:

* **wget**

* **ssh**

* **xz**

* **kpartx**

* **qemu-aarch64**

## Getting a redpesk® image

Because we want to emulate an aarch64 board, let's retrieve the m3ulcb image whis is used in the [README.md](https://github.com/redpesk/agl-service-helloworld/blob/master/README.md).

```bash
wget http://download.lorient.iot/redpesk-nightly/minimal/m3ulcb/latest/redpesk®-minimal-8_II-1.aarch64.raw.xz
export RP_IMAGE=RedPesk-minimal-8_II-1.aarch64.raw.xz
```

Then unzip it

```bash
xz -d --verbose ${RP_IMAGE}
```

## Running a redpesk® image

First of all, you must get the qemu-aarch64 functionality. For example, Ubuntu user can run

```bash
sudo apt install qemu-system-arm
```

In order to emulate an aarch64 architecture, you will need to get an aarch64 based kernel while running on a x86_64 host. You can either build your own aarch64 kernel, or get the basic one we designed for the aarch64 image you have just downloaded.

To retrieve this kernel image you must install **kpartx** and then do the following commands:  
**Warning**: some of these commands need to be run in superuser to be effective

```bash
kpartx_output="$(kpartx -sav ${PATH_TO_UNCOMPRESS_IMAGE} | grep "loop.*p2")"
loop_name="$(echo $kpartx_output | cut -d ' ' -f 3)"
generic_loop="$(echo $loop_name | sed "s/p2$//")"
```

Then, mount the partition on your host, for example here : `/tmp/mount_point`.

```bash
export MOUNT_DIR=/tmp/mount_point
mkdir -p $MOUNT_DIR
mount /dev/mapper/$loop_name $MOUNT_DIR
```

Then the kernel Image is located at the following path `$MOUNT_DIR/Image`, copy it wherever you want, we will use it for the qemu command.  
To finish properly, unmount and delete the previous partition.

```bash
umount $MOUNT_DIR
rm -r $MOUNT_DIR
kpartx -d /dev/$generic_loop
```

Once you have the kernel Image, you can finally run your redpesk® image.

```bash
export TCP_PORT=3333
qemu-system-aarch64 \
        -kernel ${PATH_TO_KERNEL_IMAGE} \
        -machine accel=tcg,type=virt \
        -m 2048 \
        -cpu cortex-a57 \
        -drive id=disk0,file=${PATH_TO_REDPESK_IMAGE},if=none,format=raw \
        -device virtio-blk-device,drive=disk0 \
        -append 'console=ttyAMA0,115200 root=/dev/vda5 security=none' \
        -net nic -net user,hostfwd=tcp::{$TCP_PORT}-:22 \
        -nographic \
        -snapshot
```

You may have noticed that in the previous command we allow the user to connect to the emulated board by establishing a ssh connection through the port `${TCP_PORT}`.

The image you have just downloaded has the following configuration:

* login: root

* password: root

Then you can access your emulated board with the following command:

```bash
ssh root@localhost -p ${TCP_PORT}
```

## Installing your package

From this point, there is no difference with the cases studied in the [README.md](../README.md)
