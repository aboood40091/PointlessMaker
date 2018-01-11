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
from objects import *


class LevelViewWidget(QtWidgets.QGraphicsView):
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
        if event.button() == Qt.RightButton:
            type_ = globals.CurrentObject

            if type_ == -1 or len(globals.Area.objects) == 2600:
                return

            data = 0
            parentFlags = 0

            w, h = [globals.TileWidth] * 2

            if type_ == 0:
                type_ = EditRengaBlock
                pix = globals.Tiles[1]

            elif type_ == 1:
                type_ = EditHatenaBlock
                pix = globals.Tiles[2]

            elif type_ == 2:
                type_ = EditHardBlock
                pix = globals.Tiles[6]

            elif type_ == 3:
                type_ = EditKumoBlock
                pix = globals.Tiles[102]

            elif type_ == 4:
                pix = globals.Tiles[120]
                type_ = EditIceBlock

            elif 4 < type_ < 76:
                data = type_ - 5
                pix = globals.Tiles[184 + data]
                type_ = EditGround

            elif type_ == 76:
                pix = globals.Tiles[7]
                type_ = EditCoin

            elif type_ == 77:
                parentFlags = 0x6000844
                pix = globals.Tiles[256]
                type_ = EditCoin

            elif type_ == 78:
                pix, w, h = globals.mainWindow.paintPipe(2, 2, 0x40)
                type_ = EditDokan

            elif type_ == 79:
                parentFlags = 0x6000800
                pix, w, h = globals.mainWindow.paintPipe(2, 2, 0)
                type_ = EditDokan

            elif type_ == 80:
                parentFlags = 0x6000860
                pix, w, h = globals.mainWindow.paintPipe(2, 2, 0x60)
                type_ = EditDokan

            elif type_ == 81:
                parentFlags = 0x6000820
                pix, w, h = globals.mainWindow.paintPipe(2, 2, 0x20)
                type_ = EditDokan

            elif type_ == 82:
                pix, w, h = globals.mainWindow.paintGroundBox(5, 5, 0)
                type_ = EditGroundBox

            elif type_ == 83:
                pix, w, h = globals.mainWindow.paintGroundBox(5, 5, 1)
                parentFlags = 0x6040840
                type_ = EditGroundBox

            elif type_ == 84:
                pix, w, h = globals.mainWindow.paintGroundBox(5, 5, 2)
                parentFlags = 0x6080840
                type_ = EditGroundBox

            elif type_ == 85:
                pix, w, h = globals.mainWindow.paintGroundGoal(13, 2)
                type_ = EditGroundGoal

            elif type_ == 86:
                pix, w, h = globals.mainWindow.paintGroundStart(8, 2)
                type_ = EditGroundStart

            clicked = globals.mainWindow.graphicsView.mapToScene(event.x(), event.y())

            clickedx = clicked.x()
            clickedy = clicked.y()

            clickedx -= globals.TileWidth // 2
            clickedy -= globals.TileWidth // 2
            clickedx = (clickedx // globals.TileWidth) * globals.TileWidth
            clickedy = (clickedy // globals.TileWidth) * globals.TileWidth
            clickedx += globals.TileWidth // 2
            clickedy += globals.TileWidth // 2

            maxX = 240 * globals.TileWidth
            minY = -27 * globals.TileWidth

            if clickedx < 0:
                clickedx = 0

            elif clickedx > maxX:
                clickedx = maxX

            if clickedy < minY:
                clickedy = minY

            elif clickedy > 0:
                clickedy = 0

            for z in objectsZValues:
                if type_ in objectsZValues[z]:
                    break

            if type_ == EditGroundBox:
                z -= 0x100000000

            item = PixmapItem(type_, clickedx, clickedy, z, w, h, pix, data)

            if parentFlags:
                item.parentFlags = parentFlags

            else:
                item.parentFlags = 0x6000840

            item.childFlags = 0x6000840
            item.childType = -1
            item.linkID = -1
            item.eIndex = -1
            item._1E = -1
            item.cTID = -1

            globals.Area.objects.append(item)
            globals.mainWindow.scene.addItem(item)

        elif event.button() == Qt.LeftButton and QtWidgets.QApplication.keyboardModifiers() == Qt.ShiftModifier:
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


class ObjectPickerWidget(QtWidgets.QListView):
    """
    Widget that shows a list of available objects
    """

    def __init__(self):
        """
        Initializes the widget
        """

        super().__init__()
        self.setFlow(QtWidgets.QListView.LeftToRight)
        self.setLayoutMode(QtWidgets.QListView.SinglePass)
        self.setMovement(QtWidgets.QListView.Static)
        self.setResizeMode(QtWidgets.QListView.Adjust)
        self.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.setWrapping(True)

        self.model = self.ObjectListModel()
        self.setModel(self.model)

        self.setItemDelegate(self.ObjectItemDelegate())

        self.clicked.connect(self.HandleObjReplace)

    @QtCore.pyqtSlot(QtCore.QModelIndex, QtCore.QModelIndex)
    def currentChanged(self, current, previous):
        """
        Throws a signal when the selected object changed
        """
        self.ObjChanged.emit(current.row())

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def HandleObjReplace(self, index):
        """
        Throws a signal when the selected object is used as a replacement
        """
        if QtWidgets.QApplication.keyboardModifiers() == Qt.AltModifier:
            self.ObjReplace.emit(index.row())

    ObjChanged = QtCore.pyqtSignal(int)
    ObjReplace = QtCore.pyqtSignal(int)

    class ObjectItemDelegate(QtWidgets.QAbstractItemDelegate):
        """
        Handles tileset objects and their rendering
        """

        def paint(self, painter, option, index):
            """
            Paints an object
            """
            if option.state & QtWidgets.QStyle.State_Selected:
                painter.fillRect(option.rect, option.palette.highlight())

            p = index.model().data(index, Qt.DecorationRole)
            painter.drawPixmap(option.rect.x() + 2, option.rect.y() + 2, p)
            # painter.drawText(option.rect, str(index.row()))

        def sizeHint(self, option, index):
            """
            Returns the size for the object
            """
            p = index.model().data(index, Qt.UserRole)
            return p

    class ObjectListModel(QtCore.QAbstractListModel):
        """
        Model containing all the objects in a tileset
        """

        def __init__(self):
            """
            Initializes the model
            """
            super().__init__()

            self.ritems = []
            self.itemsize = []

        def rowCount(self, parent=None):
            """
            Required by Qt
            """
            return len(self.ritems)

        def data(self, index, role=Qt.DisplayRole):
            """
            Get what we have for a specific row
            """
            if not index.isValid(): return None
            n = index.row()
            if n < 0: return None
            if n >= len(self.ritems): return None

            if role == Qt.DecorationRole and n < len(self.ritems):
                return self.ritems[n]

            if role == Qt.BackgroundRole:
                return QtWidgets.qApp.palette().base()

            if role == Qt.UserRole and n < len(self.itemsize):
                return self.itemsize[n]

            if role == Qt.ToolTipRole and n < len(self.tooltips):
                return self.tooltips[n]

            return None

        def loadObjects(self):
            self.ritems = []
            self.itemsize = []
            self.tooltips = []

            self.beginResetModel()

            for type_ in TilesetObjects:
                rw, rh = [globals.TileWidth] * 2

                if type_ == EditGround:
                    for i in range(71):
                        pix = globals.Tiles[184 + i]

                        self.ritems.append(pix)
                        self.itemsize.append(QtCore.QSize(rw + 4, rh + 4))
                        self.tooltips.append('%s, type %d' % (objectNames[type_], i + 1))

                    continue

                elif type_ == EditCoin:
                    pix = globals.Tiles[7]

                    self.ritems.append(pix)
                    self.itemsize.append(QtCore.QSize(rw + 4, rh + 4))
                    self.tooltips.append('%s, type 1' % objectNames[type_])

                    pix = globals.Tiles[256]

                    self.ritems.append(pix)
                    self.itemsize.append(QtCore.QSize(rw + 4, rh + 4))
                    self.tooltips.append('%s, type 2' % objectNames[type_])

                    continue

                elif type_ == EditDokan:
                    directions = [0x40, 0, 0x60, 0x20]
                    for i, direction in enumerate(directions):
                        pix, rw, rh = globals.mainWindow.paintPipe(2, 2, direction)

                        self.ritems.append(pix)
                        self.itemsize.append(QtCore.QSize(rw + 4, rh + 4))
                        self.tooltips.append('%s, type %d' % (objectNames[type_], i + 1))

                    continue

                elif type_ == EditGroundBox:
                    for boxType in [0, 1, 2]:
                        pix, rw, rh = globals.mainWindow.paintGroundBox(5, 5, boxType)

                        self.ritems.append(pix)
                        self.itemsize.append(QtCore.QSize(rw + 4, rh + 4))
                        self.tooltips.append('%s, type %d' % (objectNames[type_], boxType + 1))

                    continue

                elif type_ == EditRengaBlock:
                    pix = globals.Tiles[1]

                elif type_ == EditHatenaBlock:
                    pix = globals.Tiles[2]

                elif type_ == EditHardBlock:
                    pix = globals.Tiles[6]

                elif type_ == EditKumoBlock:
                    pix = globals.Tiles[102]

                elif type_ == EditIceBlock:
                    pix = globals.Tiles[120]

                elif type_ == EditGroundGoal:
                    pix, rw, rh = globals.mainWindow.paintGroundGoal(13, 2)

                elif type_ == EditGroundStart:
                    pix, rw, rh = globals.mainWindow.paintGroundStart(8, 2)

                self.ritems.append(pix)
                self.itemsize.append(QtCore.QSize(rw + 4, rh + 4))
                self.tooltips.append('%s' % objectNames[type_])

            self.endResetModel()
