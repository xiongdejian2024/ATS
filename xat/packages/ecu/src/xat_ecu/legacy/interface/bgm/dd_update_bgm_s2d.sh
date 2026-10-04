#!/bin/bash

function FailExit() {
  echo "ERROR: dd update Failed"
  exit 1
}

if [ ! -f imx8dxl-mars1-bgm-fit.itb ]; then
  echo "ERROR: no imx8dxl-mars1-bgm-fit.itb"
  FailExit
fi

if [ ! -f rootfs.img.bz2 ]; then
  echo "ERROR: no rootfs.img.bz2"
  FailExit
fi

if [ ! -f appfs.img.bz2 ]; then
  echo "ERROR: no appfs.img.bz2"
  FailExit
fi

echo "start: $(date)"

current_slot=`cat /proc/cmdline | awk -F ' boot=' {'print $2'} | awk -F ' ' {'print $1'}`
echo "cmdline: boot=${current_slot}"
if [ "x${current_slot}" == "x1" ]; then
    echo "current slot: A"
    dst_kernel_offset=50
    dst_rootfs_part=/dev/mmcblk0p3
    dst_appfs_part=/dev/mmcblk0p5
    dst_snap_part=/dev/mmcblk0p10
    dst_snap_file=mem-snapshotB.img.bz2
    dst_snap_img=mem-snapshotB.img
    next_slot=B
elif [ "x${current_slot}" == "x2" ]; then
    echo "current slot: B"
    dst_kernel_offset=10
    dst_rootfs_part=/dev/mmcblk0p2
    dst_appfs_part=/dev/mmcblk0p4
    dst_snap_part=/dev/mmcblk0p9
    dst_snap_file=mem-snapshotA.img.bz2
    dst_snap_img=mem-snapshotA.img
    next_slot=A
else
    echo "ERROR: can not get A/B slot"
    FailExit
fi

if [ -f "version.txt" ] ; then
  UBOOT_VERSION_SRC=`cat /proc/cmdline | awk -F ' uboot_version=' {'print $2'} | awk -F ' ' {'print $1'}`
  UBOOT_VERSION_DST=`cat version.txt | awk -F 'Uboot: ' {'print $2'}`
  echo "Current boot version [$UBOOT_VERSION_SRC]"
  echo "Target boot version [$UBOOT_VERSION_DST]"
  if [ "$UBOOT_VERSION_SRC" = "$UBOOT_VERSION_DST" ] ; then
    echo "NOTE: uboot version equal, do not flash boot"
  else
    echo "update bootloader"
    if [ -e "/sys/firmware/soc_revision" ]; then
      IMX8_HW_VERSION=$(cat /sys/firmware/soc_revision)
    else
      IMX8_HW_VERSION=$(cat /sys/devices/soc0/revision)
    fi

    if [ -z "$IMX8_HW_VERSION" ];then
      cat /sys/firmware/soc_revision
      cat /sys/devices/soc0/revision
      echo "NOTE: cannot get imx8 version, do not flash boot"
    elif [ "$IMX8_HW_VERSION" = "1.2" ] || [ "$IMX8_HW_VERSION" \> "1.2" ]; then
      if [ ! -f "flash.bin" ]; then
        echo "ERROR: no flash.bin for imx8-B bootloader"
        FailExit
      fi
      echo "flash imx8-B bootloader flash.bin"
      echo 0 > /sys/block/mmcblk0boot0/force_ro
      dd if=flash.bin of=/dev/mmcblk0boot0 bs=1K && sync
      echo 1 > /sys/block/mmcblk0boot0/force_ro

      echo 0 > /sys/block/mmcblk0boot1/force_ro
      dd if=flash.bin of=/dev/mmcblk0boot1 bs=1K && sync
      echo 1 > /sys/block/mmcblk0boot1/force_ro

      dd if=flash.bin of=/dev/mmcblk0 bs=1K seek=32 && sync
    elif [ "$IMX8_HW_VERSION" = "1.1" ] || [ "$IMX8_HW_VERSION" \< "1.1" ]; then
      if [ ! -f "flash_a1.bin" ]; then
        echo "ERROR: no flash_a1.bin for imx8-A bootloader"
        FailExit
      fi
      echo "flash imx8-A bootloader flash_a1.bin"
      echo 0 > /sys/block/mmcblk0boot0/force_ro
      dd if=flash_a1.bin of=/dev/mmcblk0boot0 bs=1K && sync
      echo 1 > /sys/block/mmcblk0boot0/force_ro

      echo 0 > /sys/block/mmcblk0boot1/force_ro
      dd if=flash_a1.bin of=/dev/mmcblk0boot1 bs=1K && sync
      echo 1 > /sys/block/mmcblk0boot1/force_ro

      dd if=flash_a1.bin of=/dev/mmcblk0 bs=1K seek=32 && sync
    else
      echo "ERROR: invalid imx8 version"
      FailExit
    fi
  fi
else
  echo "NOTE: no version.txt get uboot version, do not flash boot"
fi

echo "flash kernel /dev/mmcblk0 offset ${dst_kernel_offset}M, rootfs ${dst_rootfs_part}, app ${dst_appfs_part}, snap ${dst_snap_part}"
echo "update kernel"
dd if=imx8dxl-mars1-bgm-fit.itb of=/dev/mmcblk0 bs=1M seek=${dst_kernel_offset}
echo

echo "tar xjf rootfs.img.bz2"
touch rootfs_unpack
while [ -f rootfs_unpack ]; do
  echo "unpacking rootfs.img..."
  if [ -f rootfs.img ]; then
    ls rootfs.img -lh;
  fi
  sleep 20;
done &
tar xjvf rootfs.img.bz2
if [ $? -ne 0 ]; then
  echo "ERROR: tar rootfs.img"
  rm -rf rootfs_unpack
  FailExit
fi
rm -rf rootfs_unpack
echo

echo "update rootfs"
ls rootfs.img -l
ls rootfs.img -lh
dd if=rootfs.img of=${dst_rootfs_part} bs=1M
if [ $? -ne 0 ]; then
  echo "ERROR: dd rootfs.img"
  rm -rf rootfs.img
  FailExit
fi
echo
rm -f rootfs.img

echo "tar xjf appfs.img.bz2"
touch appfs_unpack
while [ -f appfs_unpack ]; do
  echo "unpacking appfs.img..."
  if [ -f appfs.img ]; then
    ls appfs.img -lh;
  fi
  sleep 20;
done &
tar xjvf appfs.img.bz2
if [ $? -ne 0 ]; then
  echo "ERROR: tar appfs.img"
  rm -rf appfs_unpack
  FailExit
fi
rm -rf appfs_unpack
echo

echo "update appfs"
ls appfs.img -l
ls appfs.img -lh
dd if=appfs.img of=${dst_appfs_part} bs=1M
if [ $? -ne 0 ]; then
  echo "ERROR: dd appfs.img"
  rm -rf appfs.img
  FailExit
fi
echo
rm -f appfs.img
sync

if [ -f $dst_snap_file ] ; then
  echo "unpack snap"
  touch snap_unpack
  while [ -f snap_unpack ]; do
    echo "unpacking $dst_snap_img..."
    if [ -f $dst_snap_img ]; then
      ls $dst_snap_img -lh;
    fi
    sleep 20;
  done &
  tar xjvf $dst_snap_file
  if [ $? -ne 0 ]; then
    echo "ERROR: tar $dst_snap_img"
    rm -rf snap_unpack
    FailExit
  fi
  rm -rf snap_unpack
  echo

  echo "update snap"
  ls $dst_snap_img -l
  ls $dst_snap_img -lh
  dd if=$dst_snap_img of=${dst_snap_part} bs=1M
  if [ $? -ne 0 ]; then
    echo "ERROR: dd $dst_snap_img"
    rm -rf $dst_snap_img
    FailExit
  fi
  echo
  rm -f $dst_snap_img
  sync
else
  echo "erase snap"
  dd if=/dev/zero of=${dst_snap_part} bs=1M count=16
  if [ $? -ne 0 ]; then
    echo "ERROR: erase snap"
    FailExit
  fi
  sync
fi

echo "switch slot to ${next_slot}"
/app/bin/swdl -nw 8 ${next_slot}
if [ $? -ne 0 ]; then
  echo "ERROR: switch slot"
  FailExit
fi
echo

sync

echo "INFO: dd update Success"
echo "end: $(date)"

cp /app/etc/reboot.sh /tmp/jiduer && chmod +x /tmp/jiduer/reboot.sh && runuser -l powerMgr -c '/tmp/jiduer/reboot.sh'
