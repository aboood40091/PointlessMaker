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

import zlib

from PyQt5 import QtGui
from PyQt5.QtCore import Qt

import globals
from items import PixmapItem, RectItem
from obj_names import *
from classes import *


class Area:
    def __init__(self, inb, cdt):
        self.objects = []

        for attr in dir(cdt):
            if not attr.startswith('__') and not callable(getattr(cdt, attr)):
                exec('self.%s = cdt.%s' % (attr, attr))

        mode = self.mode.decode('utf-8')
        theme = self.theme

        self.loadTileset(mode, theme)
        
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
        self.numGoundBoxes = 0
        zMults = []

        pos = 0
        for i in range(self.numObjects):
            obj = Object()
            obj.data(self.objectsBlock, pos)

            pos += obj.size

            rx = obj.x / 160 * globals.TileWidth
            ry = -obj.y / 160 * globals.TileWidth

            # Oh, this game has layers BTW
            # Probably a layer for each object
            # I'll be damned if I add support for layers now
            # Will probably wait for my holiday first
            rz = -obj.z / 16 * globals.TileWidth

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

                    # Get a proper z value
                    ## Get the z multiplier
                    zMult = 1 / ((obj.parentFlags & 0xF) + 4)

                    ## Make the z value lower than any other item
                    rz -= 0xFFFFFFFF
                    rz *= 16

                    ## Multiply by the z multiplier
                    rz *= zMult

                    ## Some shiz that I don't care about explaining
                    self.numGoundBoxes += 1
                    if zMult in zMults:
                        rz *= self.numGoundBoxes

                    else:
                        zMults.append(zMult)

                elif obj.objType == EditGroundGoal:
                    pix, rw, rh = globals.mainWindow.paintGroundGoal(obj.w, obj.h)

                elif obj.objType == EditGroundStart:
                    pix, rw, rh = globals.mainWindow.paintGroundStart(obj.w, obj.h)

                item = PixmapItem(obj.objType, rx, ry, rz, rw, rh, pix, obj.data)

            else:
                item = RectItem(obj.objType, rx, ry, rz, rw, rh, obj.data)

            item.parentFlags = obj.parentFlags
            item.childFlags = obj.childFlags
            item.objType = obj.objType
            item.childType = obj.childType
            item.linkID = obj.linkID
            item.eIndex = obj.eIndex
            item._1E = obj._1E
            item.cTID = obj.cTID

            self.objects.append(item)
            globals.mainWindow.scene.addItem(item)

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
        for obj in globals.Area.objects:
            if obj.type in [EditDokan, EditGroundBox, EditGroundGoal, EditGroundStart]:  # can't save those yet ;(
                continue

            x = obj.realX * 160 / globals.TileWidth
            y = -obj.realY * 160 / globals.TileWidth
            z = -obj.objz * 16 / globals.TileWidth
            y -= (obj.height - globals.TileWidth) * 160 / globals.TileWidth
            w = obj.width // globals.TileWidth
            h = obj.height // globals.TileWidth

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
