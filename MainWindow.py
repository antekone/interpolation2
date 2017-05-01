import gi
import cairo
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from Interpolation import Interpolation

class Graph(Gtk.DrawingArea):
    def __init__(self, inter):
        Gtk.DrawingArea.__init__(self)
        self.inter = inter

        self.set_size_request(800, 300)
        self.connect("draw", self.on_draw)
        self.connect("button-press-event", self.on_button_press)
        self.connect("configure-event", self.on_configure)
        self.connect("motion-notify-event", self.on_motion_notify)

        self.add_events(Gdk.EventMask.POINTER_MOTION_MASK |
                        Gdk.EventMask.BUTTON_PRESS_MASK |
                        Gdk.EventMask.BUTTON_RELEASE_MASK)
        self.file_loaded = self.inter.size() > 0
        self.selected_x = None

        print("inter size: {}".format(self.inter.size()))

    def on_configure(self, widget, data):
        self.width = self.get_allocated_width()
        self.graph = self.width * [0]
        widget.queue_draw()

    def draw_all(self):
        for x in range(0, self.get_allocated_width()):
            range_start, range_end = self.get_file_range_based_on_x(x)

            range_size = range_end - range_start
            v = self.inter.value_for_range(range_start, range_size)
            self.graph[x] = v

        self.queue_draw()

    def on_button_press(self, widget, event):
        range_start, range_end = self.get_file_range_based_on_x(int(event.x))
        range_size = range_end - range_start

        v = self.inter.value_for_range(range_start, range_size)
        self.graph[int(event.x)] = v

        widget.queue_draw()

    def get_file_range_based_on_x(self, x):
        self.width = self.get_allocated_width()
        self.height = self.get_allocated_height()

        max_size = self.inter.size()

        range_start = int(max_size * x / self.width)
        range_end = int(max_size * (x + 1) / self.width) - 1

        return (range_start, range_end)

    def on_motion_notify(self, widget, event):
        if self.file_loaded == False:
            return

        self.selected_x = int(event.x)
        widget.queue_draw()

    def on_draw(self, widget, c):
        self.width = self.get_allocated_width()
        self.height = self.get_allocated_height()

        c.set_source_rgb(0, 0, 0)
        c.rectangle(0, 0, 1 + self.width, 1 + self.height)
        c.fill()

        if self.file_loaded == True:
            self.on_draw_loaded(widget, c)
        else:
            self.on_draw_empty(widget, c)

    def draw_graph(self, c):
        max_value = max(self.graph)
        if max_value == 0:
            return

        c.set_source_rgb(140, 140, 140)
        c.set_line_width(1.0)

        for x in range(0, len(self.graph)):
            value = self.graph[x]
            pixel_width = int(self.height * value / max_value)

            c.move_to(x, self.height)
            c.line_to(x, self.height - pixel_width)

        c.stroke()

    def on_draw_loaded(self, widget, c):
        self.draw_graph(c)
        if self.selected_x is not None:
            c.set_source_rgb(70, 70, 70)
            c.set_line_width(1.0)
            c.move_to(self.selected_x, 0)
            c.line_to(self.selected_x, self.height)
            c.stroke()

    def on_draw_empty(self, widget, c):
        pass


class MainWindow(Gtk.Window):
    def __init__(self, inter):
        Gtk.Window.__init__(self, title = "File view")

        self.set_border_width(10)

        self.vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 6)
        self.add(self.vbox)

        self.draw_button = Gtk.Button(label = "Draw")
        self.draw_button.connect("clicked", self.on_draw_clicked)
        self.quit_button = Gtk.Button(label = "Quit")
        self.quit_button.connect("clicked", Gtk.main_quit)

        self.drawing_area = Graph(inter)

        self.button_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 6)
        self.button_box.pack_start(self.draw_button, True, True, 0)
        self.button_box.pack_start(self.quit_button, True, True, 0)

        self.vbox.pack_start(self.drawing_area, True, True, 0)
        self.vbox.pack_start(self.button_box, False, True, 0)

    def on_draw_clicked(self, widget):
        self.drawing_area.draw_all()


def main():
    inter = Interpolation("/home/antek/.local/share/Steam/steamapps/common/Rust/Bundles/shared/content.bundle")
    win = MainWindow(inter)
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()

main()
