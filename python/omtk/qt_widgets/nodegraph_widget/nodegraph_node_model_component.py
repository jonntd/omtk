from omtk.libs import libPython
from . import nodegraph_node_model_base

if False:
    from .nodegraph_port_model import NodeGraphPortModel
    from .nodegraph_controller import NodeGraphController


class NodeGraphComponentModel(nodegraph_node_model_base.NodeGraphEntityModel):
    """
    Define the data model for a Node representing a Component.
    A Component is a special OMTK datatypes that consist of an input network, an output network and one or multiple
    maya nodes sandwitched in between.
    """

    def get_children(self):
        return [
            self._registry.get_node_from_value(pynode)
            for pynode in self._entity.get_children()
        ]

    @libPython.memoized_instancemethod
    def get_attributes(self):
        # type: () -> List[NodeGraphPortModel]
        if not self._entity.is_built():
            return set()

        return super(NodeGraphComponentModel, self).get_attributes()

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
            if context._current_level == self:
                return port_model.get_parent().get_metadata() == self._entity.grp_out
            else:
                return port_model.get_parent().get_metadata() == self._entity.grp_inn
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
            if context._current_level == self:
                return port_model.get_parent().get_metadata() == self._entity.grp_inn
            else:
                return port_model.get_parent().get_metadata() == self._entity.grp_out
        return super(NodeGraphComponentModel, self).allow_output_port_display(port_model)

        # def _get_node_widget_label(self):
        #     return '{0} v{1}'.format(self._name, self._entity.version)