from omtk.libs import libPython
from . import nodegraph_node_model_base


class NodeGraphNodeRigModel(nodegraph_node_model_base.NodeGraphEntityModel):
    # todo: move to base class?
    def get_children(self):
        result = set()
        for sub_component in self._entity.iter_sub_components():
            child = self._registry.get_node_from_value(sub_component)
            result.add(child)
        return result