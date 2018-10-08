import QtQuick 2.5
import QtQuick.Controls 1.4
import QtQuick.Dialogs 1.2
import QtQuick.Window 2.0

ApplicationWindow {
    visible: true
    width: 400
    height: 1200
    title: qsTr("TFI Interface")

    menuBar: MenuBar {
        Menu {
            title: "File"
            MenuItem { text: "Open Config" }
        }

        Menu {
            title: "Target"
            MenuItem { text: "Read Config" }
            MenuItem { text: "Write Config RAM" }
            MenuItem { text: "Save flash" }
        }

        Menu {
            title: "Windows"
            MenuItem {
                text: "Dashboard"
                onTriggered: dashwindow.show()
            }
            MenuItem { text: "Log Viewer" }
            MenuItem { text: "Output Viewer" }
        }
    }

    MainForm {
        anchors.fill: parent
    }

    Window {
        id: dashwindow

        Dashboard {
            id: dash
            anchors.fill: parent
        }
    }
}
