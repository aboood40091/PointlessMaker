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

import globals
from items import *


class LevelViewWidget(QtWidgets.QGraphicsView):
    repaint = QtCore.pyqtSignal()
    dragstamp = False

    def __init__(self, scene, parent):
        super().__init__(scene, parent)

        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
        self.setMouseTracking(True)
        self.YScrollBar = QtWidgets.QScrollBar(Qt.Vertical, parent)
        self.XScrollBar = QtWidgets.QScrollBar(Qt.Horizontal, parent)
        self.setVerticalScrollBar(self.YScrollBar)
        self.setHorizontalScrollBar(self.XScrollBar)

        self.currentobj = None

        self.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and QtWidgets.QApplication.keyboardModifiers() == Qt.ShiftModifier:
            pos = self.mapToScene(event.x(), event.y())
            addsel = globals.mainWindow.scene.items(pos)
            for i in addsel:
                if (int(i.flags()) & i.ItemIsSelectable) != 0:
                    i.setSelected(not i.isSelected())
                    break

        else:
            super().mousePressEvent(event)

    def drawForeground(self, painter, rect):
        if globals.GridShown:
            drawLine = painter.drawLine
            GridColor = QtGui.QColor(255, 255, 255, 100)

            startx = rect.x()
            startx -= (startx % globals.TileWidth) + globals.TileWidth // 2
            endx = startx + rect.width() + globals.TileWidth

            starty = rect.y()
            starty -= (starty % globals.TileWidth) + globals.TileWidth // 2
            endy = starty + rect.height() + globals.TileWidth

            x = startx - globals.TileWidth

            while x <= endx:
                x += globals.TileWidth
                painter.setPen(QtGui.QPen(GridColor, 1, Qt.DotLine))
                drawLine(x, starty, x, endy)

            y = starty - globals.TileWidth

            while y <= endy:
                y += globals.TileWidth
                painter.setPen(QtGui.QPen(GridColor, 1, Qt.DotLine))
                drawLine(startx, y, endx, y)

        painter.setRenderHint(QtGui.QPainter.Antialiasing)


class Scene(QtWidgets.QGraphicsScene):
    def __init__(self, *args):
        self.bgbrush = QtGui.QBrush(QtGui.QColor(119, 136, 153))
        super().__init__(*args)

    def drawBackground(self, painter, rect):
        painter.fillRect(rect, self.bgbrush)
