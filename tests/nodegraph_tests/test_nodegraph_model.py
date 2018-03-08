"""
Ensure propre behaviour or the GraphController, GraphRegistry and every related models.
"""
import logging
import unittest

import pymel.core as pymel
from maya import cmds
from omtk.libs import libComponents
from omtk.libs import libRigging
from omtk.qt_widgets.nodegraph.nodegraph_controller import NodeGraphController
from omtk.qt_widgets.nodegraph.nodegraph_registry import NodeGraphRegistry
from omtk.qt_widgets.nodegraph.models import NodeGraphModel

log = logging.getLogger('omtk')
log.setLevel(logging.DEBUG)


class GraphRegistryTest(unittest.TestCase):
    def setUp(self):
        self._registry = NodeGraphRegistry()
        self._model = NodeGraphModel()
        self.controller = NodeGraphController(self._model)
        cmds.file(new=True, force=True)

    # def test_node_model_from_transform(self):
    #     """Ensure that we are able to read a simplement transform node and it's attributes."""
    #     transform_src = pymel.createNode('transform')
    #     transform_dst = pymel.createNode('transform')
    #     pymel.connectAttr(transform_src.translateX, transform_dst.translateX)
    #     node = self.registry.get_node_from_value(transform_src)
    #     attributes = node.get_connected_output_ports()
    #     print(len(attributes))
    #     for a in sorted(attributes):
    #         print a

    def _create_simple_compound(self):
        transform_src = pymel.createNode('transform')
        transform_dst = pymel.createNode('transform')
        util_logic = libRigging.create_utility_node(
            'multiplyDivide',
            input1X=transform_src.translateX,
        )

        # todo: make this work with compound and multi attribute!
        # pymel.connectAttr(util_logic.output, transform_dst.translate)

        pymel.connectAttr(util_logic.outputX, transform_dst.translateY)

        component = libComponents.create_component_from_bounds([transform_src, transform_dst])
        return component

    def test_component_loading(self):
        """Ensure the registry is able to load a component and it's children."""
        self.assertEqual(0, len(self._registry._nodes))

        component = self._create_simple_compound()
        node_model, node_widget = self.controller.add_node(component)

        self.assertEqual(1, len(self._registry._nodes))

        inn_attrs = node_model.get_input_ports()
        out_attrs = node_model.get_output_ports()

        self.assertEqual(1, len(inn_attrs))
        self.assertEqual('translateX', inn_attrs[0].get_name())
        self.assertEqual(1, len(out_attrs))
        self.assertEqual('translateY', inn_attrs[0].get_name())


if __name__ == '__main__':
    unittest.main()

    # todo: test discovery of nodes in a specific compound space