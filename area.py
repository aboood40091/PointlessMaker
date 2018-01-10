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

import math
import zlib

from PyQt5 import QtGui
from PyQt5.QtCore import Qt

import globals
from items import PixmapItem, RectItem
from objects import *
from structs import *


class Area:
    def __init__(self, inb, cdt, bom):
        self.objects = []

        for attr in dir(cdt):
            if not attr.startswith('__') and not callable(getattr(cdt, attr)):
                exec('self.%s = cdt.%s' % (attr, attr))

        self.bom = bom

        mode = self.mode.decode('utf-8')
        theme = self.theme

        self.loadTileset(mode, theme)

        globals.mainWindow.objPicker.model.loadObjects()
        
        self.objectsBlock = inb[0xF0:0x145F0]
        self.effectsBlock = inb[0x145F0:0x15000]

        self.loadObjects()

    def loadTileset(self, mode, theme):
        globals.Tiles = []

        widths = {"M1": 16, "M3": 16, "MW": 16, "WU": 64}
        themes = {0: "plain", 1: "underground", 2: "castle", 3: "airship", 4: "water", 5: "hauntedhouse"}

        width = widths[mode]

        Tileset = QtGui.QPixmap('tilesets/%s_Field_%s.png' % (mode, themes[theme]))
        xcount = Tileset.width() // width
        ycount = Tileset.height() // width
        sourcex = 0
        sourcey = 0

        for y in range(ycount):
            for x in range(xcount):
                if mode == "WU":
                    if globals.TileWidth != 60:
                        bmp = Tileset.copy(sourcex + 2, sourcey + 2,
                                           width - 4, width - 4).scaledToWidth(globals.TileWidth, Qt.SmoothTransformation)

                    else:
                        bmp = Tileset.copy(sourcex + 2, sourcey + 2, width - 4, width - 4)

                else:
                    if globals.TileWidth != width:
                        bmp = Tileset.copy(sourcex, sourcey,
                                           width, width).scaledToWidth(globals.TileWidth, Qt.SmoothTransformation)

                    else:
                        bmp = Tileset.copy(sourcex, sourcey, width, width)

                globals.Tiles.append(bmp)
                sourcex += width

            sourcex = 0
            sourcey += width

    def loadObjects(self):
        pos = (self.numObjects - 1) * 0x20
        for _ in range(self.numObjects):
            obj = Object(self.bom)
            obj.data(self.objectsBlock, pos)
            pos -= 0x20

            rx = obj.x / 160 * globals.TileWidth
            ry = -obj.y / 160 * globals.TileWidth

            # Oh, this game has layers BTW
            rz = obj.z

            if 0 <= rz < 11740:
                rz = 0

            elif 11740 <= rz < 13000:
                rz = 11740

            elif 13000 <= rz < 23010:
                rz = 13000

            elif 23010 <= rz < 44000:
                rz = 23010

            elif 44000 <= rz < 48010:
                rz = 44000

            elif 48010 <= rz < 59990:
                rz = 48010

            elif 59990 <= rz < 62600:
                rz = 59990

            elif 62600 <= rz < 72140:
                rz = 62600

            elif 72140 <= rz < 92670:
                rz = 72140

            elif 92670 <= rz < 93540:
                rz = 92670

            elif 93540 <= rz < 4294897396:
                rz = 93540

            elif 4294897396 <= rz < 4294907296:
                rz = 4294897396

            elif 4294907296 <= rz < 4294910396:
                rz = 4294907296

            elif 4294910396 <= rz < 4294910496:
                rz = 4294910396

            elif 4294910496 <= rz < 4294911506:
                rz = 4294910496

            elif 4294911506 <= rz < 4294916516:
                rz = 4294911506

            else:
                rz = 4294916516

            ry -= (obj.h - 1) * globals.TileWidth
            rw = obj.w * globals.TileWidth
            rh = obj.h * globals.TileWidth

            if obj.objType in TilesetObjects:
                if obj.objType == EditRengaBlock:
                    pix = globals.Tiles[1]

                elif obj.objType == EditHatenaBlock:
                    pix = globals.Tiles[2]

                elif obj.objType == EditHardBlock:
                    pix = globals.Tiles[6]

                elif obj.objType == EditKumoBlock:
                    pix = globals.Tiles[102]

                elif obj.objType == EditIceBlock:
                    pix = globals.Tiles[120]

                elif obj.objType == EditGround:
                    pix = globals.Tiles[184 + obj.data]

                elif obj.objType == EditCoin:
                    if obj.parentFlags & 4 == 4:
                        pix = globals.Tiles[256]

                    else:
                        pix = globals.Tiles[7]

                elif obj.objType == EditDokan:
                    direction = obj.parentFlags & 0x60

                    if direction != 0x40:
                        ry += (obj.h - 1) * globals.TileWidth

                        if direction == 0x60:
                            rx -= globals.TileWidth

                        else:
                            rx -= (obj.w - 1) * globals.TileWidth

                            if not direction:
                                rx += globals.TileWidth

                            else:
                                rx -= (obj.h - 2) * globals.TileWidth
                                ry -= globals.TileWidth

                    pix, rw, rh = globals.mainWindow.paintPipe(obj.w, obj.h, direction)

                elif obj.objType == EditGroundBox:
                    type_ = ((obj.parentFlags >> 16) & 0xF) // 4
                    pix, rw, rh = globals.mainWindow.paintGroundBox(obj.w, obj.h, type_)

                    rz -= 0x100000000

                elif obj.objType == EditGroundGoal:
                    pix, rw, rh = globals.mainWindow.paintGroundGoal(obj.w, obj.h)

                elif obj.objType == EditGroundStart:
                    pix, rw, rh = globals.mainWindow.paintGroundStart(obj.w, obj.h)

                # Snap to grid
                rx -= globals.TileWidth // 2
                ry -= globals.TileWidth // 2
                rx = math.ceil(rx / globals.TileWidth) * globals.TileWidth
                ry = math.ceil(ry / globals.TileWidth) * globals.TileWidth
                rx += globals.TileWidth // 2
                ry += globals.TileWidth // 2

                item = PixmapItem(obj.objType, rx, ry, rz, rw, rh, pix, obj.data)

            else:
                item = RectItem(obj.objType, rx, ry, rz, rw, rh, obj.data)

            item.parentFlags = obj.parentFlags
            item.childFlags = obj.childFlags
            item.childType = obj.childType
            item.linkID = obj.linkID
            item.eIndex = obj.eIndex
            item._1E = obj._1E
            item.cTID = obj.cTID

            self.objects.append(item)
            globals.mainWindow.scene.addItem(item)

        self.objects = list(reversed(self.objects))

    def save(self):
        self.saveObjectsBlock()

        courseBuffer = bytearray()

        courseStruct = CourseData()
        courseBuffer += courseStruct.pack(
            self.version,
            0,  # to be calculated and replaced later on
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
            self.numObjects,
            )

        courseBuffer += self.objectsBlock
        courseBuffer += self.effectsBlock

        self.checksum = zlib.crc32(courseBuffer[16:]) % (1 << 32)

        courseBuffer[8:12] = self.checksum.to_bytes(4, "big")

        return courseBuffer

    def saveObjectsBlock(self):
        buffer = bytearray()

        objects_count = 0
        numGoundBoxes = 0
        for obj in reversed(self.objects):
            rw, rh, rx, ry, rz = obj.width, obj.height, obj.realX, obj.realY, obj.objz

            if obj.objType == EditDokan:
                direction = obj.parentFlags & 0x60

                if direction in [0x40, 0x60]:
                    rw, rh = (obj.width, obj.height)

                else:
                    rw, rh = (obj.height, obj.width)

                if direction != 0x40:
                    ry -= obj.height - globals.TileWidth

                    if direction == 0x60:
                        rx -= globals.TileWidth

                    else:
                        rx -= rw - globals.TileWidth

                        if not direction:
                            rx += globals.TileWidth

                        else:
                            rx -= rh - globals.TileWidth * 2
                            ry -= globals.TileWidth

            elif obj.objType == EditGroundBox:
                rz += 0x100000000

            elif obj.objType in [EditGroundGoal, EditGroundStart]:
                rw += globals.TileWidth * 3

            x = rx * 160 / globals.TileWidth
            y = -ry * 160 / globals.TileWidth
            z = rz
            y -= (rh - globals.TileWidth) * 160 / globals.TileWidth
            w = rw // globals.TileWidth
            h = rh // globals.TileWidth

            x = int(x)
            y = int(y)
            z = int(z)

            """
            print(type(x))
            print(type(z))
            print(type(y))
            print(type(w))
            print(type(h))
            print(type(obj.parentFlags))
            print(type(obj.childFlags))
            print(type(obj.data))
            print(type(obj.objType))
            print(type(obj.childType))
            print(type(obj.linkID))
            print(type(obj.eIndex))
            print(type(obj._1E))
            print(type(obj.cTID))
            """

            objStruct = Object()
            buffer += objStruct.pack(
                x,
                z,
                y,
                w,
                h,
                obj.parentFlags,
                obj.childFlags,
                obj.data,
                obj.objType,
                obj.childType,
                obj.linkID,
                obj.eIndex,
                obj._1E,
                obj.cTID,
                )

            objects_count += 1

        self.numObjects = objects_count

        buffer += b'\0' * 0x20 * (2600-objects_count)
        self.objectsBlock = buffer
