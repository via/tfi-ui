import serial
import copy
import re
import time
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QThread, QMutex, QMutexLocker, QTimer

class Tfi(QObject):

    feed_update = pyqtSignal()
    sendCommand = pyqtSignal(str)

    def __init__(self, source):
        super(Tfi, self).__init__()
        self.lock = QMutex()
        self.fields = []

        self.command_queue = [{
            "callback": self._read_feed_vars,
            "command": "get config.feed",
            }]

        self.sendCommand.connect(source.sendCommand)
        source.packetArrived.connect(self.process_packet, Qt.QueuedConnection)

        self._send_command()

    def get(self, var, cb):
        self.command_queue.append({
            "callback": cb,
            "command": "get {0}".format(var),
        }) 
        self._send_command()

    def set(self, var, val, cb):
        self.command_queue.append({
            "callback": cb,
            "command": "set {0} {1}".format(var, val),
        }) 
        self._send_command()

    def list(self, prefix, cb):
        self.command_queue.append({
            "callback": cb,
            "command": "list {0}".format(prefix),
        }) 
        self._send_command()

    def _expire_command(self):
        del self.command_queue[0]["timer"]
        self.command_queue[0]["expired"] = True
        self.command_queue[0]["sent"] = False
        self._send_command()
        
    def _set_timeout(self, cmd, timeout):
        timeout_timer = QTimer()
        timeout_timer.setSingleShot(True)
        timeout_timer.timeout.connect(self._expire_command)
        timeout_timer.start(timeout)
        cmd["timer"] = timeout_timer

    def _send_command(self):
        if "sent" not in  self.command_queue[0]:
            self.command_queue[0]["sent"] = True
            self._set_timeout(self.command_queue[0], 10000)
            self.sendCommand.emit(self.command_queue[0]["command"])

    def _finish_command_response(self, line, success):
        if not len(self.command_queue):
            print("ERROR")
            return
        del self.command_queue[0]["timer"]
        self.command_queue[0]["callback"](line, success)
        del self.command_queue[0]
        if len(self.command_queue) > 0:
            self._send_command()
    
    def _read_feed_vars(self, line, success):
        if success:
            self.fields = line.split(',')

    def process_packet(self, feedline):
        feedline = str(feedline)
        packet = {}

        if feedline.startswith("* "):
            self._finish_command_response(feedline[2:].rstrip(), True)
            return
        if feedline.startswith("- "):
            self._finish_command_response(feedline[2:].rstrip(), False)
            return

        if len(self.fields) == 0:
            return
        parts = feedline.rstrip().split(',')

        locker = QMutexLocker(self.lock)
        try:
            self.status = dict(zip(self.fields, parts))
        except:
            return
        finally:
            locker.unlock()
        self.feed_update.emit()

    def get_status(self):
        locker = QMutexLocker(self.lock)
        return copy.copy(self.status)

class TfiConfigNode(QObject):
    read_complete = pyqtSignal()
    write_complete = pyqtSignal()
    
    def __init__(self, interface, node):
        super(TfiConfigNode, self).__init__()
       
        self.name = node
        self.interface = interface
        self.value = None
        self.issue_read()

    def get(self):
        return self.value

    def issue_read(self):
        def _read_cb(line, success):
            if not success:
                return
            self.value = line
            self.read_complete.emit()
        self.interface.get(self.name, _read_cb)

    def issue_write(self, val):
        pass

    def _is_table(self):
        return self.name.startswith("config.table.")

    def _is_sensor(self):
        return self.name.startswith("config.sensor.")

    def _is_event(self):
        return self.name == "config.events"

class TfiSensorConfigNode(TfiConfigNode):
    def __init__(self, interface, node):
        super(TfiSensorConfigNode, self).__init__(interface, node)

class ConfigNodeList(QObject):
    listing_updated = pyqtSignal()
    feedline_updated = pyqtSignal()

    special_nodes = {
            "flash" : None,
            "stats" : None,
            "config.sensors.": TfiSensorConfigNode,
            }

    def __init__(self, interface):
        super(ConfigNodeList, self).__init__()
        self.interface = interface
        self.interface.feed_update.connect(self._update_feedline)
        self.nodes = {}

    def _update_feedline(self):
        fields = self.interface.get_status()
        for key, val in fields.items():
            n = self.get_node_by_name(key)
            if n:
                n.value = val
                n.read_complete.emit()
        self.feedline_updated.emit()

    def get_node_by_name(self, name):
        if name in self.nodes:
            return self.nodes[name]
        return None

    def issue_list(self):
        self.interface.list("", self._listing_cb)

    def _node_constructor(self, node):
        for special in self.special_nodes:
            if node.startswith(special):
                return self.special_nodes[special]
        return TfiConfigNode

    def _listing_cb(self, ns, success):
        ns = ns.split(' ')
        for node in ns:
            cons = self._node_constructor(node)
            if cons:
                self.nodes[node] = cons(self.interface, node)
        self.listing_updated.emit()

