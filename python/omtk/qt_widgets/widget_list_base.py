import logging
import re

import pymel.core as pymel
from omtk import factory_tree_widget_item, factory_rc_menu
from omtk import ui_shared
from omtk.core import classModule
from omtk.core.classEntity import Entity
from omtk.core.classNode import Node
from omtk.decorators import log_info
from omtk.libs import libQt
from omtk.qt_widgets.ui import widget_list_modules
from omtk.vendor.Qt import QtCore, QtWidgets

log = logging.getLogger('omtk')


class OmtkBaseListWidget(QtWidgets.QWidget):
    actionRequested = QtCore.Signal(list)

    def __init__(self, parent=None):
        super(OmtkBaseListWidget, self).__init__(parent=parent)

        self._rig = None
        self._rigs = []
        self._is_modifying = False  # todo: document
        self._listen_events = True  # todo: replace by blockSignal calls?

        # Used to prevent cyclic dependencies
        # todo: use a solver class?
        self._known_data_ids = set()

        self.ui = widget_list_modules.Ui_Form()
        self.ui.setupUi(self)

        # Tweak gui
        self.ui.treeWidget.setStyleSheet(ui_shared._STYLE_SHEET)

        # Configure drag&drop
        self.ui.treeWidget.setDragDropOverwriteMode(False)
        self.ui.treeWidget.setDragEnabled(True)

        # Connect signal

        # Connect events
        self.ui.lineEdit_search.textChanged.connect(self.on_search_changed)
        self.ui.treeWidget.itemSelectionChanged.connect(self.on_selection_changed)
        self.ui.treeWidget.itemChanged.connect(self.on_module_changed)
        self.ui.treeWidget.itemDoubleClicked.connect(self.on_module_double_clicked)
        self.ui.treeWidget.focusInEvent = self.on_tree_focus
        self.ui.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.treeWidget.customContextMenuRequested.connect(self.on_context_menu_request)
        self.ui.btn_update.pressed.connect(self.update)

        self.update()

    def iter_selected_items(self):
        return iter(self.ui.treeWidget.selectedItems())

    def iter_selected_objects(self):
        # type:() -> [pymel.PyNode]
        """
        Get the Maya objects associated with the selection.
        :return: A list of pymel.PyNode instances.
        """
        result = []
        for item in self.iter_selected_items():
            try:
                metadata = item._metadata
            except AttributeError:
                continue

            if isinstance(metadata, Node):
                result.append(metadata)
            elif hasattr(metadata, '_network'):
                result.append(metadata._network)
            elif hasattr(metadata, '__melobject__'):
                result.append(metadata)
            else:
                print("Unexpected metadata type: {0}".format(metadata))

        return result

    @log_info
    def get_selected_entries(self):
        """
        Return the metadata stored in each selected row. Whatever the metadata type (can be Rig or Module).
        :return: A list of object instances.
        """
        return [item._meta_data for item in self.iter_selected_items()]

    @log_info
    def get_selected_modules(self):
        """
        Return the Module instances stored in each selected rows.
        :return: A list of Module instances.
        """
        return [item._meta_data for item in self.iter_selected_items() if item._meta_type == ui_shared.MimeTypes.Module]

    @log_info
    def get_selected_rigs(self):
        """
        Return the Rig instances stored in each selected rows.
        :return: A list of Rig instances.
        """
        return [item._meta_data for item in self.iter_selected_items() if item._meta_type == ui_shared.MimeTypes.Rig]

    @log_info
    def get_selected_components(self):
        """
        Return the Component instance stored in each selected rows.
        :return: A list of Component instances.
        """
        return [item._meta_data for item in self.iter_selected_items() if isinstance(item._meta_data, Entity)]

    @log_info
    def iter_values(self):
        for obj in pymel.ls(type='transform'):
            yield obj

    @log_info
    def get_qtreewidget_item(self, value):
        return factory_tree_widget_item.get(value)

    @log_info
    def update(self):
        """
        Remove all QTreeWidgetItem and rebuilt the tree.
        """
        self.ui.treeWidget.clear()
        for value in self.iter_values():
            item = self.get_qtreewidget_item(value)
            self.ui.treeWidget.addTopLevelItem(item)
            self.ui.treeWidget.expandItem(item)

        # self.update_list_visibility()

        self.refresh_ui()

    @log_info
    def refresh_ui(self):
        self._refresh_ui_modules_checked()
        self.refresh_items_visibility()

    @log_info
    def _refresh_ui_modules_checked(self):
        # Block the signal to make sure that the itemChanged event is not called when adjusting the check state
        self.ui.treeWidget.blockSignals(True)
        for qt_item in libQt.get_all_QTreeWidgetItem(self.ui.treeWidget):
            if hasattr(qt_item, "rig"):
                qt_item.setCheckState(0, QtCore.Qt.Checked if qt_item._meta_data.is_built else QtCore.Qt.Unchecked)
        self.ui.treeWidget.blockSignals(False)

    def can_show_item(self, item, query_regex):
        # type: (QtWidgets.QTreeWidgetItem, str) -> bool
        """
        :param item: A QTreeWidgetItem.
        :param query_regex: The text in the search QLineEdit.
        :return: True if the QTreeWidgetItem should be visible. False otherwise.
        """
        # # Always shows non-module
        # if not hasattr(item, 'rig'):
        #     return True
        # if not isinstance(item._meta_data, classModule.Module):
        #     return True
        #
        # module = item._meta_data  # Retrieve monkey-patched data
        # module_name = str(module)
        try:
            metadata = item._meta_data
        except AttributeError:
            log.warning("can_show_item: Unsupported metadata type {0}".format(item))
            return True

        return not query_regex or re.match(query_regex, str(metadata), re.IGNORECASE)

    @log_info
    def refresh_items_visibility(self, query_regex=None):
        if query_regex is None:
            query_raw = self.ui.lineEdit_search.text()
            query_regex = ".*{0}.*".format(query_raw) if query_raw else ".*"


        # unselectableBrush = QtGui.QBrush(QtCore.Qt.darkGray)
        # selectableBrush = QtGui.QBrush(QtCore.Qt.white)
        for qt_item in libQt.get_all_QTreeWidgetItem(self.ui.treeWidget):
            can_show = self.can_show_item(qt_item, query_regex)
            qt_item.setHidden(not can_show)

    @log_info
    def _refresh_ui_enabled(self, val):
        """
        Used for drag and drop operation, this will change the 'enabled' value for all QTreeWidgetItem that can accept the new value.
        :param val:
        :return:
        """
        for item in libQt.get_all_QTreeWidgetItem(self.ui.treeWidget):
            if item._meta_type == ui_shared.MimeTypes.Attribute:
                component_attr = item._meta_data
                if component_attr.validate(val):
                    flags = item.flags()
                    flags &= ~QtCore.Qt.ItemIsEnabled
                    item.setFlags(flags)

    @log_info
    def _reset_ui_enabled(self):
        for item in libQt.get_all_QTreeWidgetItem(self.ui.treeWidget):
            flags = item.flags()
            flags |= QtCore.Qt.ItemIsEnabled
            item.setFlags(flags)

    # Block signals need to be called in a function because if called in a signal, it will block it
    @log_info
    def _set_text_block(self, item, str):
        self.ui.treeWidget.blockSignals(True)
        if hasattr(item, "rig"):
            item.setText(0, str)
        self.ui.treeWidget.blockSignals(False)

    def iter_selection(self):
        result = []
        for item in self.ui.treeWidget.selectedItems():
            if item._meta_data.exists():
                result.append(item._meta_data)
        return result

    @log_info
    def on_selection_changed(self):
        # Filter deleted networks
        networks = [net for net in self.iter_selection() if net and net.exists()]
        print networks
        pymel.select(networks)

    @log_info
    def on_module_changed(self, item):
        if not self._listen_events:
            return

        # todo: handle exception
        # Check first if the checkbox have changed
        need_update = False
        new_state = item.checkState(0) == QtCore.Qt.Checked
        new_text = item.text(0)

        # debug
        if not hasattr(item, '_meta_data'):
            print '???', item.text(0)
            return

        module = item._meta_data
        if item._checked != new_state:
            item._checked = new_state
            # Handle checkbox change
            if new_state:
                self._build(module, update=False)  # note: setting update=True on maya-2017 can cause Qt to crash...
            else:
                self._unbuild(module, update=False)  # note: setting update=True on maya-2017 can cause Qt to crash...
            # need_update = True
            ui_shared._update_network(self._rig, item=item)

        # Check if the name have changed
        if (item._name != new_text):
            item._name = new_text
            module.name = new_text

            # Update directly the network value instead of re-exporting it
            if hasattr(item, "net"):
                name_attr = item.net.attr("name")
                name_attr.set(new_text)

                # Ensure to only refresh the UI and not recreate all
                # if need_update:
                #     self.refresh_ui()

    # @log_info
    def on_search_changed(self, *args, **kwargs):
        self.refresh_items_visibility()

    @log_info
    def on_context_menu_request(self):
        selected_items = self.ui.treeWidget.selectedItems()
        selected_components = [item._meta_data for item in selected_items if isinstance(item._meta_data, Entity)]
        if selected_components:
            factory_rc_menu.get_menu(selected_components, self.actionRequested.emit)

    @log_info
    def on_module_double_clicked(self, item):
        if hasattr(item, "rig"):
            self._set_text_block(item, item._meta_data.name)
            self._is_modifying = True  # Flag to know that we are currently modifying the name
            self.ui.treeWidget.editItem(item, 0)

    @log_info
    def on_tree_focus(self, event):
        # Set back the text with the information about the module in it
        if self._is_modifying:
            sel = self.ui.treeWidget.selectedItems()
            if sel:
                self._listen_events = False
                selected_item = sel[0]
                if isinstance(selected_item._meta_data, classModule.Module):
                    selected_item._update()
                self._listen_events = True
            self._is_modifying = False
        self.focusInEvent(event)

    @log_info
    def on_lock_selected(self):
        need_update = False
        for item in self.ui.treeWidget.selectedItems():
            val = item._meta_data
            if isinstance(val, classModule.Module) and not val.locked:
                need_update = True
                val.locked = True
        if need_update:
            ui_shared._update_network(self._rig)
            self.update()

    @log_info
    def on_unlock_selected(self):
        need_update = False
        for item in self.ui.treeWidget.selectedItems():
            val = item._meta_data
            if isinstance(val, classModule.Module) and val.locked:
                need_update = True
                val.locked = False
        if need_update:
            ui_shared._update_network(self._rig)
            self.update()


class OmtkBaseListWidgetRig(OmtkBaseListWidget):
    """
    Define a custom QTreeWidget that is related to an omtk.Rig instance.
    """
    def __init__(self, parent=None):
        super(OmtkBaseListWidgetRig, self).__init__(parent=parent)

        self._rig = None

    def set_rig(self, rig, update=True):
        self._rig = rig
        if update:
            self.update()