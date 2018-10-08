import QtQuick 2.7
import QtQuick.Controls 1.5
import QtQuick.Layouts 1.3
import QtQuick.Extras 1.4
import QtGraphicalEffects 1.0
import QtQuick.Controls.Styles 1.4

Item {
    width: 640
    height: 480

    SplitView {
        anchors.fill: parent

        TreeView {
            TableViewColumn {
              role: "key"
              title: "Config"
              width: 150
            }
            TableViewColumn {
              role: "type"
              title: "Type"
              width: 50
            }
            TableViewColumn {
              role: "value"
              title: "Value"
              width: 100
            }
            id: configTree
            width: 300
            model: configTreeModel
        }

        SplitView {
            orientation: Qt.Vertical

            TextEdit {
                height: 100
                text: qsTr("Editables!")
            }

            ListView {
                id: listView
                objectName: "myList"
                delegate: Text{text: display}
            }
        }
    }
}
