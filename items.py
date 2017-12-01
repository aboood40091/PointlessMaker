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

from obj_names import *
import globals


class LevelEditorItem(QtWidgets.QGraphicsItem):
    positionChanged = None
    autoPosChange = False

    def __init__(self):
        super().__init__()
        self.setFlag(self.ItemSendsGeometryChanges, True)

    def __lt__(self, other):
        return (self.objx * 100000 + self.objy) < (other.objx * 100000 + other.objy)

    def itemChange(self, change, value):
        if change == QtWidgets.QGraphicsRectItem.ItemPositionChange:
            newpos = value

            newpos.setX(int(int((newpos.x() + globals.TileWidth / 4) / (globals.TileWidth / 2)) * globals.TileWidth / 2))
            newpos.setY(int(int((newpos.y() + globals.TileWidth / 4) / (globals.TileWidth / 2)) * globals.TileWidth / 2))
            
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

            if newpos.x() != 0:
                self.realX = self.objx + newpos.x()

            if newpos.y() != 0:
                self.realY = self.objy + newpos.y()

            return newpos

        return QtWidgets.QGraphicsItem.itemChange(self, change, value)

    def getFullRect(self):
        return self.boundRect.translated(self.pos())

    def UpdateListItem(self, updateTooltipPreview=False):
        if not hasattr(self, 'listitem'): return
        if self.listitem is None: return

        if updateTooltipPreview:
            # It's just like Qt to make this overly complicated. XP
            img = self.renderInLevelIcon()
            byteArray = QtCore.QByteArray()
            buf = QtCore.QBuffer(byteArray)
            img.save(buf, 'PNG')
            byteObj = bytes(byteArray)
            b64 = base64.b64encode(byteObj).decode('utf-8')

            self.listitem.setToolTip('<img src="data:image/png;base64,' + b64 + '" />')

        self.listitem.setText(self.ListString())

    def renderInLevelIcon(self):
        # Constants:
        # Maximum size of the preview (it will be shrunk if it exceeds this)
        maxSize = QtCore.QSize(256, 256)
        # Percentage of the size to use for margins
        marginPct = 0.75
        # Maximum margin (24 = 1 block)
        maxMargin = 96

        # Get the full bounding rectangle
        br = self.getFullRect()

        # Expand the rect to add extra margins around the edges
        marginX = br.width() * marginPct
        marginY = br.height() * marginPct
        marginX = min(marginX, maxMargin)
        marginY = min(marginY, maxMargin)
        br.setX(br.x() - marginX)
        br.setY(br.y() - marginY)
        br.setWidth(br.width() + marginX)
        br.setHeight(br.height() + marginY)

        # Take the screenshot
        ScreenshotImage = QtGui.QImage(br.width(), br.height(), QtGui.QImage.Format_ARGB32)
        ScreenshotImage.fill(Qt.transparent)

        RenderPainter = QtGui.QPainter(ScreenshotImage)
        globals.mainWindow.scene.render(
            RenderPainter,
            QtCore.QRectF(0, 0, br.width(), br.height()),
            br,
        )
        RenderPainter.end()

        # Shrink it if it's too big
        final = ScreenshotImage
        if ScreenshotImage.width() > maxSize.width() or ScreenshotImage.height() > maxSize.height():
            final = ScreenshotImage.scaled(
                maxSize,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )

        return final

    def boundingRect(self):
        return self.boundRect

    def delete(self):
        self.scene().update(self.x(), self.y(), self.boundRect.width(), self.boundRect.height())


class PixmapItem(LevelEditorItem):
    def __init__(self, type, x, y, z, w, h, pix, data):
        super().__init__()

        self.type = type
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

    def SetType(self, type, pix):
        self.type = type
        self.pix = pix
        self.update()

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

        self.type = type
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
        painter.drawText(self.itemRect, Qt.AlignCenter, str(self.type))

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
        """
        Paints the zone on screen
        """
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

    def itemChange(self, change, value):
        return QtWidgets.QGraphicsItem.itemChange(self, change, value)
