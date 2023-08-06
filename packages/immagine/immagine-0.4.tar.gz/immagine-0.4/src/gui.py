#!/usr/bin/env python

# Copyright 2016, 2017 Matteo Franchin
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''Simple image viewer.'''

import os
import sys

import pygtk
pygtk.require('2.0')
import gtk
import gobject

from .browser_tab import BrowserTab
from .viewer_tab import ViewerTab
from .toolbar_window import ToolbarWindow
from . import file_utils
from .file_utils import FileList
from .config import get_config

def create_action_tuple(name=None, stock_id=None, label=None, accel=None,
                        tooltip=None, fn=None):
    if accel is None and tooltip is None and fn is None:
        return (name, stock_id, label)
    return (name, stock_id, label, accel, tooltip, fn)

def create_toggle_tuple(name=None, stock_id=None, label=None, accel=None,
                        tooltip=None, fn=None, value=None):
    return (name, stock_id, label, accel, tooltip, fn, value)

def create_radio_tuple(name=None, stock_id=None, label=None, accel=None,
                       tooltip=None, value=0):
    assert name is not None, 'name must be given in radio action tuple'
    return (name, stock_id, label, accel, tooltip, value)


class ApplicationMainWindow(gtk.Window):
    application_name = 'Immagine image viewer'

    def __init__(self, start_path, parent=None):
        super(ApplicationMainWindow, self).__init__()
        self.fullscreen_widget = None
        self.fullscreen_toolbar = ToolbarWindow()
        self.open_dialog = None
        self.config = get_config()
        self.sort_type = FileList.SORT_BY_MOD_DATE

        # Set screen size.
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())
        width, height = self._get_window_size()
        self.set_default_size(width, height)

        # Populate the window.
        self.set_title(self.application_name)
        self.ui_manager = ui_manager = gtk.UIManager()
        self.set_data('ui-manager', ui_manager)
        ui_info, action_group = self._create_action_group()
        ui_manager.insert_action_group(action_group, 0)
        self.add_accel_group(ui_manager.get_accel_group())
        ui_manager.add_ui_from_string(ui_info)

        # A callable which can be used to retrieve global GUI configuration.
        self.config_retriever = self._generate_config_retriever()

        # The menu is shared across all tabs.
        bar = ui_manager.get_widget('/MenuBar')
        bar.show()

        # Below the menu, we place the notebook.
        self.notebook = nb = gtk.Notebook()
        nb.set_scrollable(True)
        nb.set_tab_pos(gtk.POS_TOP)

        # When given a directory open a browsing tab. When given a file open
        # the parent directory and the file in two separate tabs.
        start_file = None
        if start_path is None:
            start_dir = os.getcwd()
        elif os.path.isdir(start_path):
            start_dir = start_path
        else:
            start_dir = os.path.dirname(start_path) or os.getcwd()
            if not os.path.isdir(start_dir):
                start_dir = os.getcwd()
            elif os.path.exists(start_path):
                start_file = os.path.split(start_path)[1]
        self.browser_tab = self.open_tab(start_dir)
        if start_file is not None:
            self.open_tab(start_file)

        # Place menu and notebook in a VBox. Add this to the window.
        self.window_content = vbox = gtk.VBox()
        vbox.pack_start(bar, expand=False)
        vbox.pack_start(nb)
        self.add(self.window_content)

        # Allow the window to get events.
        mask = gtk.gdk.KEY_PRESS_MASK | gtk.gdk.POINTER_MOTION_MASK
        self.add_events(mask)
        self.connect('key-press-event', self.on_key_press_event)
        self.connect("motion_notify_event", self.on_motion_notify_event)

        self.show_all()

    def _get_screen_size(self):
        screen = self.get_screen()
        num_monitors = screen.get_n_monitors()
        geoms = [screen.get_monitor_geometry(i) for i in range(num_monitors)]
        return (min(g.width for g in geoms), min(g.height for g in geoms))

    def _get_window_size(self, min_size=(200, 200)):
        screen_size = self._get_screen_size()
        rel_size = (0.5, 0.8)
        ret = []
        for i, coord in enumerate(('width', 'height')):
            abs_val = self.config.get('window', coord, of=int, default=None)
            if abs_val is None:
                rel_val = self.config.get('window', 'rel_' + coord, of=int,
                                          default=rel_size[i])
                abs_val = int(screen_size[i] * min(1.0, max(0.0, rel_val)))
            ret.append(max(min_size[i], min(screen_size[i], abs_val)))
        return tuple(ret)

    def _get_thumb_size(self):
        screen_size = self._get_screen_size()
        rel_size = (0.6 / 4, 0.6 / 3)
        ret = []
        for i, coord in enumerate(('width', 'height')):
            abs_val = self.config.get('thumb', 'max_' + coord, of=int,
                                      default=None)
            if abs_val is None:
                rel_val = self.config.get('thumb', 'rel_' + coord, of=float,
                                          default=rel_size[i])
                abs_val = int(screen_size[i] * min(1.0, max(0.0, rel_val)))
            ret.append(max(5, abs_val))
        return tuple(ret)

    def _generate_config_retriever(self):
        '''Generate a callable which can be used to retrieve configuration.

        This callable receives two arguments (name, default_value) similarly to
        the get method of a dict object.
        '''
        uim = self.ui_manager
        show_hidden_toggle = uim.get_widget('/MenuBar/ViewMenu/ShowHidden')
        reversed_toggle = uim.get_widget('/MenuBar/ViewMenu/ReverseSortOrder')
        config_dict = \
           {'show_hidden_files': (lambda: show_hidden_toggle.get_active()),
            'reversed_sort': (lambda: reversed_toggle.get_active()),
            'sort_type': (lambda: self.sort_type),
            'thumb_size': (lambda: self._get_thumb_size())}
        def retriever(name, default=None):
            fn = config_dict.get(name, None)
            if fn is not None:
                return fn()
            return default
        return retriever

    def change_layout(self):
        '''Switch in/out of fullscreen layout.'''
        nb = self.notebook
        if not self.get_fullscreen_mode():
            # Go to fullscreen mode.
            # Remove the widget (to be fullscreen-ed) from its parent tab.
            n = nb.get_current_page()
            tab = nb.get_nth_page(n)
            toolbar, tab_content = tab.get_children()
            tab.remove(toolbar)
            tab.remove(tab_content)

            # Remember the parent widget so that we can restore the tab when
            # going out of fullscreen mode.
            self.fullscreen_widget = tab
            self.fullscreen_toolbar.begin(toolbar)

            # Remove the main window widget and replace it with the tab widget.
            self.remove(self.window_content)
            self.add(tab_content)
        else:
            # Quit fullscreen mode.
            # Remove the tab widget from the window and replace it with the
            # default widget.
            tab_content = self.get_children()[0]
            self.remove(tab_content)
            self.add(self.window_content)

            # Put back the tab widget to its original parent.
            toolbar = self.fullscreen_toolbar.end()
            self.fullscreen_widget.pack_start(toolbar, expand=False)
            self.fullscreen_widget.pack_start(tab_content)
            self.fullscreen_widget = None

        fs = self.get_fullscreen_mode()
        for page in range(nb.get_n_pages()):
            tab = nb.get_nth_page(page)
            tab.set_fullscreen(fs)

    def on_motion_notify_event(self, widget, event):
        if self.get_fullscreen_mode():
            self.fullscreen_toolbar.show_if_mouse_nearby()

    def get_current_tab(self):
        '''Return the active tab. This is either a BrowserTab or a ViewerTab.
        '''
        if self.fullscreen_widget is not None:
            return self.fullscreen_widget
        n = self.notebook.get_current_page()
        return self.notebook.get_nth_page(n)

    def _create_action_group(self):
        ui_info = \
          '''<ui>
            <menubar name='MenuBar'>
              <menu action='FileMenu'>
                <menuitem action='Open'/>
                <separator/>
                <menuitem action='Quit'/>
              </menu>
              <menu action='ViewMenu'>
                <menuitem action='CloseTab'/>
                <menuitem action='Fullscreen'/>
                <menuitem action='ShowHidden'/>
                <menu action='SortFilesBy'>
                  <menuitem action='SortFilesByName'/>
                  <menuitem action='SortFilesByModDate'/>
                  <menuitem action='SortFilesByExt'/>
                  <menuitem action='SortFilesBySize'/>
                </menu>
                <menuitem action='ReverseSortOrder'/>
              </menu>
              <menu action='HelpMenu'>
                <menuitem action='About'/>
              </menu>
            </menubar>
          </ui>'''

        action = create_action_tuple
        action_entries = \
          (action(name='FileMenu', label='_File'),
           action(name='ViewMenu', label='_View'),
           action(name='SortFilesBy', label='_Sort files by'),
           action(name='HelpMenu', label='_Help'),
           action(name='Quit', stock_id=gtk.STOCK_QUIT, label='Quit',
                  accel='<control>Q', tooltip='Quit',
                  fn=self.quit_action),
           action(name='Open', stock_id=gtk.STOCK_OPEN,
                  label='_Open directory', accel='<control>O',
                  tooltip='Open a directory', fn=self.on_open_location),
           action(name='CloseTab', label='_Close current tab',
                  accel='<control>W', tooltip='Toggle fullscreen mode',
                  fn=self.close_tab_action),
           action(name='Fullscreen', label='_Fullscreen', accel='F11',
                  tooltip='Toggle fullscreen mode',
                  fn=self.fullscreen_action),
           action(name='About', label='_About', accel='<control>A',
                  tooltip='About', fn=self.about_action))

        toggle = create_toggle_tuple
        toggle_entries = \
          (toggle(name='ShowHidden', label='_Show hidden files',
                  accel='<control>H', tooltip='Show hidden files',
                  fn=self.update_album_handler, value=False),
           toggle(name='ReverseSortOrder', label='_Reverse sort order',
                  accel='<control>R', tooltip='Reverse the sort order',
                  fn=self.update_album_handler, value=False))

        radio = create_radio_tuple
        radio_entries = \
          (radio(name='SortFilesByName', label='Name',
                 accel='<control>N', tooltip='Sort by file name',
                 value=FileList.SORT_BY_FILE_NAME),
           radio(name='SortFilesByModDate', label='Modification date',
                 accel='<control>D',
                 tooltip='Sort first by modification date, then name',
                 value=FileList.SORT_BY_MOD_DATE),
           radio(name='SortFilesByExt', label='Extension',
                 accel='<control>E',
                 tooltip='Sort first by file extension, then name',
                 value=FileList.SORT_BY_FILE_EXT),
           radio(name='SortFilesBySize', label='Size',
                 accel='<control>S',
                 tooltip='Sort first by file size, then name',
                 value=FileList.SORT_BY_FILE_SIZE))

        action_group = gtk.ActionGroup('AppWindowActions')
        action_group.add_actions(action_entries)
        action_group.add_toggle_actions(toggle_entries)
        action_group.add_radio_actions(radio_entries,
                                       on_change=self.on_radio_change,
                                       value=self.sort_type)
        return (ui_info, action_group)

    def quit_action(self, action):
        gtk.main_quit()

    def open_tab(self, path):
        '''Create a new tab for the given file/directory path.'''
        if os.path.isdir(path):
            return self.open_browser_tab(path)
        else:
            return self.open_viewer_tab(path)

    def open_browser_tab(self, path):
        '''Create a new BrowserTab to browser the given directory path.'''
        if not os.path.isdir(path):
            return None

        bt = BrowserTab(path, config_retriever=self.config_retriever)
        bt.set_callback('toggle_fullscreen', self.fullscreen_action)
        bt.set_callback('directory_changed', self.on_directory_changed)
        bt.set_callback('image_clicked', self.on_image_clicked)
        bt.set_callback('open_location', self.on_open_location)
        bt.image_browser.grab_focus()
        bt.show_all()

        self.notebook.append_page(bt, tab_label=bt.label)
        self.notebook.set_tab_reorderable(bt, True)
        self.notebook.set_current_page(-1)
        return bt

    def open_viewer_tab(self, path, **kwargs):
        '''Create a new ViewerTab to view the image at the given path.'''
        vt = ViewerTab(path, **kwargs)
        vt.set_callback('close_tab', self.on_close_tab)
        vt.set_callback('toggle_fullscreen', self.fullscreen_action)
        vt.show_all()

        self.notebook.append_page(vt, tab_label=vt.tab_top)
        self.notebook.set_tab_reorderable(vt, True)
        self.notebook.set_current_page(-1)
        self.on_tab_changed()

    def on_tab_changed(self):
        '''Called when the current tab changes.'''
        if self.get_fullscreen_mode():
            self.change_layout()
            self.change_layout()

    def about_action(self, action):
        dialog = gtk.AboutDialog()
        dialog.set_name('Immagine Image Viewer')
        dialog.set_copyright('\302\251 Copyright 2016, 2017 Matteo Franchin')
        dialog.set_website('https://github.com/mfnch/immagine')
        dialog.connect('response', lambda d, r: d.destroy())
        dialog.show()

    def close_tab_action(self, action):
        n = self.notebook.get_current_page()
        self.on_close_tab(self.notebook.get_nth_page(n))

    def get_fullscreen_mode(self):
        return (self.fullscreen_widget is not None)

    def fullscreen_action(self, action):
        self.change_layout()
        if self.get_fullscreen_mode():
            self.fullscreen()
        else:
            self.unfullscreen()

    def on_key_press_event(self, main_window, event):
        tab = self.get_current_tab()
        return tab.on_key_press_event(event)

    def on_directory_changed(self, new_directory):
        self.set_title(new_directory + ' - ' + self.application_name)

    def on_image_clicked(self, file_list, file_item):
        if not file_item.is_dir:
            self.open_viewer_tab(file_item.full_path,
                                 file_list=file_list,
                                 file_index=file_item.index)

    def on_close_tab(self, viewer):
        if isinstance(viewer, ViewerTab):
            n = self.notebook.page_num(viewer)
            self.notebook.remove_page(n)
            self.on_tab_changed()

    def on_open_location(self, *action):
        if self.open_dialog is None:
            buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                       gtk.STOCK_OPEN, gtk.RESPONSE_OK)
            self.open_dialog = fc = gtk.FileChooserDialog(
                title='Choose directory',
                parent=None,
                action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                buttons=buttons, backend=None)
            fc.set_default_response(gtk.RESPONSE_OK)

            f = gtk.FileFilter()
            f.set_name('All files')
            f.add_pattern("*")
            fc.add_filter(f)

            f = gtk.FileFilter()
            f.set_name("Images")
            f.add_mime_type("image/png")
            f.add_mime_type("image/jpeg")
            f.add_mime_type("image/gif")
            for ext in file_utils.image_file_extensions:
                f.add_pattern('*' + ext)
            fc.add_filter(f)

        fc = self.open_dialog
        response = fc.run()
        choice = (fc.get_filename() if response == gtk.RESPONSE_OK else None)
        fc.hide()

        if choice is not None:
            self.browser_tab.go_to_directory(choice)

    def update_album_handler(self, *args):
        self.browser_tab.update_album()

    def on_radio_change(self, first_radio, active_radio):
        new_sort_type = active_radio.get_current_value()
        if new_sort_type != self.sort_type:
            self.sort_type = new_sort_type
            self.browser_tab.update_album()

def main(args=None):
    args = args or sys.argv
    start_path = (args[1] if len(args) >= 2 else None)
    gtk.gdk.threads_init()
    gtk.gdk.threads_enter()
    ApplicationMainWindow(start_path)
    gtk.main()
    gtk.gdk.threads_leave()
