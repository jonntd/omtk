import pymel.core as pymel
from . import graph_proxy_model
from omtk.core import session
from omtk.qt_widgets.nodegraph.models.node import node_component
from omtk.vendor.enum34 import Enum

if False:
    from typing import List, Generator
    from omtk.qt_widgets.nodegraph.models import NodeGraphNodeModel


class GraphComponentProxyFilterModel(graph_proxy_model.NodeGraphGraphProxyModel):
    def __init__(self, model=None, level=None):
        super(GraphComponentProxyFilterModel, self).__init__(model=model)

        self._level = None
        if level:
            self.set_level(level)

        self._cur_level_bound_inn = None
        self._cur_level_bound_out = None
        self._cur_level_children = None
        self._bound_inn_dirty = False
        self._bound_out_dirty = False
        self._children_dirty = False
        self._need_refresh = False

    def get_level(self):
        # type: () -> NodeGraphNodeModel
        return self._level

    def set_level(self, level):
        # type: (NodeGraphNodeModel | None) -> None
        # assert(isinstance(level, node_component.NodeGraphComponentModel))

        self.onAboutToBeReset.emit()  # hack
        self._level = level
        self.reset()  # is this the right call? do we need to define a clear?

        if level is None:  # root level
            self._cur_level_bound_inn = None
            self._cur_level_bound_out = None
            self._cur_level_children = []
        else:
            self._bound_inn_dirty = False
            self._bound_out_dirty = False

            registry = level._registry

            # Pre-allocate bounds on Component levels
            if isinstance(level, node_component.NodeGraphComponentModel):
                c = level.get_metadata()

                c_model = registry.get_node_from_value(c)

                new_nodes = []

                if c.grp_inn:
                    g = node_component.NodeGraphComponentInnBoundModel(registry, c.grp_inn, c_model)
                    self._cur_level_bound_inn = g
                    new_nodes.append(g)

                if c.grp_out:
                    g = node_component.NodeGraphComponentOutBoundModel(registry, c.grp_out, c_model)
                    self._cur_level_bound_out = g
                    new_nodes.append(g)

                self._cur_level_children = [registry.get_node_from_value(child) for child in c.get_children()]

                new_nodes.extend(self._cur_level_children)

                for node in new_nodes:
                    self.add_node(node)
                    self.expand_node_ports(node)

                for node in new_nodes:
                    self.expand_node_connections(node)

                # for child in self._cur_level_children:
                #     self.add_node(child)
                #     self.expand_node_ports(child)
                #     self.expand_node_connections(child)

                self._children_dirty = False
                self._need_refresh = True

        # self.reset()  # we need to refresh everything

    # todo: move upper?
    def expand_node_ports(self, node):
        # type: (NodeGraphNodeModel) -> None
        """
        Show all available attributes for a PyFlowgraph Node.
        Add it in the pool if it didn't previously exist.
        :return:
        """
        for port_model in sorted(self.iter_node_ports(node)):
            self.add_port(port_model, emit_signal=True)

    # todo: move upper?
    def expand_node_connections(self, node, inputs=True, outputs=True):
        # type: (NodeGraphNodeModel, bool, bool) -> None
        for connection in self.iter_node_connections(node, inputs=inputs, outputs=outputs):
            self._model.add_connection(connection)

    def can_show_node(self, node):
        # type: (NodeGraphNodeModel) -> bool
        return node.get_parent() == self._level

    def can_show_port(self, port):
        node = port.get_parent()
        if isinstance(node, node_component.NodeGraphComponentBoundBaseModel):
            if not port.is_user_defined():
                return False
        return super(GraphComponentProxyFilterModel, self).can_show_port(port)

    def can_show_connection(self, connection):
        return True

    # still used?
    def intercept_node(self, node):
        # type: (NodeGraphNodeModel) -> Generator[NodeGraphNodeModel]
        s = session.get_session()
        registry = node._registry

        pynode = node.get_metadata()
        c = s.get_component_from_obj(pynode) if isinstance(pynode, pymel.PyNode) else None

        # If we just entered a level, yield the bound
        if self._level and self._need_refresh:
            self._need_refresh = False
            if self._cur_level_bound_inn:
                yield self._cur_level_bound_inn

            if self._cur_level_bound_out:
                yield self._cur_level_bound_out

            for child in self._cur_level_children:
                yield child

        if c:
            # If we are inside the component, should it's input and output hub.
            # Otherwise show only the component.
            if self._level and c == self._level.get_metadata():
               pass
            else:
                yield registry.get_node_from_value(c)
            return
        else:
            # If the object parent is NOT a compound and we are NOT at root level, the object is hidden.
            # We decided to hide the object here instead of in can_show_node in case the user
            if self._level:
                print("Hiding {}".format(node))
                return

        yield node

    def intercept_port(self, port):
        registry = port._registry
        s = session.get_session()
        node = port.get_parent()
        pynode = node.get_metadata()
        component_data= s.get_component_from_obj(pynode) if isinstance(pynode, pymel.PyNode) else None

        if component_data:
            component = registry.get_node_from_value(component_data)
            if component != self._level:
                pass

        yield port

    def intercept_connection(self, connection):
        from omtk.core import component
        def _get_port_by_name(node, name):
            for port in node.iter_ports():
                if port.get_name() == name:
                    return port

        # If we encounter a connection to an hub node and we are NOT in the compound, we want to replace it with
        # a conenction to the compound itself.
        registry = connection._registry
        s = session.get_session()

        need_swap = False
        port_src = connection.get_source()
        port_dst = connection.get_destination()
        node_src = port_src.get_parent()
        node_dst = port_dst.get_parent()

        node_src_data = node_src.get_metadata()
        node_dst_data = node_dst.get_metadata()

        # If the source is the current compount, remap the connection to the hub inn.
        if isinstance(node_src_data, component.Component) and self._level and self._level.get_metadata() == node_src_data:
            # Ignore internal connection
            if node_dst.get_parent() != self._level:
                return
            attr = node_src_data.grp_inn.attr(port_src.get_name())
            port_src = registry.get_port_model_from_value(attr)
            need_swap = True

        # If the connection to an output hub?
        elif isinstance(node_src_data, pymel.PyNode):
            c = s.get_component_from_obj(node_src_data)
            if c:
                c_model = registry.get_node_from_value(c)
                if self._level != c_model:
                    # Get the replacement port, it have the same name as the current port.
                    port_src = _get_port_by_name(c_model, port_src.get_name())
                    need_swap = True
                else:
                    # the source is from the component output, this mean that the connection cannot be shown
                    if isinstance(node_dst_data, pymel.PyNode):
                        c2 = s.get_component_from_obj(node_dst_data)
                        if c2 != c:
                            return

        # If the destination is the current compound, remap the connection to the hub out.
        if isinstance(node_dst_data, component.Component) and self._level and self._level.get_metadata() == node_dst_data:
            # Ignore external connection
            if node_src.get_parent() != self._level:
                return
            attr = node_dst_data.grp_out.attr(port_dst.get_name())
            port_dst = registry.get_port_model_from_value(attr)
            need_swap = True

        # If the connection from an input hub?
        elif isinstance(node_dst_data, pymel.PyNode):
            c = s.get_component_from_obj(node_dst_data)
            if c:
                c_model = registry.get_node_from_value(c)
                if self._level != c_model:
                    # Get the replacement port, it have the same name as the current port.
                    port_dst = _get_port_by_name(c_model, port_dst.get_name())
                    need_swap = True
                else:
                    # the destination is from the component input, this mean that that connection cannot be shown
                    if isinstance(node_src_data, pymel.PyNode):
                        c2 = s.get_component_from_obj(node_src_data)
                        if c2 != c:
                            return

        if need_swap:
            yield registry.get_connection_model_from_values(port_src, port_dst)
        else:
            yield connection

    def iter_nodes(self):
        for node in super(GraphComponentProxyFilterModel, self).iter_nodes():
            for yielded in self.intercept_node(node):
                yield yielded

    def iter_node_ports(self, node):
        for port in super(GraphComponentProxyFilterModel, self).iter_node_ports(node):
            for yielded in self.intercept_port(port):
                yield yielded

    def _iter_node_output_connections(self, node_model):
        for port in node_model.get_connected_output_ports(self):
            if not self.can_show_port(port):
                continue

            for connection_model in self.iter_port_output_connections(port):
                node_model_dst = connection_model.get_destination().get_parent()
                for yielded in self.intercept_connection(connection_model, port):
                    yield yielded

    def _iter_node_input_connections(self, node_model):
        for port_model in node_model.get_connected_input_ports():
            if not self.can_show_port(port_model):
                continue

            for connection_model in self.iter_port_input_connections(port_model):
                node_model_src = connection_model.get_source().get_parent()

                for yielded in self.intercept_connection(connection_model, port_model):
                    yield yielded

    def iter_port_input_connections(self, model):
        # type: (NodeGraphPortModel) -> List[NodeGraphPortModel]
        """
        Control what output connection models are exposed for the provided port model.
        :param model: The source port model to use while resolving the connection models.
        :return: A list of connection models using the provided port model as source.
        """
        for connection in model.get_input_connections():
            if self.can_show_connection(connection):
                for yielded in self.intercept_connection(connection):
                    yield yielded

    def iter_port_output_connections(self, model):
        # type: (NodeGraphPortModel) -> List[NodeGraphPortModel]
        """
        Control what output connection models are exposed for the provided port model.
        :param model: The source port model to use while resolving the connection models.
        :return: A list of connection models using the provided port model as source.
        """
        for connection in model.get_output_connections():
            if self.can_show_connection(connection):
                for yielded in self.intercept_connection(connection):
                    yield yielded

    # def collapse_node_attributes(self, node_model):
    #     # There's no API method to remove a port in PyFlowgraph.
    #     # For now, we'll just re-created the node.
    #     # node_widget = self.get_node_widget(node_model)
    #     # self._view.removeNode(node_widget)
    #     # self.get_node_widget.cache[node_model]  # clear cache
    #     # node_widget = self.get_node_widget(node_model)
    #     # self._view.addNode(node_widget)
    #     raise NotImplementedError

    # def iter_port_connections(self, port):
    #     # type: (NodeGraphPortModel) -> Generator[NodeGraphConnectionModel]
    #     for connection in self.iter_port_input_connections(port):
    #         yield self.intercept_connection(connection, port)
    #     for connection in self.iter_port_output_connections(port):
    #         yield self.intercept_connection(connection, port)
    #
    # def get_port_connections(self, port):
    #     return list(self.iter_port_connections(port))
    #
    # def iter_port_input_connections(self, port):
    #     # type: (NodeGraphPortModel) -> list[NodeGraphConnectionModel]
    #     """
    #     Control what input connection models are exposed for the provided port model.
    #     :param model: The destination port model to use while resolving the connection models.
    #     :return: A list of connection models using the provided port model as destination.
    #     """
    #     for connection in self._model.iter_port_input_connections(port):
    #         for yielded in self.intercept_connection(connection, port):
    #             yield yielded
    #
    # @decorators.memoized_instancemethod
    # def get_port_input_connections(self, model):
    #     return list(self.iter_port_input_connections(model))  # cannot memoize a generator
    #
    # def iter_port_output_connections(self, port):
    #     # type: (NodeGraphPortModel) -> List[NodeGraphPortModel]
    #     """
    #     Control what output connection models are exposed for the provided port model.
    #     :param port: The source port model to use while resolving the connection models.
    #     :return: A list of connection models using the provided port model as source.
    #     """
    #     for connection in self._model.iter_port_output_connections(port):
    #         for yielded in self.intercept_connection(connection, port):
    #             yield yielded

    # @decorators.memoized_instancemethod
    # def get_port_output_connections(self, model):
    #     return list(self.iter_port_output_connections(model))  # cannot memoize a generator
    #
    # def expand_port(self, port, inputs=True, outputs=True):
    #     # type: (NodeGraphPortModel, bool, bool) -> None
    #     self._model.expand_port(port, inputs=inputs, outputs=outputs)
    #
    # def expand_port_input_connections(self, port):
    #     self._model.expand_port_input_connections(port)
    #
    # def expand_port_output_connections(self, port):
    #     self._model.expand_port_output_connections(port)
    #
    # def expand_node_ports(self, node, inputs=True, outputs=True):
    #     # type: (NodeGraphNodeModel, bool, bool) -> None
    #     self._model.expand_node_connections(node, inputs=True, outputs=True)

    def get_connection_parent(self, connection):
        # type: (NodeGraphNodeModel) -> NodeGraphNodeModel
        """
        By default, a connection parent is either the same as it's input attribute or it's output attribute.
        This difference is important with Compound nodes.
        :return:
        """
        port_src = connection.get_source()
        port_dst = connection.get_destination()
        node_src = port_src.get_parent()
        node_dst = port_dst.get_parent()

        # If the connection if from a component, this is an external connection.
        if isinstance(node_src, node_component.NodeGraphComponentModel):
            return node_src.get_parent()
        if isinstance(node_dst, node_component.NodeGraphComponentModel):
            return node_dst.get_parent()

        pynode_src = node_src.get_metadata()
        pynode_dst = node_dst.get_metadata()

        class ConnectionKind(Enum):
            normal = 1
            normal_to_compound_inn = 2  # src (node is outside the compound)
            normal_to_compound_out = 3  # dst (node is inside the compound)
            compound_inn_to_normal = 4  # src (node is inside the compound)
            compound_out_to_normal = 5  # dst (node is outside the compound)
            compound_inn_to_compound_inn = 6  # dst (destination is inside source)
            compound_inn_to_compound_out = 7  # any (source and destination are inside the same compound)
            compound_out_to_compound_inn = 8  # any (source and destination are inside the same compound)
            compound_out_to_compound_out = 9  # src (source is inside destination)

        def get_connection_kind():
            """
            The possibilities are:
            - Connection from a component out to a component on the same level.
            - Connection from a component inn to a component inn inside this same component.
            - Connection from a component out to a parent component out.
            """
            from omtk.libs import libComponents
            src_role = libComponents.get_metanetwork_role(pynode_src)
            dst_role = libComponents.get_metanetwork_role(pynode_dst)

            src_is_compound_bound = src_role != libComponents.ComponentMetanetworkRole.NoRole
            dst_is_compound_bound = dst_role != libComponents.ComponentMetanetworkRole.NoRole
            if src_is_compound_bound and dst_is_compound_bound:
                src_is_inn = src_role == libComponents.ComponentMetanetworkRole.Inn
                dst_is_inn = dst_role == libComponents.ComponentMetanetworkRole.Out
                # Connection from a component inn to another component inn.
                # In that case the destination component is a child of the source component.
                if src_is_inn and dst_is_inn:
                    return ConnectionKind.compound_inn_to_compound_inn
                # Connection from a component inn to a component out.
                # In that case the connection is from the same component (or there's something really wrong in the scene).
                # In that case both src and dst are in the same space.
                elif src_is_inn and not dst_is_inn:
                    return ConnectionKind.compound_inn_to_compound_out
                # Connection from a component out to a component inn
                # In that case the source component is a child of the destination component.
                elif not src_is_inn and dst_is_inn:
                    return ConnectionKind.compound_out_to_compound_inn
                # Connection from a component out to a component out
                # In that case the source component is a child of the destination component.
                else:
                    return ConnectionKind.compound_out_to_compound_out

            elif src_is_compound_bound:  # exiting a compounds
                src_is_inn = src_role == libComponents.ComponentMetanetworkRole.Inn
                if src_is_inn:
                    return ConnectionKind.compound_inn_to_normal
                else:
                    return ConnectionKind.compound_out_to_normal
            elif dst_is_compound_bound:  # entering a compound
                dst_is_inn = dst_role == libComponents.ComponentMetanetworkRole.Inn
                if dst_is_inn:
                    return ConnectionKind.normal_to_compound_inn
                else:
                    return ConnectionKind.normal_to_compound_out

        def get_connection_node_model():
            """
            Define if we should use the source or destination node model to fetch the parent.
            normal_to_compound_inn = 2  # src (node is outside the compound)
            normal_to_compound_out = 3  # dst (node is inside the compound)
            compound_inn_to_normal = 4  # src (node is inside the compound)
            compound_out_to_normal = 5  # dst (node is outside the compound)
            compound_inn_to_compound_inn = 6  # dst (destination is inside source)
            compound_inn_to_compound_out = 7  # any (source and destination are inside the same compound)
            compound_out_to_compound_inn = 8  # any (source and destination are inside the same compound)
            compound_out_to_compound_out = 9  # src (source is inside destination)
            """
            connection_kind = get_connection_kind()
            if connection_kind in (
                ConnectionKind.compound_inn_to_normal,
                ConnectionKind.compound_inn_to_compound_inn,
                ConnectionKind.compound_out_to_compound_out,
                ConnectionKind.compound_out_to_normal,
            ):
                return node_dst
            else:
                return node_src

        node_model = get_connection_node_model()
        return node_model

