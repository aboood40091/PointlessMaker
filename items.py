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

from PyQt5 import QtCore, QtGui, QtWidgets
Qt = QtCore.Qt

if not hasattr(QtWidgets.QGraphicsItem, 'ItemSendsGeometryChanges'):
    QtWidgets.QGraphicsItem.ItemSendsGeometryChanges = QtWidgets.QGraphicsItem.GraphicsItemFlag(0x800)

import globals
from objects import *


class LevelEditorItem(QtWidgets.QGraphicsItem):
    def __init__(self):
        super().__init__()
        self.setFlag(self.ItemSendsGeometryChanges, True)

    def __lt__(self, other):
        return (self.objx * 100000 + self.objy) < (other.objx * 100000 + other.objy)

    def boundingRect(self):
        return self.boundRect

    def delete(self):
        self.scene().update(self.x(), self.y(), self.boundRect.width(), self.boundRect.height())


class PixmapItem(LevelEditorItem):
    def __init__(self, type, x, y, z, w, h, pix, data):
        super().__init__()

        self.objType = type
        self.objx = x
        self.objy = y
        self.objz = z
        self.width = w
        self.height = h
        self.pix = pix
        self.data = data
        self.setZValue(self.objz)

        self.realX = x
        self.realY = y

        self.setFlag(self.ItemIsMovable, True)
        self.setFlag(self.ItemIsSelectable, True)
        self.UpdateRects()

    def SetType(self, type, pix, z):
        self.objType = type
        self.objz = z
        self.pix = pix

        self.setZValue(self.objz)
        self.UpdateRects()
        self.update()

    def itemChange(self, change, value):
        if change == super().ItemPositionChange:
            newpos = value

            newpos.setX(int(newpos.x() / globals.TileWidth) * globals.TileWidth)
            newpos.setY(int(newpos.y() / globals.TileWidth) * globals.TileWidth)
            
            x = newpos.x()
            y = newpos.y()

            maxX = 240 * globals.TileWidth
            minY = -27 * globals.TileWidth

            if self.objx + x < 0:
                newpos.setX(-self.objx)

            elif self.objx + x > maxX:
                newpos.setX(maxX - self.objx)

            if self.objy + y < minY:
                newpos.setY(minY - self.objy)

            elif self.objy + y > 0:
                newpos.setY(-self.objy)

            self.realX = self.objx + newpos.x()
            self.realY = self.objy + newpos.y()

            return newpos

        return super().itemChange(change, value)

    def paint(self, painter, option, widget):
        painter.save()
        painter.drawPixmap(self.objx, self.objy, self.pix)
        painter.restore()

        if self.isSelected():
            painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255), 1, Qt.DotLine))
            painter.drawRect(self.boundRect)
            painter.fillRect(self.boundRect, QtGui.QColor(255, 255, 255, 64))

    def UpdateRects(self):
        self.prepareGeometryChange()

        if self.width <= 0: self.width = globals.TileWidth
        if self.height <= 0: self.height = globals.TileWidth

        self.boundRect = QtCore.QRectF(self.objx, self.objy, self.width, self.height)


class RectItem(LevelEditorItem):
    def __init__(self, type, x, y, z, w, h, data):
        super().__init__()
        self.setZValue(z)

        self.objType = type
        self.objx = x
        self.objy = y
        self.objz = z
        self.width = w
        self.height = h
        self.data = data

        self.realX = x
        self.realY = y

        self.setFlag(self.ItemIsMovable, True)
        self.setFlag(self.ItemIsSelectable, True)
        self.UpdateRects()

        self.font = QtGui.QFont('Tahoma', 7 * (globals.TileWidth / 16))

    def itemChange(self, change, value):
        if change == super().ItemPositionChange:
            newpos = value

            newpos.setX(int(newpos.x() / (globals.TileWidth // 2)) * globals.TileWidth // 2)
            newpos.setY(int(newpos.y() / (globals.TileWidth // 2)) * globals.TileWidth // 2)
            
            x = newpos.x()
            y = newpos.y()

            maxX = 240 * globals.TileWidth
            minY = -27 * globals.TileWidth

            if self.objx + x < 0:
                newpos.setX(-self.objx)

            elif self.objx + x > maxX:
                newpos.setX(maxX - self.objx)

            if self.objy + y < minY:
                newpos.setY(minY - self.objy)

            elif self.objy + y > 0:
                newpos.setY(-self.objy)

            self.realX = self.objx + newpos.x()
            self.realY = self.objy + newpos.y()

            return newpos

        return super().itemChange(change, value)

    def paint(self, painter, option, widget):
        painter.setClipRect(option.exposedRect)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        if self.isSelected():
            painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 92, 196, 240)))
            painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255), 1))

        else:
            painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 92, 196, 120)))
            painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 1))

        painter.drawRoundedRect(self.itemRect, 4 * (globals.TileWidth / 16), 4 * (globals.TileWidth / 16))

        painter.setFont(self.font)
        painter.drawText(self.itemRect, Qt.AlignCenter, str(self.objType))

    def UpdateRects(self):
        self.prepareGeometryChange()

        if self.width <= 0: self.width = globals.TileWidth
        if self.height <= 0: self.height = globals.TileWidth

        self.itemRect = QtCore.QRectF(self.objx + 1 * (globals.TileWidth / 16), self.objy + 1 * (globals.TileWidth / 16),
                                      self.width - 2 * (globals.TileWidth / 16), self.height - 2 * (globals.TileWidth / 16))
        self.boundRect = QtCore.QRectF(self.objx, self.objy, self.width, self.height)


class BorderItem(LevelEditorItem):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.setZValue(50000)

        self.objx = x
        self.objy = y
        self.width = w
        self.height = h
        self.UpdateRects()

        self.dragging = False
        self.dragstartx = -1
        self.dragstarty = -1

    def paint(self, painter, option, widget):
        # painter.setClipRect(option.exposedRect)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        painter.setPen(QtGui.QPen(QtGui.QColor(145, 200, 255, 176), 3 * globals.TileWidth / 24))
        painter.drawRect(self.drawRect)

    def UpdateRects(self):
        self.prepareGeometryChange()

        if self.width <= 0: self.width = globals.TileWidth
        if self.height <= 0: self.height = globals.TileWidth

        self.drawRect = QtCore.QRectF(self.objx + 1 * (globals.TileWidth / 16), self.objy + 1 * (globals.TileWidth / 16),
                                      self.width - 2 * (globals.TileWidth / 16), self.height - 2 * (globals.TileWidth / 16))
        self.boundRect = QtCore.QRectF(self.objx, self.objy, self.width, self.height)
