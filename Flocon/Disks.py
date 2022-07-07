#!/usr/bin/env python
#
# Disk parser for Flocon
#
from dataclasses import dataclass
import re
import subprocess
import shlex
import sys

_size = {'T' : 1e12,'t' : 1e12, 'G' : 1e9 ,'g' : 1e9 , 'M' : 1e6, 'm' : 1e6, 'K' : 1e3,  'k' : 1e3 }

def _reprSize(size : int) :
    if size > 1e12 :
        return str(float(size)/1e12) + 'T'
    elif size > 1e9 :
        return str(float(size)/1e9) + 'G'
    elif size > 1e6 :
        return str(float(size)/1e6) + 'M'
    elif size > 1e3 :
        return str(float(size)/1e3) + 'K'
    else :
        return str(size)

@dataclass
class Partition:
    drive : str
    partnum :  int
    size : int
    def __repr__(self) -> str:
        return self.drive + str(self.partnum) + "\n   drive :" + self.drive + "\n   partidx:" + str(self.partnum) + "\n   size:"+ _reprSize(self.size)

@dataclass
class PrimaryPartition(Partition):
    bootable : bool
    def __repr__(self) -> str:
        return Partition.__repr__(self) +  "\n   bootable :" + {True:"yes", False:"no"}[self.bootable]

# version of BlockDevice for partitions
@dataclass
class LVMPartition(Partition):
    vggroup : str
    lvname : str
    dmpath : str
    def __repr__(self) -> str:
        return Partition.__repr__(self) +  "\n   vg name : " + self.vggroup + "\n   lvname : " + self.lvname + "\n   dmpath : " + self.dmpath
    

# parse fdisk output
def _parse_fdisk(fdisk_output):
    result = []
    partidx = 0
    for line in fdisk_output.split("\n"):
        if not line.startswith("/"):
            partidx = 0
            continue
        partidx += 1
        parts = line.split()
        name = parts[0]
        drive = re.search(r'([\S\d]+)\d\b', name).group(1)
        if parts[1] == "*":
            bootable = True
            del parts[1]
        else:
            bootable = False
        g = re.search(r'([\d.,]+)([TGMkK])\b', parts[4])
        size = int(float(g.group(1).replace(',','.')) * _size[g.group(2)])
        type = " ".join(parts[5:])
        result.append(PrimaryPartition(drive, partidx,size, bootable))
    return result


def _parse_vgdisplay(lvdisplay_output):
    result = []
    lines = lvdisplay_output.split("\n")
    partidx = 0
    vgname = ""
    lines.pop(0)
    for line in lines:
        g = re.findall(r'([^\s]+)', line)
        if len(g) != 5 :
            break
        if g[0] != vgname :
            partidx = 0
        else :
            partidx += 1
        vgname = g[0]
        lvname = g[1]
        sizerg = re.search(r'([\d.,]+)([TGMkK])\b', g[2])
        size = int(float(sizerg.group(1).replace(',','.')) * _size[sizerg.group(2)])
        lvpath = g[3]
        dmpath = g[4]
        result.append(LVMPartition(lvpath, partidx,size, vgname, lvname, dmpath))
    return result

#
#   Get partitions infos from Fdisk
#
def getPrimaryPartitions():
    proc = subprocess.Popen(shlex.split("pkexec fdisk -l"),
                            stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    fdisk_output, fdisk_error = proc.communicate()
    fdisk_output = fdisk_output.decode(sys.stdout.encoding)
    return _parse_fdisk(fdisk_output)

#
#   Get LVM infos from vgdisplay
#
def getLVM2Partitions():
    proc = subprocess.Popen(shlex.split("pkexec lvdisplay -C --units H -o vg_name,lv_name,size,lv_path,lv_dm_path"),
                            stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    vgdisplay_output, fdisk_error = proc.communicate()
    vgdisplay_output = vgdisplay_output.decode(sys.stdout.encoding)
    return _parse_vgdisplay(vgdisplay_output)
        
# todo : ask pkexec only once
# primary   = getPrimaryPartitions()
# secondary = getLVM2Partitions()