#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# PointlessMaker
# Version 0.2
# Copyright © 2017 MasterVermilli0n/AboodXD

# This file is part of PointlessMaker.

# PointlessMaker is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# PointlessMaker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import struct


class CourseData(struct.Struct):
    def __init__(self):
        super().__init__('>4x2I4xH6BQB7x66s2sx3BH2BI104s12xI')

    def data(self, data, pos):
        (self.version,
         self.checksum,
         self.year,
         self.month,
         self.day,
         self.hour,
         self.minute,
         self.unk1,
         self.unk2,
         self.levelcode,
         self.unk3,
         self.name,
         self.mode,
         self.theme,
         self.unk4,
         self.unk5,
         self.timer,
         self.scroll,
         self.flags,
         self.areaWidth,
         self.miiData,
         self.numObjects) = self.unpack_from(data, pos)

        self.mii = MiiData(self.miiData)


class MiiData(struct.Struct):
    def __init__(self, miiData):
        super().__init__('<IQI6s2xH20sH16sB7x20sI')

        (self.ID,
         self.sysID,
         self.date,
         self.MAC,
         self.opt,
         self.name,
         self.size_,
         self.design,
         self.copying,
         self.unk1,
         self.unk2) = self.unpack_from(miiData, 0)

        (self.country,
         self.uploadFlag) = struct.unpack('>2I', miiData[0x60:])

        self.name = self.u16BytestrByteSwap(self.name)

    def u16BytestrByteSwap(self, bytestr):
        i = 0
        swapped = bytearray()
        while i < len(self.name):
            swapped.append(bytestr[i+1])
            swapped.append(bytestr[i])
            i += 2

        return bytes(swapped)


class Object(struct.Struct):
    def __init__(self):
        super().__init__('>2Ih2b3I2b2h2b')

    def data(self, data, pos):
        (self.x,
         self.z,
         self.y,
         self.w,
         self.h,
         self.parentFlags,
         self.childFlags,
         self.data,
         self.objType,
         self.childType,
         self.linkID,
         self.eIndex,
         self._1E,
         self.cTID) = self.unpack_from(data, pos)
