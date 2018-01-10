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

import sys
import zlib

from PyQt5 import QtCore, QtGui, QtWidgets
Qt = QtCore.Qt

from area import *
import globals
from items import *
from objects import *
from structs import *
from widgets import *

EditorVersion = '0.2'


class MainWindow(QtWidgets.QMainWindow):
    def CreateAction(self, shortname, function, icon, text, statustext, shortcut, toggle=False):
        """
        Helper function to create an action
        From Miyamoto
        """
        if icon is not None:
            act = QtWidgets.QAction(icon, text, self)

        else:
            act = QtWidgets.QAction(text, self)

        if shortcut is not None:
            act.setShortcut(shortcut)

        if statustext is not None:
            act.setStatusTip(statustext)

        if toggle:
            act.setCheckable(True)

        if function is not None:
            act.triggered.connect(function)

        self.actions[shortname] = act

    def __init__(self):
        super().__init__(None)
        self.setWindowTitle('PointlessMaker v0.2')
        self.setUnifiedTitleAndToolBarOnMac(True)

        self.UpdateFlag = False
        self.selObj = None
        self.CurrentSelection = []

        self.scene = Scene(0, -(27 * globals.TileWidth), 241 * globals.TileWidth, 28 * globals.TileWidth, self)
        self.scene.setItemIndexMethod(QtWidgets.QGraphicsScene.NoIndex)
        self.scene.selectionChanged.connect(self.handleSceneSelectionChanged)

        self.graphicsView = LevelViewWidget(self.scene, self)
        self.graphicsView.centerOn(0, -(26.5 * globals.TileWidth))

        self.setCentralWidget(self.graphicsView)

        self.selAllShort = QtWidgets.QShortcut(QtGui.QKeySequence.SelectAll, self)
        self.selAllShort.activated.connect(self.SelectAll)

        self.gridShort = QtWidgets.QShortcut(QtGui.QKeySequence('G'), self)
        self.gridShort.activated.connect(self.ToggleGrid)

    def __init2__(self):
        self.createMenubar()
        self.SetupDocksAndPanels()
        self.HandleOpenFromFile()

    actions = {}

    def createMenubar(self):
        self.CreateAction('openfromfile', self.HandleOpenFromFile, None,
                          'Open Level by File...', 'Open a level based on its filename',
                          QtGui.QKeySequence('Ctrl+Shift+O'))
        self.CreateAction('save', self.HandleSaveAs, None, 'Save Level',
                          'Save the level back to the archive file', QtGui.QKeySequence.Save)
        self.CreateAction('screenshot', self.HandleScreenshot, None, 'Level Screenshot...',
                          'Take a full size screenshot of your level for you to share', QtGui.QKeySequence('Ctrl+Alt+S'))


        menubar = QtWidgets.QMenuBar()
        self.setMenuBar(menubar)

        fmenu = menubar.addMenu('&File')
        fmenu.addAction(self.actions['openfromfile'])
        fmenu.addSeparator()
        fmenu.addAction(self.actions['save'])
        fmenu.addSeparator()
        fmenu.addAction(self.actions['screenshot'])

    def SetupDocksAndPanels(self):
        dock = QtWidgets.QDockWidget('Modify Selected Object Properties', self)
        dock.setVisible(False)
        dock.setFeatures(QtWidgets.QDockWidget.DockWidgetMovable | QtWidgets.QDockWidget.DockWidgetFloatable)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        dock.setObjectName('objecteditor')

        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        dock.setFloating(True)

        # create the palette
        dock = QtWidgets.QDockWidget('Palette', self)
        dock.setFeatures(
            QtWidgets.QDockWidget.DockWidgetMovable | QtWidgets.QDockWidget.DockWidgetFloatable | QtWidgets.QDockWidget.DockWidgetClosable)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        dock.setObjectName('palette')  # needed for the state to save/restore correctly

        self.creationDock = dock
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        dock.setVisible(True)

        self.objPicker = ObjectPickerWidget()
        self.objPicker.ObjChanged.connect(self.ObjectChoiceChanged)
        self.objPicker.ObjReplace.connect(self.ObjectReplace)
        dock.setWidget(self.objPicker)

    def HandleOpenFromFile(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, "Open Level", '', 'Course data file (*.cdt)')[0]
        if filename:
            self.LoadLevel(str(filename))
            return True

        return

    def HandleSaveAs(self):
        if globals.LevelLoaded:
            filename = QtWidgets.QFileDialog.getSaveFileName(self, "Save Level As", '', 'Wii U Course data file (*.cdt)')[0]
            if filename:
                courseBuffer = globals.Area.save()
                with open(filename, "wb+") as out:
                    out.write(courseBuffer)

                return True

        return

    def HandleScreenshot(self):
        if globals.LevelLoaded:
            fn = QtWidgets.QFileDialog.getSaveFileName(self, "Save Screenshot", '/untitled.png',
                                                       'PNG file (*.png)')[0]
            if fn == '': return
            fn = str(fn)

            areaWidth = globals.Area.areaWidth * globals.TileWidth / 16

            ScreenshotImage = QtGui.QImage(areaWidth, 27 * globals.TileWidth, QtGui.QImage.Format_ARGB32)
            ScreenshotImage.fill(Qt.transparent)

            RenderPainter = QtGui.QPainter(ScreenshotImage)
            self.scene.render(RenderPainter, QtCore.QRectF(0, 0, areaWidth, 27 * globals.TileWidth),
                              QtCore.QRectF(0.5 * globals.TileWidth,
                                            -26.5 * globals.TileWidth,
                                            areaWidth,
                                            27 * globals.TileWidth))
            RenderPainter.end()

            ScreenshotImage.save(fn, 'PNG', 50)

    def SelectAll(self):
        paintRect = QtGui.QPainterPath()
        paintRect.addRect(0, -(26.5 * globals.TileWidth), 241 * globals.TileWidth, 27.5 * globals.TileWidth)
        self.scene.setSelectionArea(paintRect)

    def ToggleGrid(self):
        globals.GridShown = not globals.GridShown
        self.scene.update()

    def LoadLevel(self, filename):
        with open(filename, "rb") as inf:
            inb = inf.read()

        checksum = zlib.crc32(inb[16:]) % (1 << 32)
        if inb[8:12] == checksum.to_bytes(4, "big"):
            bom = '>'

        elif inb[8:12] == checksum.to_bytes(4, "little"):
            bom = '<'

        else:
            print("Invalid checksum! Level data seems to be corrupted...")
            return

        cdt = CourseData(bom)
        cdt.data(inb, 0)

        self.scene.clearSelection()
        self.CurrentSelection = []
        self.scene.clear()

        self.graphicsView.centerOn(0, -(26.5 * globals.TileWidth))

        areaWidth = cdt.areaWidth * globals.TileWidth / 16
        border = BorderItem(0.5 * globals.TileWidth, -26.5 * globals.TileWidth, areaWidth, 27 * globals.TileWidth)
        self.scene.addItem(border)

        globals.Area = Area(inb, cdt, bom)

        globals.LevelLoaded = True

        levelname = globals.Area.name.split(b'\x00\x00')[0].decode('utf-16-be')
        self.setWindowTitle(levelname)

    def handleSceneSelectionChanged(self):
        try:
            selitems = self.scene.selectedItems()

        except RuntimeError:
            return

        showObjectPanel = False
        updateModeInfo = False

        if len(selitems) == 1:
            item = selitems[0]
            self.selObj = item

        elif not selitems:
            self.selObj = None

        self.CurrentSelection = selitems

    def keyPressEvent(self, event):
        if event.key() in [Qt.Key_Delete, Qt.Key_Backspace]:
            sel = self.scene.selectedItems()
            for obj in sel:
                index = globals.Area.objects.index(obj)
                del globals.Area.objects[index]

                obj.delete()
                obj.setSelected(False)
                self.scene.removeItem(obj)

            event.accept()

        elif event.key() == Qt.Key_L:
            sel = self.scene.selectedItems()
            for obj in sel:
                if isinstance(obj, PixmapItem) or isinstance(obj, Area):
                    continue

                obj.height += globals.TileWidth

                oldrect = obj.boundRect
                newrect = QtCore.QRectF(obj.x(), obj.y(), obj.width, obj.height)
                updaterect = oldrect.united(newrect)

                obj.update(updaterect)

                obj.UpdateRects()
                self.scene.update(updaterect)

            event.accept()

        elif event.key() == Qt.Key_K:
            sel = self.scene.selectedItems()
            for obj in sel:
                if isinstance(obj, PixmapItem) or isinstance(obj, Area):
                    continue

                obj.height -= globals.TileWidth

                oldrect = obj.boundRect
                newrect = QtCore.QRectF(obj.x(), obj.y(), obj.width, obj.height)
                updaterect = oldrect.united(newrect)

                obj.UpdateRects()
                self.scene.update(updaterect)

            event.accept()

        else:
            super().keyPressEvent(event)

    @QtCore.pyqtSlot(int)
    def ObjectChoiceChanged(self, type_):
        globals.CurrentObject = type_

    @QtCore.pyqtSlot(int)
    def ObjectReplace(self, type_):
        items = self.scene.selectedItems()
        type_obj = PixmapItem

        parentFlags = 0x6000840

        if type_ == 0:
            type_ = EditRengaBlock

        elif type_ == 1:
            type_ = EditHatenaBlock

        elif type_ == 2:
            type_ = EditHardBlock

        elif type_ == 3:
            type_ = EditKumoBlock

        elif type_ == 4:
            type_ = EditIceBlock

        elif 4 < type_ < 76:
            data = type_ - 5
            type_ = EditGround

        elif type_ == 76:
            type_ = EditCoin

        elif type_ == 77:
            parentFlags |= 0x4
            type_ = EditCoin

        elif type_ == 78:
            type_ = EditDokan

        elif type_ == 79:
            parentFlags = 0x6000800
            type_ = EditDokan

        elif type_ == 80:
            parentFlags = 0x6000860
            type_ = EditDokan

        elif type_ == 81:
            parentFlags = 0x6000820
            type_ = EditDokan

        elif type_ == 82:
            type_ = EditGroundBox

        elif type_ == 83:
            parentFlags |= 0x40000
            type_ = EditGroundBox

        elif type_ == 84:
            parentFlags |= 0x80000
            type_ = EditGroundBox

        elif type_ == 85:
            type_ = EditGroundGoal

        elif type_ == 86:
            type_ = EditGroundStart

        else:
            return

        for x in items:
            if isinstance(x, type_obj) and x.type != type_:
                for z in objectsZValues:
                    if type_ in objectsZValues[z]:
                        break

                if type_ == EditRengaBlock:
                    pix = globals.Tiles[1]
                    x.width = globals.TileWidth
                    x.height = globals.TileWidth

                elif type_ == EditHatenaBlock:
                    pix = globals.Tiles[2]
                    x.width = globals.TileWidth
                    x.height = globals.TileWidth

                elif type_ == EditHardBlock:
                    pix = globals.Tiles[6]
                    x.width = globals.TileWidth
                    x.height = globals.TileWidth

                elif type_ == EditKumoBlock:
                    pix = globals.Tiles[102]
                    x.width = globals.TileWidth
                    x.height = globals.TileWidth

                elif type_ == EditIceBlock:
                    pix = globals.Tiles[120]
                    x.width = globals.TileWidth
                    x.height = globals.TileWidth

                elif type_ == EditGround:
                    pix = globals.Tiles[184 + data]
                    x.width = globals.TileWidth
                    x.height = globals.TileWidth
                    x.data = data

                elif type_ == EditCoin and not parentFlags & 0x4:
                    pix = globals.Tiles[7]
                    x.width = globals.TileWidth
                    x.height = globals.TileWidth

                elif type_ == EditCoin and parentFlags & 0x4 == 4:
                    pix = globals.Tiles[256]
                    x.width = globals.TileWidth
                    x.height = globals.TileWidth

                elif type_ == EditDokan:
                    pix, x.width, x.height = globals.mainWindow.paintPipe(2, max(2, x.height // globals.TileWidth), parentFlags & 0x60)

                elif type_ == EditGroundBox:
                    pix, x.width, x.height = globals.mainWindow.paintGroundBox(max(3, x.width // globals.TileWidth), max(3, x.height // globals.TileWidth), ((parentFlags >> 16) & 0xF) // 4)

                elif type_ == EditGroundGoal:
                    pix, x.width, x.height = globals.mainWindow.paintGroundGoal(max(13, x.width // globals.TileWidth + 3), max(2, x.height // globals.TileWidth))

                elif type_ == EditGroundStart:
                    pix, x.width, x.height = globals.mainWindow.paintGroundStart(max(8, x.width // globals.TileWidth + 3), max(2, x.height // globals.TileWidth))

                x.parentFlags = parentFlags
                x.SetType(type_, pix, z)

    def paintPipe(self, w, h, direction):
        pix = QtGui.QPixmap()
        painter = QtGui.QPainter(pix)
        rw, rh = 0, 0
        top = True

        if direction in [0x40, 0x60]:
            rw, rh = (w * globals.TileWidth, h * globals.TileWidth)
            pix = QtGui.QPixmap(rw, rh)
            pix.fill(Qt.transparent)
            painter = QtGui.QPainter(pix)

            ys = {0x60: range(h - 1, -1, -1), 0x40: range(h)}

            for y in ys[direction]:
                for x in range(w):
                    realX = x

                    while realX > 1:
                        realX -= 2

                    if top:
                        if direction == 0x40:  # Up
                            painter.drawPixmap(globals.TileWidth * x, globals.TileWidth * y, globals.Tiles[14 + 1 * realX])

                        else:  # Down
                            painter.drawPixmap(globals.TileWidth * x, globals.TileWidth * y, globals.Tiles[46 + 1 * realX])

                    else:
                        painter.drawPixmap(globals.TileWidth * x, globals.TileWidth * y, globals.Tiles[30 + 1 * realX])

                top = False

        elif direction in [0, 0x20]:
            rw, rh = (h * globals.TileWidth, w * globals.TileWidth)
            pix = QtGui.QPixmap(rw, rh)
            pix.fill(Qt.transparent)
            painter = QtGui.QPainter(pix)

            xs = {0: range(h - 1, -1, -1), 0x20: range(h)}

            for x in xs[direction]:
                for y in range(w):
                    realY = y

                    while realY > 1:
                        realY -= 2

                    if top:
                        if not direction:  # Right
                            painter.drawPixmap(globals.TileWidth * x, globals.TileWidth * y, globals.Tiles[13 + 16 * realY])

                        else:  # Left
                            painter.drawPixmap(globals.TileWidth * x, globals.TileWidth * y, globals.Tiles[11 + 16 * realY])

                    else:
                        painter.drawPixmap(globals.TileWidth * x, globals.TileWidth * y, globals.Tiles[12 + 16 * realY])

                top = False

        painter.end()

        return pix, rw, rh

    def paintGroundBox(self, w, h, type_):
        rw, rh = (w * globals.TileWidth, h * globals.TileWidth)
        pix = QtGui.QPixmap(rw, rh)
        pix.fill(Qt.transparent)
        painter = QtGui.QPainter(pix)

        # Top
        if 0 < w < 3:
            painter.drawPixmap(0, 0, globals.TileWidth, globals.TileWidth, globals.Tiles[55 + 3 * type_])

            if w > 1:
                painter.drawPixmap(globals.TileWidth, 0, globals.TileWidth, globals.TileWidth, globals.Tiles[57 + 3 * type_])

        elif w:
            painter.drawPixmap(0, 0, globals.TileWidth, globals.TileWidth, globals.Tiles[55 + 3 * type_])
            painter.drawTiledPixmap(globals.TileWidth, 0, (w - 2) * globals.TileWidth, globals.TileWidth, globals.Tiles[56 + 3 * type_])
            painter.drawPixmap(globals.TileWidth + (w - 2) * globals.TileWidth, 0, globals.TileWidth, globals.TileWidth, globals.Tiles[57 + 3 * type_])

        # Middle
        l1 = [71, 87]
        l2 = [72, 88]
        l3 = [73, 89]

        if 0 < w < 3:
            for y in range(1, h - 1):
                realY = y - 1

                while realY > 1:
                    realY -= 2

                painter.drawPixmap(0, globals.TileWidth * y, globals.TileWidth, globals.TileWidth, globals.Tiles[l1[realY] + 3 * type_])

                if w > 1:
                    painter.drawPixmap(globals.TileWidth, globals.TileWidth * y, globals.TileWidth,
                                       globals.TileWidth, globals.Tiles[l3[realY] + 3 * type_])

        elif w:
            for y in range(1, h - 1):
                realY = y - 1

                while realY > 1:
                    realY -= 2

                painter.drawPixmap(0, globals.TileWidth * y, globals.TileWidth, globals.TileWidth, globals.Tiles[l1[realY] + 3 * type_])

                for x in range(1, w - 1):
                    realX = x - 1

                    while realX > 1:
                        realX -= 2

                    if realX == realY:
                        painter.drawTiledPixmap(globals.TileWidth * x, globals.TileWidth * y, globals.TileWidth,
                                                globals.TileWidth, globals.Tiles[l2[0] + 3 * type_])

                    else:
                        painter.drawTiledPixmap(globals.TileWidth * x, globals.TileWidth * y, globals.TileWidth,
                                                globals.TileWidth, globals.Tiles[l2[1] + 3 * type_])

                painter.drawPixmap(globals.TileWidth + ((w - 2) * globals.TileWidth), globals.TileWidth * y, globals.TileWidth,
                                   globals.TileWidth, globals.Tiles[l3[realY] + 3 * type_])

        # Bottom
        if 0 < w < 3:
            painter.drawPixmap(0, (h - 1) * globals.TileWidth, globals.TileWidth, globals.TileWidth, globals.Tiles[103 + 3 * type_])

            if w > 1:
                painter.drawPixmap(globals.TileWidth, (h - 1) * globals.TileWidth, globals.TileWidth, globals.TileWidth, globals.Tiles[105 + 3 * type_])

        elif w:
            painter.drawPixmap(0, (h - 1) * globals.TileWidth, globals.TileWidth, globals.TileWidth, globals.Tiles[103 + 3 * type_])
            painter.drawTiledPixmap(globals.TileWidth, (h - 1) * globals.TileWidth, (w - 2) * globals.TileWidth,
                                    globals.TileWidth, globals.Tiles[104 + 3 * type_])
            painter.drawPixmap(globals.TileWidth + (w - 2) * globals.TileWidth, (h - 1) * globals.TileWidth, globals.TileWidth,
                               globals.TileWidth, globals.Tiles[105 + 3 * type_])

        painter.end()

        return pix, rw, rh

    def paintGroundStart(self, w, h):
        w -= 3
        rw, rh = (w * globals.TileWidth, h * globals.TileWidth)
        pix = QtGui.QPixmap(rw, rh)
        pix.fill(Qt.transparent)
        painter = QtGui.QPainter(pix)

        edge = True

        for x in range(w - 1, -1, -1):
            for y in range(h):
                if x == w - 1:
                    if not y:
                        painter.drawPixmap(globals.TileWidth * x, globals.TileWidth * y, globals.Tiles[122])

                    else:
                        painter.drawPixmap(globals.TileWidth * x, globals.TileWidth * y, globals.Tiles[138])

                else:
                    if not y:
                        painter.drawPixmap(globals.TileWidth * x, globals.TileWidth * y, globals.Tiles[121])

                    else:
                        painter.drawPixmap(globals.TileWidth * x, globals.TileWidth * y, globals.Tiles[137])

            edge = False

        painter.end()

        return pix, rw, rh

    def paintGroundGoal(self, w, h):
        w -= 3
        rw, rh = (w * globals.TileWidth, h * globals.TileWidth)
        pix = QtGui.QPixmap(rw, rh)
        pix.fill(Qt.transparent)
        painter = QtGui.QPainter(pix)

        for x in range(w):
            for y in range(h):
                if not x:
                    if not y:
                        painter.drawPixmap(globals.TileWidth * x, globals.TileWidth * y, globals.Tiles[123])

                    else:
                        painter.drawPixmap(globals.TileWidth * x, globals.TileWidth * y, globals.Tiles[139])

                else:
                    if not y:
                        painter.drawPixmap(globals.TileWidth * x, globals.TileWidth * y, globals.Tiles[124])

                    else:
                        painter.drawPixmap(globals.TileWidth * x, globals.TileWidth * y, globals.Tiles[140])

        painter.end()

        return pix, rw, rh


def main():
    globals.app = QtWidgets.QApplication(sys.argv)
    globals.app.setApplicationDisplayName('PointlessMaker v%s' % EditorVersion)

    globals.mainWindow = MainWindow()
    globals.mainWindow.__init2__()
    globals.mainWindow.show()
    exitcodesys = globals.app.exec_()
    globals.app.deleteLater()
    sys.exit(exitcodesys)


if __name__ == '__main__': main()
