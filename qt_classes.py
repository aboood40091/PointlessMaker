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

from PyQt5 import QtCore, QtGui, QtWidgets
Qt = QtCore.Qt

if not hasattr(QtWidgets.QGraphicsPixmapItem, 'ItemSendsGeometryChanges'):
    QtWidgets.QGraphicsPixmapItem.ItemSendsGeometryChanges = QtWidgets.QGraphicsPixmapItem.GraphicsItemFlag(0x800)

if not hasattr(QtWidgets.QGraphicsEllipseItem, 'ItemSendsGeometryChanges'):
    QtWidgets.QGraphicsEllipseItem.ItemSendsGeometryChanges = QtWidgets.QGraphicsEllipseItem.GraphicsItemFlag(0x800)

if not hasattr(QtWidgets.QGraphicsRectItem, 'ItemSendsGeometryChanges'):
    QtWidgets.QGraphicsRectItem.ItemSendsGeometryChanges = QtWidgets.QGraphicsRectItem.GraphicsItemFlag(0x800)


class Scene(QtWidgets.QGraphicsScene):
    def __init__(self, *args):
        self.bgbrush = QtGui.QBrush(QtGui.QColor(119, 136, 153))
        QtWidgets.QGraphicsScene.__init__(self, *args)

    def drawBackground(self, painter, rect):
        painter.fillRect(rect, self.bgbrush)

    def drawForeground(self, painter, rect):
        drawLine = painter.drawLine
        GridColor = QtGui.QColor(255, 255, 255, 100)

        startx = rect.x()
        startx -= (startx % 16) + 8
        endx = startx + rect.width() + 16

        starty = rect.y()
        starty -= (starty % 16) + 8
        endy = starty + rect.height() + 16

        x = startx - 16
        while x <= endx:
            x += 16
            painter.setPen(QtGui.QPen(GridColor, 1, Qt.DotLine))
            drawLine(x, starty, x, endy)

        y = starty - 16
        while y <= endy:
            y += 16
            painter.setPen(QtGui.QPen(GridColor, 1, Qt.DotLine))
            drawLine(startx, y, endx, y)

        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        drawRect = QtCore.QRectF(8, -424, 3840, 432)
        painter.setPen(QtGui.QPen(QtGui.QColor(145, 200, 255, 176), 3))
        painter.drawRect(drawRect)


class PixmapItem(QtWidgets.QGraphicsPixmapItem):
    def __init__(self, x, y, *args):
        self.objx = x
        self.objy = y

        QtWidgets.QGraphicsPixmapItem.__init__(self, *args)
        self.setFlag(self.ItemSendsGeometryChanges, True)

    def itemChange(self, change, value):
        if change == QtWidgets.QGraphicsPixmapItem.ItemPositionChange:
            newpos = value

            newpos.setX(int(int((newpos.x() + 16 / 4) / (16 / 2)) * 16 / 2))
            newpos.setY(int(int((newpos.y() + 16 / 4) / (16 / 2)) * 16 / 2))
            
            x = newpos.x()
            y = newpos.y()

            if self.objx+x < 0: newpos.setX(0-self.objx)
            if self.objx+x > 3840: newpos.setX(3840-self.objx)
            if self.objy+y < -432: newpos.setY(-432-self.objy)
            if self.objy+y > 0: newpos.setY(0-self.objy)

            return newpos

        return QtWidgets.QGraphicsPixmapItem.itemChange(self, change, value)


class EllipseItem(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, *args):
        self.objx = args[0]
        self.objy = args[1]

        QtWidgets.QGraphicsEllipseItem.__init__(self, *args)
        self.setFlag(self.ItemSendsGeometryChanges, True)

    def itemChange(self, change, value):
        if change == QtWidgets.QGraphicsEllipseItem.ItemPositionChange:
            newpos = value

            newpos.setX(int(int((newpos.x() + 16 / 4) / (16 / 2)) * 16 / 2))
            newpos.setY(int(int((newpos.y() + 16 / 4) / (16 / 2)) * 16 / 2))
            
            x = newpos.x()
            y = newpos.y()

            if self.objx+x < 0: newpos.setX(0-self.objx)
            if self.objx+x > 3840: newpos.setX(3840-self.objx)
            if self.objy+y < -432: newpos.setY(-432-self.objy)
            if self.objy+y > 0: newpos.setY(0-self.objy)

            return newpos

        return QtWidgets.QGraphicsEllipseItem.itemChange(self, change, value)


class RectItem(QtWidgets.QGraphicsRectItem):
    def __init__(self, *args):
        self.objx = args[0]
        self.objy = args[1]

        QtWidgets.QGraphicsRectItem.__init__(self, *args)
        self.setFlag(self.ItemSendsGeometryChanges, True)

    def itemChange(self, change, value):
        if change == QtWidgets.QGraphicsRectItem.ItemPositionChange:
            newpos = value

            newpos.setX(int(int((newpos.x() + 16 / 4) / (16 / 2)) * 16 / 2))
            newpos.setY(int(int((newpos.y() + 16 / 4) / (16 / 2)) * 16 / 2))
            
            x = newpos.x()
            y = newpos.y()

            if self.objx+x < 0: newpos.setX(0-self.objx)
            if self.objx+x > 3840: newpos.setX(3840-self.objx)
            if self.objy+y < -432: newpos.setY(-432-self.objy)
            if self.objy+y > 0: newpos.setY(0-self.objy)

            return newpos

        return QtWidgets.QGraphicsRectItem.itemChange(self, change, value)
