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

import struct, sys

from PyQt5 import QtCore, QtGui, QtWidgets
Qt = QtCore.Qt

from mainwindowui import Ui_MainWindow

EditKuribo = 0
EditNokonoko = 1
EditPakkun = 2
EditHammerBros = 3
EditRengaBlock = 4
EditHatenaBlock = 5
EditHardBlock = 6
EditGround = 7
EditCoin = 8
EditDokan = 9
EditJumpStep = 10
EditLift = 11
EditDossun = 12
EditKillerHoudai = 13
EditGroundMushroom = 14
EditBombhei = 15
EditGroundBox = 16
EditBridge = 17
EditPSwitch = 18
EditPowBlock = 19
EditSuperKinoko = 20
EditChikuwaBlock = 21
EditKumoBlock = 22
EditOnpuBlock = 23
EditFireBar = 24
EditTogezo = 25
EditGroundGoal = 26
EditGoalPole = 27
EditMet = 28
EditClearBlock = 29
EditJugem = 30
EditJugemCloud = 31
EditTsutaBlock = 32
Edit1upKinoko = 33
EditFireFlower = 34
EditSuperStar = 35
EditYouganLift = 36
EditGroundStart = 37
EditStartSignBoard = 38
EditKameck = 39
EditTogemet = 40
EditTeresa = 41
EditKoopaClown = 42
EditToge = 43
EditKinokoFunny = 44
EditKutsuKuribo = 45
EditKaron = 46
EditSenkanHoudai = 47
EditGesso = 48
EditCastleBridge = 49
EditCharaKinoko = 50
EditDekaKinoko = 51
EditHanachan = 52
EditBeltConveyor = 53
EditBurner = 54
EditDoor = 55
EditPukupuku = 56
EditBlackPakkun = 57
EditPoo = 58
EditRail = 59
EditBubble = 60
EditWanwan = 61
EditKoopa = 62
EditIceBlock = 63
EditTsuta = 64
EditCharaMario = 65
EditAirSignBoard = 66
EditHalfHitWall = 67
EditSaw = 68
EditPlayer = 69

objectNames = {0: "EditKuribo",
               1: "EditNokonoko",
               2: "EditPakkun",
               3: "EditHammerBros",
               4: "EditRengaBlock",
               5: "EditHatenaBlock",
               6: "EditHardBlock",
               7: "EditGround",
               8: "EditCoin",
               9: "EditDokan",
               10: "EditJumpStep",
               11: "EditLift",
               12: "EditDossun",
               13: "EditKillerHoudai",
               14: "EditGroundMushroom",
               15: "EditBombhei",
               16: "EditGroundBox",
               17: "EditBridge",
               18: "EditPSwitch",
               19: "EditPowBlock",
               20: "EditSuperKinoko",
               21: "EditChikuwaBlock",
               22: "EditKumoBlock",
               23: "EditOnpuBlock",
               24: "EditFireBar",
               25: "EditTogezo",
               26: "EditGroundGoal",
               27: "EditGoalPole",
               28: "EditMet",
               29: "EditClearBlock",
               30: "EditJugem",
               31: "EditJugemCloud",
               32: "EditTsutaBlock",
               33: "Edit1upKinoko",
               34: "EditFireFlower",
               35: "EditSuperStar",
               36: "EditYouganLift",
               37: "EditGroundStart",
               38: "EditStartSignBoard",
               39: "EditKameck",
               40: "EditTogemet",
               41: "EditTeresa",
               42: "EditKoopaClown",
               43: "EditToge",
               44: "EditKinokoFunny",
               45: "EditKutsuKuribo",
               46: "EditKaron",
               47: "EditSenkanHoudai",
               48: "EditGesso",
               49: "EditCastleBridge",
               50: "EditCharaKinoko",
               51: "EditDekaKinoko",
               52: "EditHanachan",
               53: "EditBeltConveyor",
               54: "EditBurner",
               55: "EditDoor",
               56: "EditPukupuku",
               57: "EditBlackPakkun",
               58: "EditPoo",
               59: "EditRail",
               60: "EditBubble",
               61: "EditWanwan",
               62: "EditKoopa",
               63: "EditIceBlock",
               64: "EditTsuta",
               65: "EditCharaMario",
               66: "EditAirSignBoard",
               67: "EditHalfHitWall",
               68: "EditSaw",
               69: "EditPlayer"}


class CourseData(struct.Struct):
    def __init__(self):
        super().__init__('>QI4xH6BQB7x64s2x2s4BH2BI96B2I12xI')

    def data(self, data, pos):
        (self.version,
         self.checksum,
         self.year,
         self.month,
         self.day,
         self.hour,
         self.minute,
         self.unk1,
         self.unk2,
         self.unk3,
         self.unk4,
         self.name,
         self.mode,
         self.unk5,
         self.theme,
         self.unk6,
         self.unk7,
         self.timer,
         self.scroll,
         self.unk8,
         self.unk9,
         self.unk10,
         self.unk11,
         self.unk12,
         self.unk13,
         self.unk14,
         self.unk15,
         self.unk16,
         self.unk17,
         self.unk18,
         self.unk19,
         self.unk20,
         self.unk21,
         self.unk22,
         self.unk23,
         self.unk24,
         self.unk25,
         self.unk26,
         self.unk27,
         self.unk28,
         self.unk29,
         self.unk30,
         self.unk31,
         self.unk32,
         self.unk33,
         self.unk34,
         self.unk35,
         self.unk36,
         self.unk37,
         self.unk38,
         self.unk39,
         self.unk40,
         self.unk41,
         self.unk42,
         self.unk43,
         self.unk44,
         self.unk45,
         self.unk46,
         self.unk47,
         self.unk48,
         self.unk49,
         self.unk50,
         self.unk51,
         self.unk52,
         self.unk53,
         self.unk54,
         self.unk55,
         self.unk56,
         self.unk57,
         self.unk58,
         self.unk59,
         self.unk60,
         self.unk61,
         self.unk62,
         self.unk63,
         self.unk64,
         self.unk65,
         self.unk66,
         self.unk67,
         self.unk68,
         self.unk69,
         self.unk70,
         self.unk71,
         self.unk72,
         self.unk73,
         self.unk74,
         self.unk75,
         self.unk76,
         self.unk77,
         self.unk78,
         self.unk79,
         self.unk80,
         self.unk81,
         self.unk82,
         self.unk83,
         self.unk84,
         self.unk85,
         self.unk86,
         self.unk87,
         self.unk88,
         self.unk89,
         self.unk90,
         self.unk91,
         self.unk92,
         self.unk93,
         self.unk94,
         self.unk95,
         self.unk96,
         self.unk97,
         self.unk98,
         self.unk99,
         self.unk100,
         self.unk101,
         self.unk102,
         self.unk103,
         self.unk104,
         self.unk105,
         self.unk106,
         self.unk107,
         self.numObjects) = self.unpack_from(data, pos)


class Object(struct.Struct):
    def __init__(self):
        super().__init__('>2Ih2b3I2b2h2b')

    def data(self, data, pos):
        (self.x,
         self.z,
         self.y,
         self.w,
         self.h,
         self.parentFlags,
         self.childFlags,
         self.data,
         self.objType,
         self.childType,
         self.linkID,
         self.eIndex,
         self._1E,
         self.cTID) = self.unpack_from(data, pos)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.setupUi(self)

        self.items = []

        self.scene = QtWidgets.QGraphicsScene(self)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)

        self.scene.selectionChanged.connect(self.handleSceneSelectionChanged)

        colours = {}
        colours[EditRengaBlock] = QtGui.QColor(158, 95, 25)
        colours[EditHatenaBlock] = Qt.yellow
        colours[EditHardBlock] = QtGui.QColor(212, 162, 103)
        colours[EditKumoBlock] = QtGui.QColor(255, 252, 255) # cloud
        colours[EditKuribo] = QtGui.QColor(158, 95, 25)
        colours[EditDokan] = QtGui.QColor(182, 237, 57)
        colours[EditGround] = QtGui.QColor(75, 202, 13)
        colours[EditIceBlock] = Qt.cyan
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
                rz = obj.z // 10
                ry -= (obj.h - 1) * 16
                rw = obj.w * 16
                rh = obj.h * 16
                item = QtWidgets.QGraphicsItem

                if obj.objType == EditGround:
                    ri = QtWidgets.QGraphicsRectItem(rx, ry, rw, rh)
                    ri.setBrush(colours[EditGround])
                    item = ri
                    text = QtWidgets.QGraphicsSimpleTextItem(str(obj.data), ri)
                    text.setPos(rx + 2, ry + 2)

                elif obj.objType == EditCoin:
                    ei = QtWidgets.QGraphicsEllipseItem(rx + 1, ry, rw - 2, rh)
                    ei.setBrush(Qt.yellow)
                    item = ei

                elif obj.objType == EditKuribo:
                    ei = QtWidgets.QGraphicsEllipseItem(rx, ry, rw, rh)
                    ei.setBrush(colours[EditKuribo])
                    item = ei

                elif obj.objType == EditSaw:
                    ei = QtWidgets.QGraphicsEllipseItem(rx, ry, rw, rh)
                    ei.setBrush(colours[EditSaw])
                    item = ei

                elif obj.objType == EditTsuta:
                    ri = QtWidgets.QGraphicsRectItem(rx + 6, ry, rw - 12, rh)
                    ri.setBrush(colours[EditTsuta])
                    item = ri

                elif obj.objType == EditPoo: # wrench
                    ri = QtWidgets.QGraphicsRectItem(rx, ry + 12, rw, rh - 12)
                    ri.setBrush(QtGui.QColor(64, 64, 64))
                    item = ri

                elif obj.objType == EditDoor:
                    ri = QtWidgets.QGraphicsRectItem(rx, ry - 16, rw, rh)
                    ri.setBrush(QtGui.QColor(192, 187, 65))
                    item = ri

                elif obj.objType == EditLift:
                    ri = QtWidgets.QGraphicsRectItem(rx, ry, rw, rh - 12)
                    ri.setBrush(QtGui.QColor(192, 187, 65))
                    item = ri

                else:
                    ri = QtWidgets.QGraphicsRectItem(rx, ry, rw, rh);
                    if obj.objType in colours:
                        ri.setBrush(colours[obj.objType])
                    else:
                        ri.setBrush(Qt.magenta)
                    item = ri

                item.setToolTip(str(obj.objType))

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
        if items.size() == 1:
            index = self.items.index(items[0])
            #self.objectList.setCurrentRow(index)
            self.objectList.setCurrentCell(index, 0)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
