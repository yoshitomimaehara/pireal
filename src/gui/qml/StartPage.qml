/*
 * Copyright 2015-2016 - Gabriel Acosta <acostadariogabriel@gmail.com>
 *
 * This file is part of Pireal.
 *
 * Pireal is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * any later version.
 *
 * Pireal is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Pireal; If not, see <http://www.gnu.org/licenses/>.
 */

import QtQuick 2.6
import QtQuick.Layouts 1.1
//import QtMultimedia 5.0
import QtQuick.Controls 2.0
import "widgets"

Item {
    id: root

    property bool compressed: false
    signal openRecentDatabase(string path)
    signal newDatabase
    signal openDatabase
    signal removeCurrent(string path)

    function loadItem(name, path) {
        listModel.append({"name": name, "path": path})
    }

    function clear() {
        listModel.clear();
    }

    ListModel {
        id: listModel

        ListElement {
            name: ""
            path: ""
        }
    }

    Component.onCompleted: {
        listModel.clear();
    }

    onWidthChanged: {
        if(root.width < 1022) {
            root.compressed = true;
        } else {
            root.compressed = false;
        }
    }

    SwipeView {
        id: view

        currentIndex: 0
        anchors.fill: parent

        RowLayout {
            id: rowLayout

            Item {
                id: leftArea

                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.maximumWidth: 400
                visible: !root.compressed

                onVisibleChanged: {
                    leftArea.width = Layout.maximumWidth
                }

                Image {
                    id: logo
                    source: "pireal_logo-black.png"
                    anchors.horizontalCenter: parent.horizontalCenter
                }

                Text {
                    id: whatIsPireal
                    text: qsTr("<b>π</b>real is a teaching tool for use in learning introduction to database. It allows the user to interactively experiment with Relational Algebra.")
                    anchors.top: logo.bottom
                    anchors.left: parent.left
                    anchors.right: separator.left
                    anchors.margins: 20
                    wrapMode: Text.WordWrap
                    renderType: Text.NativeRendering
                    font.pointSize: 12
                    color: "#5f6566"
                }

                Text {
                    id: getStarted
                    text: qsTr("Getting Started")
                    anchors.top: whatIsPireal.bottom
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.topMargin: 50
                    renderType: Text.NativeRendering
                    font.pointSize: 18
                    color: "#5f6566"
                }
                ColumnLayout {
                    id: buttons
                    spacing: 10
                    anchors.top: getStarted.bottom
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.topMargin: 30

                    Button {
                        text: qsTr("Create a new Database")
                        onClicked: {
                            newDatabase();
                        }

                    }

                    Button {
                        text: qsTr("Open a Database")
                        implicitWidth: parent.width;
                        onClicked: {
                            openDatabase();
                        }
                    }


                }

                Column {
                    spacing: 10
                    anchors.top: buttons.bottom
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.margins: 30

                    Text {
                        text: qsTr("• Open a recent database from the list.")
                        font.pointSize: 12
                        renderType: Text.NativeRendering
                        anchors.left: parent.left
                        anchors.right: parent.right
                        wrapMode: Text.WordWrap
                        color: "#5f6566"
                    }

                    Text {
                        text: qsTr("• <a href=\"#\">Press here</a> or slide the screen to the left to see an example.")
                        anchors.left: parent.left
                        anchors.right: parent.right
                        font.pointSize: 12
                        renderType: Text.NativeRendering
                        linkColor: "#4896b8"
                        color: "#5f6566"
                        wrapMode: Text.WordWrap
                        onLinkActivated: {
                            view.currentIndex = 1;
                            //player.play();
                        }
                    }

                }



                Rectangle {
                    id: separator
                    color: "#ccc"
                    width: 1
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    anchors.topMargin: 20
                    anchors.bottomMargin: 20
                    anchors.left: parent.right

                }


            }

            Item {
                id: rightArea

                Layout.fillWidth: true
                Layout.fillHeight: true

                Rectangle {
                    id: container

                    width: root.width / 2; height: root.height / 1.5
                    anchors.centerIn: parent
                    color: "#f5f5f5"
                    border.color: "#dddddd"
                    border.width: 1
                    enabled: !parent.flipped
                    radius: 3
                    Text {
                        text: qsTr("No recent database")
                        color: "#838b8c"
                        anchors.centerIn: parent
                        visible: listModel.count ? false : true
                        font.pointSize: 20
                        renderType: Text.NativeRendering
                    }
                    ListView {
                        id: listView

                        anchors {
                            topMargin: 5
                            fill: parent
                        }
                        width: parent.width / 2.5; height: parent.height / 1.5
                        model: listModel
                        spacing: 3
                        focus: true
                        clip: true
                        currentIndex: -1
                        property bool empty: listView.count == 0
                        delegate: Rectangle {
                            id: listItem
                            anchors {
                                left: parent.left
                                right: parent.right
                                leftMargin: 5
                                rightMargin: 5
                            }
                            height: 75
                            property bool current: ListView.isCurrentItem
                            color: listItem.current ? "#5294e2" : "#ebebeb"
                            MouseArea {
                                anchors.fill: parent
                                hoverEnabled: true

                                onHoveredChanged: {
                                    listView.currentIndex = index;
                                }

                                onExited: {
                                    listView.currentIndex = -1;
                                }

                                onClicked: {
                                    root.openRecentDatabase(path);
                                }
                            }

                            Column {
                                spacing: 8
                                anchors {
                                    verticalCenter: parent.verticalCenter
                                    left: parent.left
                                    right: parent.right
                                    leftMargin: 20
                                    rightMargin: 20
                                }

                                Text {
                                    text: name
                                    font.bold: true
                                    font.pixelSize: 30
                                    color: listItem.current ? "#fafbfb" : "#979dac"
                                    renderType: Text.NativeRendering
                                }

                                Text {
                                    text: path
                                    color:listItem.current ? "#fafbfb" : "#979dac"
                                    width: parent.width
                                    elide: Text.ElideLeft
                                    renderType: Text.NativeRendering
                                    font.pixelSize: 16
                                }
                            }

                            Image {
                                id: imgDelete
                                source: "close.png"
                                anchors {
                                    right: parent.right
                                    top: parent.top
                                    topMargin: 15
                                    rightMargin: 15
                                }
                                scale: ma.pressed ? 0.7 : 1
                                visible: listItem.current ? true: false
                                onVisibleChanged: NumberAnimation {
                                    target: imgDelete; property: "scale"; from: 0; to: 1; duration: 200
                                }

                                MouseArea {
                                    id: ma
                                    anchors.fill: parent
                                    onClicked: {
                                        root.removeCurrent(path);
                                        listView.model.remove(index);
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        Item {
            id: itemPlayer

            Rectangle {
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                anchors.margins: 50
                border.width: 1

                /*MediaPlayer {
                    id: player
                    source: "/home/gabo/pireal.webm"
                    property bool paused: false

                    onStopped: {
                        view.currentIndex = 0;
                    }

                }*/

                /*VideoOutput {
                    id: output
                    source: player
                    anchors.fill: parent

                    MouseArea {
                        anchors.fill: parent

                        onClicked: {
                            if (!player.paused) {
                                player.pause();
                                player.paused = true;
                            } else {
                                player.play();
                                player.paused = false;
                            }
                        }

                        onDoubleClicked:  {
                            player.stop();
                        }
                    }
                }*/
            }
        }
    }

    PageIndicator {
          currentIndex: view.currentIndex
          count: view.count
    }
    Row {
        spacing: 10
        anchors {
            bottom: parent.bottom
            right: parent.right
            bottomMargin: 5
            rightMargin: 10
        }

        Text {
         text: "Powered by: "
         color: "#838b8c"
         height: logoPython.height
         verticalAlignment: Text.AlignVCenter
         font.pixelSize: 12
        }

        Image { id: logoPython; source: "python-logo.png"; opacity: 0.7 }
        Image { source: "bwqt.png"; opacity: 0.7 }
    }

    Text {
        text: "Copyright © 2015-" + new Date().getFullYear() + " Gabriel Acosta. Pireal is distributed under the terms of the GNU GPLv3+ copyleft license"
        color: "#838b8c"
        anchors {
            bottom: parent.bottom
            left: parent.left
            bottomMargin: 5
            leftMargin: 10
        }
        font.pixelSize: 12
        visible: root.compressed ? false : true
        renderType: Text.NativeRendering
    }

}
