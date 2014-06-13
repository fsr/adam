# !/usr/bin/python3
from gi.repository import Gtk, Gio, Gdk

import create_coding


class GenerateCodingWindow(Gtk.Window):
    courses = []

    def __init__(self):
        Gtk.Window.__init__(self, title="Coding generation")
        self.set_default_size(800, 600)

        # HeaderBar

        self.hb = Gtk.HeaderBar()
        self.hb.set_show_close_button(True)
        self.hb.set_title("Coding generation")
        self.hb.set_subtitle("Import plain text descriptions on the left")
        self.set_titlebar(self.hb)

        self.maximize_button = Gtk.ToggleButton()
        self.maximize_button.set_image(
            Gtk.Image.new_from_gicon(Gio.ThemedIcon(name="view-fullscreen"), Gtk.IconSize.BUTTON))
        self.maximize_button.connect("toggled", self.toggle_window_state)
        self.hb.pack_end(self.maximize_button)

        self.connect("window-state-event", self.window_state_changed)

        self.choose_file_button = Gtk.Button()
        icon = Gio.ThemedIcon(name="document-open")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        self.choose_file_button.add(image)
        self.choose_file_button.connect("clicked", self.choose_file_click)
        self.hb.pack_start(self.choose_file_button)

        self.save_json_button = Gtk.Button()
        icon = Gio.ThemedIcon(name="document-save")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        self.save_json_button.add(image)
        self.save_json_button.connect("clicked", self.save_json_click)
        self.hb.pack_start(self.save_json_button)

        # Lower Grid

        self.paned = Gtk.Paned()
        self.add(self.paned)

        self.file_list_store = Gtk.ListStore(str)
        self.file_list = Gtk.TreeView(self.file_list_store)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Interpreted files", renderer, text=0)
        self.file_list.append_column(column)
        self.file_list.set_hexpand(True)
        self.file_list.set_vexpand(True)
        self.file_list.set_size_request(200, -1)
        self.paned.pack1(self.file_list)

        self.scrolledwindow = Gtk.ScrolledWindow()
        self.scrolledwindow.set_hexpand(True)
        self.scrolledwindow.set_vexpand(True)
        self.json_text = Gtk.Label()
        self.json_text.set_hexpand(True)
        self.json_text.set_vexpand(True)
        self.json_text.set_justify(Gtk.Justification.LEFT)
        self.scrolledwindow.add(self.json_text)
        self.paned.pack2(self.scrolledwindow)

    def toggle_window_state(self, button):
        if button.get_active():
            icon = Gio.ThemedIcon(name="view-restore")
            self.maximize()
        else:
            icon = Gio.ThemedIcon(name="view-fullscreen")
            self.unmaximize()
        button.set_image(Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON))

    def window_state_changed(self, window, event):
        if event.changed_mask == Gdk.WindowState.MAXIMIZED:
            if event.new_window_state & Gdk.WindowState.MAXIMIZED:
                self.maximize_button.set_active(True)
            else:
                self.maximize_button.set_active(False)
        return False

    def refresh_json_output(self, filename):
        self.courses.extend(create_coding.parse_course_data_from_file(filename))
        self.json_text.set_text(create_coding.prettyprint_json(self.courses))

    def choose_file_click(self, widget):
        dialog = Gtk.FileChooserDialog("Choose course file", self,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.file_list_store.append([dialog.get_filename()[::-1].split("/", 1)[0][::-1]])
            self.refresh_json_output(dialog.get_filename())

        dialog.destroy()

    def save_json_click(self, widget):
        dialog = Gtk.FileChooserDialog("Choose course file", self,
                                       Gtk.FileChooserAction.SAVE,
                                       (Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            with open(dialog.get_filename(), 'w') as f:
                f.write(self.json_text.get_text())

        dialog.destroy()


def show_coding_window():
    win = GenerateCodingWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()


show_coding_window()
