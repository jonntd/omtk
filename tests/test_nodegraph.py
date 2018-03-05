import unittest
import pymel.core as pymel
from omtk.qt_widgets.nodegraph import NodeGraphModel, NodeGraphController, NodeGraphView, \
    NodeGraphControllerFilter, NodeGraphProxyModel
from omtk.vendor.Qt import QtCore, QtGui, QtWidgets
from maya import cmds

def _port_model_to_json(port_model):
    return {
        'name': port_model.get_name(),
        'readable': port_model.is_readable(),
        'writable': port_model.is_writable(),
    }


def _node_model_to_json(graph_model, node_model):
    ports_models = graph_model.get_node_model_ports(node_model)
    return {
        'name': node_model.get_name(),
        'ports': sorted(
            [_port_model_to_json(port_model) for port_model in ports_models])
    }


class TestRawNodeGraph(unittest.TestCase):

    def setUp(self):
        cmds.file(new=True, force=True)
        self.model = NodeGraphModel()
        self.filter = NodeGraphControllerFilter(self.model)
        # self.controller = NodeGraphController(self.model)

    def test_dg_node(self):
        obj = pymel.createNode('multMatrix')
        node_model = self.model.get_node_model_from_value(obj)

        self.assertDictEqual(
            _node_model_to_json(self.model, node_model),
            {
                'name': u'multMatrix1',
                'ports': [
                    {'writable': True, 'readable': True, 'name': u'binMembership'},
                    {'writable': True, 'readable': True, 'name': u'caching'},
                    {'writable': True, 'readable': True, 'name': u'frozen'},
                    {'writable': True, 'readable': True, 'name': u'isHistoricallyInteresting'},
                    {'writable': True, 'readable': True, 'name': u'matrixIn'},
                    {'writable': True, 'readable': True, 'name': u'matrixIn[1]'},
                    {'writable': False, 'readable': True, 'name': u'matrixSum'},
                    {'writable': False, 'readable': True, 'name': u'message'},
                    {'writable': True, 'readable': True, 'name': u'nodeState'}
                ]
            }
        )

    def test_dag_node(self):
        """Ensure that we are able to represent a single transform."""
        obj = pymel.createNode('transform')
        node_model = self.model.get_node_model_from_value(obj)

        print _node_model_to_json(self.model, node_model)

        pass

    def test_simple_connection(self):
        """Ensure that we are able to represent a single connection."""

    def test_create_compound(self):
        """Ensure that we are able to create a compound."""


class TestProxyNodeGraph(unittest.TestCase):
    def setUp(self):
        cmds.file(new=True, force=True)
        self.source_model = NodeGraphModel()
        self.model = NodeGraphProxyModel(self.source_model)
        self.filter = NodeGraphControllerFilter(self.model)
        self.model.set_filter(self.filter)
        # self.controller = NodeGraphController(self.model)

    def test_dg_node(self):
        obj = pymel.createNode('multMatrix')
        node_model = self.model.get_node_model_from_value(obj)

        self.assertDictEqual(
            _node_model_to_json(self.model, node_model),
            {
                'name': u'multMatrix1',
                'ports': [
                    {'writable': True, 'readable': True, 'name': u'matrixIn'},
                    {'writable': True, 'readable': True, 'name': u'matrixIn[1]'},
                    {'writable': False, 'readable': True, 'name': u'matrixSum'}
                ]
            }
        )


if __name__ == '__main__':
    unittest.main()
