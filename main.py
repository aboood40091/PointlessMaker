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
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
Qt = QtCore.Qt

from area import *
from classes import *
from items import *
from obj_names import *
from widgets import *

import globals

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

        if shortcut is not None: act.setShortcut(shortcut)
        if statustext is not None: act.setStatusTip(statustext)
        if toggle:
            act.setCheckable(True)
        if function is not None: act.triggered.connect(function)

        self.actions[shortname] = act

    def __init__(self):
        super().__init__(None)
        self.setWindowTitle('PointlessMaker v0.2')
        self.setUnifiedTitleAndToolBarOnMac(True)

        self.UpdateFlag = False
        self.selObj = None
        self.CurrentSelection = []
        self.keylist = []

        self.scene = Scene(0, -(27 * globals.TileWidth), 241 * globals.TileWidth, 28 * globals.TileWidth, self)
        self.scene.setItemIndexMethod(QtWidgets.QGraphicsScene.NoIndex)
        self.scene.selectionChanged.connect(self.handleSceneSelectionChanged)

        self.graphicsView = LevelViewWidget(self.scene, self)
        self.graphicsView.centerOn(0, -(26.5 * globals.TileWidth))

        self.setCentralWidget(self.graphicsView)

    def __init2__(self):
        self.createMenubar()

        filename = QtWidgets.QFileDialog.getOpenFileName(self, "Open Level", '', 'Level file (*.cdt)')[0]
        if filename:
            self.LoadLevel(str(filename))

    actions = {}

    def createMenubar(self):
        self.CreateAction('openfromfile', self.HandleOpenFromFile, None,
                          'Open Level by File...', 'Open a level based on its filename',
                          QtGui.QKeySequence('Ctrl+Shift+O'))
        self.CreateAction('save', self.HandleSaveAs, None, 'Save Level As',
                          'Save the level with a new filename', QtGui.QKeySequence.Save)


        menubar = QtWidgets.QMenuBar()
        self.setMenuBar(menubar)

        fmenu = menubar.addMenu('&File')
        fmenu.addAction(self.actions['openfromfile'])
        fmenu.addSeparator()
        fmenu.addAction(self.actions['save'])

    @QtCore.pyqtSlot()
    def HandleOpenFromFile(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, "Open Level", '', 'Level file (*.cdt)')[0]
        if filename:
            self.LoadLevel(str(filename))
            return True

        return

    @QtCore.pyqtSlot()
    def HandleSaveAs(self):
        if globals.LevelLoaded:
            filename = QtWidgets.QFileDialog.getSaveFileName(self, "Save Level As", '', 'Level file (*.cdt)')[0]
            if filename:
                courseBuffer = globals.Area.save()
                with open(filename, "wb+") as out:
                    out.write(courseBuffer)

                return True

        return

    def LoadLevel(self, filename):
        with open(filename, "rb") as inf:
            inb = inf.read()

        cdt = CourseData()
        cdt.data(inb, 0)

        checksum = zlib.crc32(inb[16:]) % (1 << 32)
        if checksum != cdt.checksum:
            print("Invalid checksum! Level data seems to be corrupted...")
            return

        self.scene.clearSelection()
        self.CurrentSelection = []
        self.scene.clear()

        self.graphicsView.centerOn(0, -(26.5 * globals.TileWidth))

        areaWidth = cdt.areaWidth * globals.TileWidth / 16
        border = BorderItem(0.5 * globals.TileWidth, -26.5 * globals.TileWidth, areaWidth, 27 * globals.TileWidth)
        self.scene.addItem(border)

        globals.Area = Area(inb, cdt)

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
        self.keylist.append(event.key())

        if Qt.Key_Control in self.keylist and Qt.Key_A in self.keylist:
            paintRect = QtGui.QPainterPath()
            paintRect.addRect(0, -(26.5 * globals.TileWidth), 241 * globals.TileWidth, 27.5 * globals.TileWidth)
            self.scene.setSelectionArea(paintRect)

            event.accept()

            return
        
        elif event.key() in [Qt.Key_Delete, Qt.Key_Backspace]:
            try:
                sel = self.scene.selectedItems()

            except RuntimeError:
                return

            if len(sel) > 0:
                for obj in sel:
                    index = globals.Area.objects.index(obj)
                    del globals.Area.objects[index]

                    self.scene.update(obj.boundRect)
                    obj.setSelected(False)
                    obj.delete()
                    
                    self.scene.removeItem(obj)
                    self.scene.update()

                    del obj

                event.accept()
                return

        elif event.key() == Qt.Key_G:
            globals.GridShown = not globals.GridShown
            self.scene.update()

            event.accept()
            return

        super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        try:
            del self.keylist[-1]

        except IndexError:
            pass

        super().keyReleaseEvent(event)

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

            ys = {0x60: list(reversed(range(h))), 0x40: range(h)}

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

            xs = {0: list(reversed(range(h))), 0x20: range(h)}

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

        for x in list(reversed(range(w))):
            for y in range(h):
                if edge:
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

        edge = True

        for x in range(w):
            for y in range(h):
                if edge:
                    if not y:
                        painter.drawPixmap(globals.TileWidth * x, globals.TileWidth * y, globals.Tiles[123])

                    else:
                        painter.drawPixmap(globals.TileWidth * x, globals.TileWidth * y, globals.Tiles[139])

                else:
                    if not y:
                        painter.drawPixmap(globals.TileWidth * x, globals.TileWidth * y, globals.Tiles[124])

                    else:
                        painter.drawPixmap(globals.TileWidth * x, globals.TileWidth * y, globals.Tiles[140])

            edge = False

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
