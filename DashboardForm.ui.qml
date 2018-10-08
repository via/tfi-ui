import QtQuick 2.4
import QtQuick.Layouts 1.3
import QtQuick.Extras 1.4
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4


Item {
    width: 400
    height: 400

    Rectangle {
        id: rectangle
        color: "#141414"
        anchors.rightMargin: 0
        anchors.bottomMargin: 0
        anchors.leftMargin: 0
        anchors.topMargin: 0
        border.color: "#262626"
        anchors.fill: parent

        ColumnLayout {
            spacing: 30
            anchors.fill: parent

            CircularGauge {
                id: gaugeRPM
                objectName: "gaugeRPM"
                Layout.preferredHeight: 200
                Layout.preferredWidth: 200
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                maximumValue: 8000
                style: CircularGaugeStyle {
                  labelStepSize: 1000
                  tickmarkStepSize: 500
                }
            }

            GridLayout {
                width: 100
                height: 100
                Layout.preferredWidth: 200
                columnSpacing: 4
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                rows: 2
                columns: 2

                CircularGauge {
                    id: gaugeMAP
                    objectName: "gaugeMAP"
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    maximumValue: 240
                    style: CircularGaugeStyle {
                      labelStepSize: 20
                      tickmarkStepSize: 20
                    }
                }

                CircularGauge {
                    id: gaugeEGO
                    objectName: "gaugeEGO"
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    minimumValue: 9.0
                    maximumValue: 18.0
                    style: CircularGaugeStyle {
                      labelStepSize: 1
                      tickmarkStepSize: 1
                    }
                }

                Label {
                    color: "#e9e9e9"
                    text: qsTr("MAP")
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                }

                Label {
                    color: "#e9e9e9"
                    text: qsTr("EGO")
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                }
            }


            GridLayout {
                width: 100
                height: 100
                Layout.preferredWidth: 200
                columnSpacing: 4
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                rows: 2
                columns: 4

                Gauge {
                    id: gaugeIAT
                    objectName: "gaugeIAT"
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    Layout.preferredWidth: 60
                }

                Gauge {
                    id: gaugeCLT
                    objectName: "gaugeCLT"
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    Layout.preferredWidth: 60
                }

                Gauge {
                    id: gaugeBRV
                    objectName: "gaugeBRV"
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    Layout.preferredWidth: 60
                    maximumValue: 25
                }

                Gauge {
                    id: gaugeTPS
                    objectName: "gaugeTPS"
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    Layout.preferredWidth: 60
                }

                Label {
                    color: "#e9e9e9"
                    text: qsTr("IAT")
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                }

                Label {
                    color: "#e9e9e9"
                    text: qsTr("CLT")
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                }

                Label {
                    color: "#e9e9e9"
                    text: qsTr("BRV")
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                }

                Label {
                    color: "#e9e9e9"
                    text: qsTr("TPS")
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                }
            }

            GridLayout {
                width: 100
                height: 100
                Layout.preferredWidth: 200
                columnSpacing: 4
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                rows: 2
                columns: 4

                StatusIndicator {
                    id: statusConn
                    objectName: "gaugeCONN"
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                }

                StatusIndicator {
                    id: statusSync
                    objectName: "gaugeSYNC"
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                }

                StatusIndicator {
                    id: statusCut
                    objectName: "gaugeCUT"
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                }

                StatusIndicator {
                    objectName: "gaugeFAULT"
                    id: sensorFault
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                }

                Label {
                    color: "#e9e9e9"
                    text: qsTr("CONN")
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                }

                Label {
                    color: "#e9e9e9"
                    text: qsTr("SYNC")
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                }

                Label {
                    color: "#e9e9e9"
                    text: qsTr("CUT")
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                }

                Label {
                    color: "#e9e9e9"
                    text: qsTr("FAULT")
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                }
            }
        }
    }
}
