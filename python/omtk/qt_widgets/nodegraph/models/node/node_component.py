import pymel.core as pymel

from omtk import decorators
from omtk.core import component
from omtk.core import entity_attribute
from omtk.vendor.Qt import QtGui

from omtk.qt_widgets.nodegraph.models.node import node_base, node_dg
from omtk.qt_widgets.nodegraph import pyflowgraph_node_widget

if False:
    from typing import List
    from omtk.qt_widgets.nodegraph.port_model import NodeGraphPortModel
    from omtk.qt_widgets.nodegraph.nodegraph_controller import NodeGraphController


class NodeGraphComponentModel(node_base.NodeGraphEntityModel):
    """
    Define the data model for a Node representing a Component.
    A Component is a special OMTK datatypes that consist of an input network, an output network and one or multiple
    maya nodes sandwitched in between.
    """

    def __init__(self, registry, entity):
        assert (isinstance(entity, component.Component))
        super(NodeGraphComponentModel, self).__init__(registry, entity)

    def __hash__(self):
        # todo: find a better way
        return hash(self._name)

    def delete(self):
        # todo: verify it work
        pymel.delete(self._entity.get_children())

    def get_children(self):
        return [
            self._registry.get_node_from_value(pynode)
            for pynode in self._entity.get_children()
        ]

    def get_nodes(self):
        return self._entity.get_children()

    @decorators.memoized_instancemethod
    def get_ports(self):
        # type: () -> List[NodeGraphPortModel]
        result = set()

        if not self._entity.is_built():
            return result

        for attr_def in self.get_ports_metadata():
            # todo: use a factory?
            # log.debug('{0}'.format(attr_def))
            inst = self._registry.get_port_model_from_value(attr_def)

            # inst._node = self  # hack currently compound attribute won't point to the compound object...
            if isinstance(attr_def, entity_attribute.EntityPymelAttribute):
                attr_node = attr_def._attr.node()
                if attr_node == self._entity.grp_inn:
                    attr_def._node = self._entity.grp_inn
                elif attr_node == self._entity.grp_out:
                    attr_def._node = self._entity.grp_out

            # inst = NodeGraphEntityPymelAttributePortModel(self._registry, self, attr_def)
            # self._registry._register_attribute(inst)
            result.add(inst)

        return result

    def allow_input_port_display(self, port_model, context=None):
        # type: (NodeGraphPortModel, NodeGraphController) -> bool
        """
        Component network attributes are inputs and outputs at the same time.
        For example, an input attribute is an output attribute when looking from inside the component.
        The NodeGraphController server as context holder.
        """
        # todo: cleanup private variable usage
        # If we are viewing the component content
        if context:
            if context._current_level_model == self:
                return port_model.get_parent().get_metadata() == self._entity.grp_inn
            else:
                return port_model.get_parent().get_metadata() == self._entity.grp_out
        return super(NodeGraphComponentModel, self).allow_input_port_display(port_model)

    def allow_output_port_display(self, port_model, context=None):
        # type: (NodeGraphController, NodeGraphPortModel) -> bool
        """
        Component network attributes are inputs and outputs at the same time.
        For example, an output attribute is an input attribute when looking from inside the component.
        The NodeGraphController server as context holder.
        """
        # todo: cleanup private variable usage
        # If we are viewing the component content
        if context:
            if context._current_level_model == self:
                return port_model.get_parent() == self._entity.grp_out
            else:
                return port_model.get_parent() == self._entity.grp_inn
        return super(NodeGraphComponentModel, self).allow_output_port_display(port_model)

        # def _get_node_widget_label(self):
        #     return '{0} v{1}'.format(self._name, self._entity.version)

    def _get_widget_cls(self):
        return pyflowgraph_node_widget.OmtkNodeGraphComponentNodeWidget


class NodeGraphComponentBoundBaseModel(node_dg.NodeGraphDgNodeModel):
    """
    Since dagnode contain input and output network that define their bound, it is usefull for us
    to have access to a dedicated model for the bounds that point to the compound model.
    """

    def __init__(self, registry, pynode, component):
        super(NodeGraphComponentBoundBaseModel, self).__init__(registry, pynode)
        self._component = component

    # todo: deprecate in favor of .get_parent()
    # @libPython.memoized_instancemethod
    def _get_component(self):
        # type(): () -> Component
        # net = libComponents.get_component_metanetwork_from_hub_network(self._pynode)
        # inst = self._registry._manager.import_network(net)
        # return inst
        return self._component

    def get_parent(self):
        return self._get_component()


class NodeGraphComponentInnBoundModel(NodeGraphComponentBoundBaseModel):
    _widget_background_color = QtGui.QColor(0, 195, 227)

    def get_widget(self, graph, ctrl):
        # debugging
        widget = super(NodeGraphComponentBoundBaseModel, self).get_widget(graph, ctrl)
        color = self._widget_background_color
        widget.setColor(color)
        return widget


class NodeGraphComponentOutBoundModel(NodeGraphComponentBoundBaseModel):
    _widget_background_color = QtGui.QColor(255, 69, 84)

    def get_widget(self, graph, ctrl):
        # debugging
        widget = super(NodeGraphComponentBoundBaseModel, self).get_widget(graph, ctrl)
        color = self._widget_background_color
        widget.setColor(color)
        return widget