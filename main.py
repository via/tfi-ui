from PyQt5.QtCore import QUrl, Qt, QAbstractItemModel, QAbstractTableModel, QModelIndex, QByteArray, QVariant, QObject, QTimer
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQuick import QQuickView, QQuickItem
from PyQt5.QtQml import QQmlApplicationEngine
import qml_qrc
import sys

from tfi import sources, interface

app = QApplication(sys.argv)
engine = QQmlApplicationEngine()

class ConfigTreeNode(QObject):
    def __init__(self, node=None, parent=None, model=None):
        super(ConfigTreeNode, self).__init__(parent)
        self.model = model
        self.key = node.name.split('.')[-1] if node else None
        self.node = node
        self.parent = parent
        self.children = []
        self.row = 0
        if self.parent:
            self.parent.children.append(self)
            self.row = len(self.parent.children) - 1


class ConfigTreeModel(QAbstractItemModel):
    ROLE_KEY=Qt.UserRole
    ROLE_TYPE=Qt.UserRole + 1
    ROLE_VALUE=Qt.UserRole + 2

    def __init__(self, parent, nodes):
        super(ConfigTreeModel, self).__init__(parent)
        self.nodes = [nodes[n] for n in sorted(nodes.keys())]
        self.root = ConfigTreeNode("", model=self)
        self.root_obj = QModelIndex()

        def _recurse(parent, prefix, remaining):
            while len(remaining):
                current = remaining[0]
                if current.name.startswith(prefix): # descend
                    remaining = remaining[1:]
                    newnode = ConfigTreeNode(current, parent, model=self)
                    remaining = _recurse(newnode, current.name, remaining)
                else:
                    return remaining
            return []

        _recurse(self.root, "", self.nodes)

    def refresh(self):
        self.layoutChanged.emit()

    def index(self, row, col, parent):
        if not self.hasIndex(row, col, parent):
            return QModelIndex()

        if not parent.isValid():
            parentNode = self.root
        else:
            parentNode = parent.internalPointer()

        try:
            childNode = parentNode.children[row]
            return self.createIndex(row, col, childNode)
        except:
            pass
        return QModelIndex()
    
    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        node = index.internalPointer()
        parent = node.parent
        if parent == self.root:
            return self.root_obj

        return self.createIndex(parent.row, 0, parent)


    def rowCount(self, parent=QModelIndex()):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            node = self.root
        else:
            node = parent.internalPointer()

        return len(node.children)

    def columnCount(self, parent=QModelIndex()):
        return 3

    def roleNames(self):
        roles = super(ConfigTreeModel, self).roleNames()
        roles.update({
            ConfigTreeModel.ROLE_KEY: b"key",
            ConfigTreeModel.ROLE_TYPE: b"type",
            ConfigTreeModel.ROLE_VALUE: b"value"
        })
        return roles

    def data(self, index, role):
        if not index.isValid():
            return QVariant()

        if role == ConfigTreeModel.ROLE_KEY or role == Qt.DisplayRole:
            node = index.internalPointer()
            return node.key
        if role == ConfigTreeModel.ROLE_TYPE:
            return "int"
        if role == ConfigTreeModel.ROLE_VALUE:
            node = index.internalPointer()
            return node.node.get()
        return QVariant()

def main():
    engine.rootContext().setContextProperty("configTreeModel", None)
    
    engine.load(QUrl("qrc:/main.qml"))
    
    tcpsrc = sources.TCPTFISource(port=1235)
    iface = interface.Tfi(tcpsrc)
    config_nodes = interface.ConfigNodeList(iface)
    config_nodes_model = None

    refresh_timer = QTimer()
    
    dashboard_gauge_nodes = {}

    def refresh_dashboard():
        nonlocal config_nodes_model
        for node, gauge in dashboard_gauge_nodes.items():
            gauge.setProperty('value', node.get())

    def populate_config_model():
        nonlocal config_nodes_model
        config_nodes_model = ConfigTreeModel(None, config_nodes.nodes)
        engine.rootContext().setContextProperty("configTreeModel", config_nodes_model)

        print('populate')
        for objname, confname in [
                ('gaugeRPM', 'status.rpm'),
                ('gaugeIAT', 'status.sensors.iat'),
                ('gaugeCLT', 'status.sensors.clt'),
                ('gaugeBRV', 'status.sensors.brv'),
                ('gaugeMAP', 'status.sensors.map'),
                ('gaugeTPS', 'status.sensors.tps'),
                ('gaugeEGO', 'status.sensors.ego')
                ]:
            node = config_nodes.get_node_by_name(confname)
            gauge = engine.rootObjects()[0].findChild(QQuickItem, objname)
            if node:
                dashboard_gauge_nodes[node] = gauge
                node.read_complete.connect(refresh_dashboard)

        refresh_timer.timeout.connect(config_nodes_model.refresh)
        refresh_timer.start(50)
    
    config_nodes.listing_updated.connect(populate_config_model)
    
    tcpsrc.start()
    
    config_nodes.issue_list()
    
    app.exec()

main()
