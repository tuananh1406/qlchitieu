import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class nhapchitieu(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Nhập danh mục")

        #Khởi tạo lưới
        grid = Gtk.Grid()
        #Thiết lập tự động co giãn cho hàng và cột
        grid.set_column_homogeneous('TRUE')
        grid.set_row_homogeneous('TRUE')
        self.add(grid)

        #Khởi tạo các thành phần
        self.lb_tendanhmuc = Gtk.Label('Tên danh mục:')
        self.et_tendanhmuc = Gtk.Entry()
        self.lb_madanhmuc = Gtk.Label('Mã danh mục:')
        self.et_madanhmuc = Gtk.Entry()
        self.bt_capnhat = Gtk.Button('Cập nhật')
        self.bt_capnhat.connect("clicked", self.capnhat)
        self.et_madanhmuc.connect('activate', self.capnhat)

        #Sắp xếp các thành phần
        grid.add(self.lb_tendanhmuc)
        grid.attach(self.et_tendanhmuc, 1, 0, 2, 1)
        grid.attach(self.lb_madanhmuc, 0, 1, 1, 1)
        grid.attach(self.et_madanhmuc, 1, 1, 2, 1)
        grid.attach(self.bt_capnhat, 1, 2, 1, 1)

    def capnhat(self, sukien):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK,
            self.et_tendanhmuc.get_text())
        dialog.format_secondary_text(self.et_madanhmuc.get_text())
        dialog.run()
        dialog.destroy()

if __name__ == '__main__':
    win = nhapchitieu()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
