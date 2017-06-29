import logging

import pymel.core as pymel
from omtk import factory_datatypes
from omtk.core.classComponent import Component
from omtk.libs import libPython
from omtk.libs import libComponents
from omtk.vendor import libSerialization
from omtk.core import classEntityAttribute
from .nodegraph_node_model import NodeGraphDagNodeModel, NodeGraphComponentModel
from .nodegraph_port_model import NodeGraphPortModel, NodeGraphPymelPortModel
from .nodegraph_connection_model import NodeGraphConnectionModel

log = logging.getLogger('omtk')


class NodeGraphModel(object):
    """
    This class act a sort of global cache for the multiple models that compose the GraphView.
    This allow multiple view can re-use the same data.
    """

    def __init__(self):
        self._nodes = set()
        self._attributes = set()
        self._connections = set()

        self._nodes_by_metadata = {}

    # --- Registration methods ---

    def _register_node(self, inst):
        self._nodes.add(inst)

    def _register_attribute(self, inst):
        self._attributes.add(inst)

    def _register_connections(self, inst):
        self._connections.add(inst)

    # --- Access methods ---

    @libPython.memoized_instancemethod
    def get_node_from_value(self, val):
        # type: (object) -> GraphNodeModel
        """
        Public entry point to access a Node from a provided value.
        This handle all the caching and registration.
        """
        log.debug('Exploring new value {0}'.format(val))
        data_type = factory_datatypes.get_component_attribute_type(val)
        if data_type == factory_datatypes.AttributeType.Component:
            return NodeGraphComponentModel(self, val)

        if data_type == factory_datatypes.AttributeType.Node:
            network = None
            if isinstance(val, pymel.nodetypes.Network):
                if libSerialization.is_network_from_class(val, Component.__name__):
                    network = val
                else:
                    network = libComponents.get_component_metanetwork_from_hub_network(val)
            if network:
                component = libSerialization.import_network(network)
                return NodeGraphComponentModel(self, component)

            return NodeGraphDagNodeModel(self, val)

        raise Exception("Unsupported value {0} of type {1}".format(
            val, data_type
        ))
        # self._register_node(inst)
        # return inst

    @libPython.memoized_instancemethod
    def get_port_model_from_value(self, attr):
        # type: () -> List[NodeGraphPortModel]
        # todo: add support for pure EntityAttribute
        if isinstance(attr, classEntityAttribute.EntityPymelAttribute):
            node_model = self.get_node_from_value(attr._attr.node())
            # Let EntityAttribute defined if they are inputs or outputs
            inst = NodeGraphPymelPortModel(self, node_model, attr)
        elif isinstance(attr, classEntityAttribute.EntityAttribute):
            raise NotImplementedError
        else:
            node_model = self.get_node_from_value(attr.node())
            inst = NodeGraphPymelPortModel(self, node_model, attr)
        self._register_attribute(inst)
        return inst

    @libPython.memoized_instancemethod
    def get_connection_model_from_values(self, model_src, model_dst):
        if not isinstance(model_src, NodeGraphPortModel):
            model_src = self.get_port_model_from_value(model_src)

        if not isinstance(model_dst, NodeGraphPortModel):
            model_dst = self.get_port_model_from_value(model_dst)

        inst = NodeGraphConnectionModel(self, None, model_src, model_dst)
        self._register_connections(inst)
        return inst

    # def walk_inside_component(self, component):
    #     # type: (NodeGraphComponentModel) -> None


    def iter_nodes_from_parent(self, parent):
        for node in self._nodes:
            if node.get_parent() == parent:
                yield node