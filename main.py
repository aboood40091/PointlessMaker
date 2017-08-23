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

import sys

from PyQt5 import QtCore, QtGui, QtWidgets
Qt = QtCore.Qt

from mainwindowui import Ui_MainWindow

from classes import *
from obj_names import *
from qt_classes import *


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.setupUi(self)

        self.items = []

        self.scene = Scene(0, -428, 3856, 440, self)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)

        self.scene.selectionChanged.connect(self.handleSceneSelectionChanged)

        colours = {}
        colours[EditKuribo] = QtGui.QColor(158, 95, 25)
        colours[EditDokan] = QtGui.QColor(182, 237, 57)
        colours[EditTsuta] = QtGui.QColor(52, 190, 48) # vine
        colours[EditSaw] = QtGui.QColor(155, 183, 175)

        filename = QtWidgets.QFileDialog.getOpenFileName(self, "Open Level", '', 'Level file (*.cdt)')[0]

        if filename:
            with open(filename, "rb") as inf:
                inb = inf.read()

            pos = 0

            cdt = CourseData()
            cdt.data(inb, pos)

            pos += cdt.size

            self.mode = cdt.mode.decode('utf-8')
            self.theme = cdt.theme

            self.loadTileset()

            levelname = b''.join(cdt.name.split(b'\x00\x00')).decode('utf-16-be')

            self.setWindowTitle(('%s - MarioUnmaker v0.2' % levelname))

            self.objectList.setRowCount(cdt.numObjects)
            self.objectList.setColumnCount(14)
            self.objectList.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("X"))
            self.objectList.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem("Y"))
            self.objectList.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem("Z"))
            self.objectList.setHorizontalHeaderItem(3, QtWidgets.QTableWidgetItem("Width"))
            self.objectList.setHorizontalHeaderItem(4, QtWidgets.QTableWidgetItem("Height"))
            self.objectList.setHorizontalHeaderItem(5, QtWidgets.QTableWidgetItem("Parent Name"))
            self.objectList.setHorizontalHeaderItem(6, QtWidgets.QTableWidgetItem("Parent Flags"))
            self.objectList.setHorizontalHeaderItem(7, QtWidgets.QTableWidgetItem("Child Object"))
            self.objectList.setHorizontalHeaderItem(8, QtWidgets.QTableWidgetItem("Child Flags"))
            self.objectList.setHorizontalHeaderItem(9, QtWidgets.QTableWidgetItem("Object Data"));
            self.objectList.setHorizontalHeaderItem(10, QtWidgets.QTableWidgetItem("Pipe Link ID"));
            self.objectList.setHorizontalHeaderItem(11, QtWidgets.QTableWidgetItem("Effect Index"));
            self.objectList.setHorizontalHeaderItem(12, QtWidgets.QTableWidgetItem("_1E"));
            self.objectList.setHorizontalHeaderItem(13, QtWidgets.QTableWidgetItem("Child T ID"));

            for i in range(cdt.numObjects):
                obj = Object()
                obj.data(inb, pos)

                pos += obj.size

                rx = obj.x // 10
                ry = -obj.y // 10
                rz = -obj.z // 10
                ry -= (obj.h - 1) * 16
                rw = obj.w * 16
                rh = obj.h * 16
                item = QtWidgets.QGraphicsItem

                noimage = True

                if obj.objType == EditRengaBlock:
                    pi = PixmapItem(rx, ry)
                    pi.setOffset(float(rx), float(ry))
                    pi.setPixmap(self.tiles[1])
                    item = pi
                    noimage = False

                elif obj.objType == EditHatenaBlock:
                    pi = PixmapItem(rx, ry)
                    pi.setOffset(float(rx), float(ry))
                    pi.setPixmap(self.tiles[2])
                    item = pi
                    noimage = False

                elif obj.objType == EditHardBlock:
                    pi = PixmapItem(rx, ry)
                    pi.setOffset(float(rx), float(ry))
                    pi.setPixmap(self.tiles[6])
                    item = pi
                    noimage = False

                elif obj.objType == EditKumoBlock:
                    pi = PixmapItem(rx, ry)
                    pi.setOffset(float(rx), float(ry))
                    pi.setPixmap(self.tiles[102])
                    item = pi
                    noimage = False

                elif obj.objType == EditIceBlock:
                    pi = PixmapItem(rx, ry)
                    pi.setOffset(float(rx), float(ry))
                    pi.setPixmap(self.tiles[120])
                    item = pi
                    noimage = False

                elif obj.objType == EditGround:
                    pi = PixmapItem(rx, ry)
                    pi.setOffset(float(rx), float(ry))
                    pi.setPixmap(self.tiles[184+obj.data])
                    item = pi
                    noimage = False

                elif obj.objType == EditCoin:
                    pi = PixmapItem(rx, ry)
                    pi.setOffset(float(rx), float(ry))
                    if obj.parentFlags & 4 == 4:
                        pi.setPixmap(self.tiles[256])
                    else:
                        pi.setPixmap(self.tiles[7])
                    item = pi
                    noimage = False

                elif obj.objType == EditDokan:
                    pi = PixmapItem(rx, ry)
                    direction = obj.parentFlags & 0x60
                    if direction == 0x40:
                        pi.setOffset(float(rx), float(ry))
                    else:
                        ry += (obj.h - 1) * 16
                        if direction == 0x60:
                            pi.setOffset(float(rx-16), float(ry))
                        else:
                            rx -= (obj.w - 1) * 16
                            if not direction:
                                pi.setOffset(float(rx+16), float(ry))
                            else:
                                pi.setOffset(float(rx), float(ry-16))
                    pix = self.paintPipe(obj.w, obj.h, direction)
                    pi.setPixmap(pix)
                    item = pi
                    noimage = False

                elif obj.objType == EditGroundBox:
                    pi = PixmapItem(rx, ry)
                    type_ = ((obj.parentFlags >> 16) & 0xF) // 4
                    pi.setOffset(float(rx), float(ry))
                    pix = self.paintGroundBox(obj.w, obj.h, type_)
                    pi.setPixmap(pix)
                    item = pi
                    noimage = False

                    zMult = ((obj.parentFlags & 0xF) + 3) // 4
                    if not zMult: zMult = 1
                    rz *= 2*zMult

                elif obj.objType == EditGroundGoal:
                    pi = PixmapItem(rx, ry)
                    pi.setOffset(float(rx), float(ry))
                    pix = self.paintGroundGoal(obj.w, obj.h)
                    pi.setPixmap(pix)
                    item = pi
                    noimage = False

                elif obj.objType == EditGroundStart:
                    pi = PixmapItem(rx, ry)
                    pi.setOffset(float(rx), float(ry))
                    pix = self.paintGroundStart(obj.w, obj.h)
                    pi.setPixmap(pix)
                    item = pi
                    noimage = False

                elif obj.objType == EditKuribo:
                    ei = EllipseItem(rx, ry, rw, rh)
                    ei.setBrush(colours[EditKuribo])
                    item = ei

                elif obj.objType == EditSaw:
                    ei = EllipseItem(rx, ry, rw, rh)
                    ei.setBrush(colours[EditSaw])
                    item = ei

                elif obj.objType == EditTsuta:
                    ri = RectItem(rx + 8, ry, rw - 16, rh)
                    ri.setBrush(colours[EditTsuta])
                    item = ri

                elif obj.objType == EditPoo: # wrench
                    ri = RectItem(rx, ry, rw, rh)
                    ri.setBrush(QtGui.QColor(158, 95, 25))
                    item = ri

                elif obj.objType == EditDoor:
                    ri = RectItem(rx, ry, rw, rh)
                    ri.setBrush(QtGui.QColor(192, 187, 65))
                    item = ri

                elif obj.objType == EditLift:
                    ri = RectItem(rx, ry, rw, rh)
                    ri.setBrush(QtGui.QColor(192, 187, 65))
                    item = ri

                else:
                    ri = RectItem(rx, ry, rw, rh)
                    if obj.objType in colours:
                        ri.setBrush(colours[obj.objType])
                    else:
                        ri.setBrush(Qt.magenta)
                    item = ri

                if noimage:
                    text = QtWidgets.QGraphicsSimpleTextItem(("" if obj.objType == -1 else str(obj.objType)), item)
                    text.setPos(rx + 2, ry + 2)

                item.setToolTip(hex(obj.data))

                item.setZValue(rz)
                item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
                item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
                self.scene.addItem(item)
                self.items.append(item)

                self.objectList.setItem(i, 0, QtWidgets.QTableWidgetItem(str(obj.x//10)))
                self.objectList.setItem(i, 1, QtWidgets.QTableWidgetItem(str(obj.y//10)))
                self.objectList.setItem(i, 2, QtWidgets.QTableWidgetItem(str(obj.z//10)))
                self.objectList.setItem(i, 3, QtWidgets.QTableWidgetItem(str(obj.w)))
                self.objectList.setItem(i, 4, QtWidgets.QTableWidgetItem(str(obj.h)))
                self.objectList.setItem(i, 5, QtWidgets.QTableWidgetItem("" if obj.objType == -1 else objectNames[obj.objType]))
                self.objectList.setItem(i, 6, QtWidgets.QTableWidgetItem("" if obj.parentFlags == -1 else hex(obj.parentFlags)));
                self.objectList.setItem(i, 7, QtWidgets.QTableWidgetItem("" if obj.childType == -1 else objectNames[obj.childType]))
                self.objectList.setItem(i, 8, QtWidgets.QTableWidgetItem("" if obj.childFlags == -1 else hex(obj.childFlags)))
                self.objectList.setItem(i, 9, QtWidgets.QTableWidgetItem(hex(obj.data)))
                self.objectList.setItem(i, 10, QtWidgets.QTableWidgetItem("" if obj.linkID == -1 else str(obj.linkID)))
                self.objectList.setItem(i, 11, QtWidgets.QTableWidgetItem("" if obj.eIndex == -1 else str(obj.eIndex)))
                self.objectList.setItem(i, 12, QtWidgets.QTableWidgetItem("" if obj._1E == -1 else str(obj._1E)))
                self.objectList.setItem(i, 13, QtWidgets.QTableWidgetItem("" if obj.cTID == -1 else str(obj.cTID)))


    def handleSceneSelectionChanged(self):
        items = self.scene.selectedItems()
        if len(items) == 1:
            index = self.items.index(items[0])
            #self.objectList.setCurrentRow(index)
            self.objectList.setCurrentCell(index, 0)


    def loadTileset(self):
        TileWidths = {"M1": 16, "M3": 16, "MW": 16, "WU": 64}

        themes = {0: "plain", 1: "underground", 2: "castle", 3: "airship", 4: "water", 5: "hauntedhouse"}

        TileWidth = TileWidths[self.mode]

        Tileset = QtGui.QPixmap('tilesets/%s_Field_%s.png' % (self.mode, themes[self.theme]))
        self.tiles = []
        xcount = Tileset.width() // TileWidth
        ycount = Tileset.height() // TileWidth
        sourcex = 0
        sourcey = 0

        for y in range(ycount):
            for x in range(xcount):
                if self.mode == "WU":
                    bmp = Tileset.copy(sourcex + 2, sourcey + 2, TileWidth - 4, TileWidth - 4).scaledToWidth(16, Qt.SmoothTransformation)
                else:
                    bmp = Tileset.copy(sourcex, sourcey, TileWidth, TileWidth)
                self.tiles.append(bmp)
                sourcex += TileWidth
            sourcex = 0
            sourcey += TileWidth


    def paintPipe(self, w, h, direction):
        pix = QtGui.QPixmap(w*16, h*16)
        pix.fill(Qt.transparent)
        painter = QtGui.QPainter(pix)

        top = True

        if direction in [0x40, 0x60]:
            ys = {0x60: list(reversed(range(h))), 0x40: range(h)}

            for y in ys[direction]:
                for x in range(w):
                    realX = x
                    while realX > 1:
                        realX -= 2
                    if top:
                        if direction == 0x40: # Up
                            painter.drawPixmap(16*x, 16*y, self.tiles[14+1*realX])
                        else: # Down
                            painter.drawPixmap(16*x, 16*y, self.tiles[46+1*realX])

                    else:
                        painter.drawPixmap(16*x, 16*y, self.tiles[30+1*realX])
                top = False

        elif direction in [0, 0x20]:
            xs = {0: list(reversed(range(w))), 0x20: range(w)}

            for x in xs[direction]:
                for y in range(h):
                    realY = y
                    while realY > 1:
                        realY -= 2
                    if top:
                        if not direction: # Right
                            painter.drawPixmap(16*x, 16*y, self.tiles[13+16*realY])
                        else: # Left
                            painter.drawPixmap(16*x, 16*y, self.tiles[11+16*realY])

                    else:
                        painter.drawPixmap(16*x, 16*y, self.tiles[12+16*realY])
                top = False

        painter.end()

        return pix


    def paintGroundBox(self, w, h, type_):
        pix = QtGui.QPixmap(w*16, h*16)
        pix.fill(Qt.transparent)
        painter = QtGui.QPainter(pix)

        # Top
        if 0 < w < 3:
            painter.drawPixmap(0, 0, 16, 16, self.tiles[55+3*type_])
            if w > 1:
                painter.drawPixmap(16, 0, 16, 16, self.tiles[57+3*type_])
        elif w:
            painter.drawPixmap(0, 0, 16, 16, self.tiles[55+3*type_])
            painter.drawTiledPixmap(16, 0, (w-2)*16, 16, self.tiles[56+3*type_])
            painter.drawPixmap(16+(w-2)*16, 0, 16, 16, self.tiles[57+3*type_])

        # Middle
        l1 = [71, 87]
        l2 = [72, 88]
        l3 = [73, 89]
        if 0 < w < 3:
            for y in range(1, h-1):
                realY = y-1
                while realY > 1:
                    realY -= 2
                painter.drawPixmap(0, 16*y, 16, 16, self.tiles[l1[realY]+3*type_])
                if w > 1:
                    painter.drawPixmap(16, 16*y, 16, 16, self.tiles[l3[realY]+3*type_])
        elif w:
            for y in range(1, h-1):
                realY = y-1
                while realY > 1:
                    realY -= 2
                painter.drawPixmap(0, 16*y, 16, 16, self.tiles[l1[realY]+3*type_])
                for x in range(1, w-1):
                    realX = x-1
                    while realX > 1:
                        realX -= 2
                    if realX ==  realY:
                        painter.drawTiledPixmap(16*x, 16*y, 16, 16, self.tiles[l2[0]+3*type_])
                    else:
                        painter.drawTiledPixmap(16*x, 16*y, 16, 16, self.tiles[l2[1]+3*type_])
                painter.drawPixmap(16+((w-2)*16), 16*y, 16, 16, self.tiles[l3[realY]+3*type_])

        # Bottom
        if 0 < w < 3:
            painter.drawPixmap(0, (h-1)*16, 16, 16, self.tiles[103+3*type_])
            if w > 1:
                painter.drawPixmap(16, (h-1)*16, 16, 16, self.tiles[105+3*type_])
        elif w:
            painter.drawPixmap(0, (h-1)*16, 16, 16, self.tiles[103+3*type_])
            painter.drawTiledPixmap(16, (h-1)*16, (w-2)*16, 16, self.tiles[104+3*type_])
            painter.drawPixmap(16+(w-2)*16, (h-1)*16, 16, 16, self.tiles[105+3*type_])

        painter.end()

        return pix


    def paintGroundStart(self, w, h):
        w -= 3
        pix = QtGui.QPixmap(w*16, h*16)
        pix.fill(Qt.transparent)
        painter = QtGui.QPainter(pix)

        edge = True

        for x in list(reversed(range(w))):
            for y in range(h):
                if edge:
                    if not y:
                        painter.drawPixmap(16*x, 16*y, self.tiles[122])
                    else:
                        painter.drawPixmap(16*x, 16*y, self.tiles[138])

                else:
                    if not y:
                        painter.drawPixmap(16*x, 16*y, self.tiles[121])
                    else:
                        painter.drawPixmap(16*x, 16*y, self.tiles[137])
            edge = False

        painter.end()

        return pix


    def paintGroundGoal(self, w, h):
        w -= 3
        pix = QtGui.QPixmap(w*16, h*16)
        pix.fill(Qt.transparent)
        painter = QtGui.QPainter(pix)

        edge = True

        for x in range(w):
            for y in range(h):
                if edge:
                    if not y:
                        painter.drawPixmap(16*x, 16*y, self.tiles[123])
                    else:
                        painter.drawPixmap(16*x, 16*y, self.tiles[139])

                else:
                    if not y:
                        painter.drawPixmap(16*x, 16*y, self.tiles[124])
                    else:
                        painter.drawPixmap(16*x, 16*y, self.tiles[140])
            edge = False

        painter.end()

        return pix


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
