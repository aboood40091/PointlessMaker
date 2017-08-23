#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# MarioUnmaker
# Version 0.2
# Copyright © 2015 Treeki, 2017 Stella/AboodXD

# This file is part of MarioUnmaker.

# MarioUnmaker is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# MarioUnmaker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import struct


class CourseData(struct.Struct):
    def __init__(self):
        super().__init__('>QI4xH6BQB7x64s2x2s4BH2BI96B2I12xI')

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
         self.unk3,
         self.unk4,
         self.name,
         self.mode,
         self.unk5,
         self.theme,
         self.unk6,
         self.unk7,
         self.timer,
         self.scroll,
         self.unk8,
         self.zoneWidth,
         self.unk9,
         self.unk10,
         self.unk11,
         self.unk12,
         self.unk13,
         self.unk14,
         self.unk15,
         self.unk16,
         self.unk17,
         self.unk18,
         self.unk19,
         self.unk20,
         self.unk21,
         self.unk22,
         self.unk23,
         self.unk24,
         self.unk25,
         self.unk26,
         self.unk27,
         self.unk28,
         self.unk29,
         self.unk30,
         self.unk31,
         self.unk32,
         self.unk33,
         self.unk34,
         self.unk35,
         self.unk36,
         self.unk37,
         self.unk38,
         self.unk39,
         self.unk40,
         self.unk41,
         self.unk42,
         self.unk43,
         self.unk44,
         self.unk45,
         self.unk46,
         self.unk47,
         self.unk48,
         self.unk49,
         self.unk50,
         self.unk51,
         self.unk52,
         self.unk53,
         self.unk54,
         self.unk55,
         self.unk56,
         self.unk57,
         self.unk58,
         self.unk59,
         self.unk60,
         self.unk61,
         self.unk62,
         self.unk63,
         self.unk64,
         self.unk65,
         self.unk66,
         self.unk67,
         self.unk68,
         self.unk69,
         self.unk70,
         self.unk71,
         self.unk72,
         self.unk73,
         self.unk74,
         self.unk75,
         self.unk76,
         self.unk77,
         self.unk78,
         self.unk79,
         self.unk80,
         self.unk81,
         self.unk82,
         self.unk83,
         self.unk84,
         self.unk85,
         self.unk86,
         self.unk87,
         self.unk88,
         self.unk89,
         self.unk90,
         self.unk91,
         self.unk92,
         self.unk93,
         self.unk94,
         self.unk95,
         self.unk96,
         self.unk97,
         self.unk98,
         self.unk99,
         self.unk100,
         self.unk101,
         self.unk102,
         self.unk103,
         self.unk104,
         self.unk105,
         self.unk106,
         self.numObjects) = self.unpack_from(data, pos)


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
