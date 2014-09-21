# Copyright 2014 Gonzalo Odird, SugarLabs
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import os
import logging

from gi.repository import Gtk
from gi.repository import Gdk

from gettext import gettext as _

from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityToolbarButton
from sugar3.activity.widgets import StopButton
from sugar3.graphics import style


class ComunicatorMakerActivity(activity.Activity):

    def __init__(self, handle):
        """Set up the HelloWorld activity."""
        activity.Activity.__init__(self, handle)

        # Change the following number to change max participants
        self.max_participants = 1

        toolbar_box = ToolbarBox()

        activity_button = ActivityToolbarButton(self)
        toolbar_box.toolbar.insert(activity_button, 0)
        activity_button.show()

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()

        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()

        background = Gtk.EventBox()
        background.modify_bg(Gtk.StateType.NORMAL,
                             style.Color('#FFFFFF').get_gdk_color())
        self.set_canvas(background)

        # canvas
        hbox = Gtk.HBox()
        background.add(hbox)

        # treeview with pictograms
        self._create_picto_treeview()
        scrolled = Gtk.ScrolledWindow()
        scrolled.props.hscrollbar_policy = Gtk.PolicyType.AUTOMATIC
        scrolled.props.vscrollbar_policy = Gtk.PolicyType.AUTOMATIC
        scrolled.set_size_request(Gdk.Screen.width() / 4, -1)
        scrolled.add_with_viewport(self._picto_tree_view)
        hbox.pack_start(scrolled, False, False, 0)

        self._board_edit_panel = BoardEditPanel()
        hbox.pack_start(self._board_edit_panel, True, True, 0)

        self._load_pictograms()

        self.show_all()

    def _create_picto_treeview(self):
        self._picto_tree_view = Gtk.TreeView()
        self._picto_tree_view.props.headers_visible = False

        cell = Gtk.CellRendererText()
        self._column = Gtk.TreeViewColumn()
        self._column.pack_start(cell, True)
        self._column.add_attribute(cell, 'text', 0)
        self._picto_tree_view.append_column(self._column)
        self._picto_tree_view.set_search_column(0)

    def _load_pictograms(self):
        self._picto_tree_view.set_model(Gtk.TreeStore(str, str))
        self._picto_model = self._picto_tree_view.get_model()
        self._add_dir_to_model('./pictograms', self._filter_function)

    def _add_dir_to_model(self, dir_path, filter_function, parent=None):
        logging.error('dir %s', dir_path)
        for f in os.listdir(dir_path):
            full_path = os.path.join(dir_path, f)
            if os.path.isdir(full_path):
                new_iter = self._picto_model.append(parent, [f, full_path])
                self._add_dir_to_model(full_path, filter_function, new_iter)
            else:
                if filter_function(full_path):
                    self._picto_model.append(parent, [f, full_path])

    def _filter_function(self, path):
        return True


class BoardEditPanel(Gtk.EventBox):

    def __init__(self):
        Gtk.EventBox.__init__(self)
        vbox = Gtk.VBox()
        self.add(vbox)
        title_label = Gtk.Label(_('Board name'))
        title_label.set_valign(Gtk.Align.START)
        title_label.set_halign(Gtk.Align.START)
        title_label.props.margin = 10
        vbox.add(title_label)
        # size = Gdk.Screen.width() / 6
        grid = Gtk.Grid()
        vbox.add(grid)
        for row in range(2):
            for column in range(3):
                picto_editor = PictoEditPanel()
                grid.attach(picto_editor, column, row, 1, 1)


class PictoEditPanel(Gtk.EventBox):

    def __init__(self):
        Gtk.EventBox.__init__(self)
        vbox = Gtk.VBox()
        self.add(vbox)
        self.image = Gtk.Image()
        vbox.add(self.image)
        self.entry = Gtk.Entry()
        vbox.add(self.entry)
