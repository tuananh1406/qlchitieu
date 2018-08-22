import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from datetime import date as ngaythang


class nhapchitieu(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title='Nhập chi tiêu')
        self.move(700, 300)
        self.ngayhientai = ngaythang.today().strftime('%d/%m/%Y')
        #Khởi tạo lưới tọa độ
        grid = Gtk.Grid()
        #Thiết lập tự động co giãn cho hàng và cột
        grid.set_column_homogeneous('TRUE')
        grid.set_row_homogeneous('TRUE')
        self.add(grid)
        #Khởi tạo các thành phần trong cửa sổ
        self.lb_hangmuc = Gtk.Label('Chọn hạng mục')
        dshangmuc = self.laydshangmuc()
        self.cbb_hangmuc = Gtk.ComboBox.new_with_model(dshangmuc)
        self.cbb_hangmuc.set_active(0)
        rendertext = Gtk.CellRendererText()
        self.cbb_hangmuc.pack_start(rendertext, True)
        self.cbb_hangmuc.add_attribute(rendertext, "text", 0)
        self.lb_tenchitieu = Gtk.Label('Tên chi tiêu:')
        dschitieu = self.laydschitieu()
        self.cbb_tenchitieu = Gtk.ComboBox.new_with_model_and_entry(dschitieu)
        self.cbb_tenchitieu.set_entry_text_column(0)
        self.cbb_tenchitieu.set_active(0)
        self.lb_sotien = Gtk.Label('Số tiền:')
        self.et_sotien = Gtk.Entry()
        self.et_sotien.set_placeholder_text('Nhập số tiền (*1000)')
        self.lb_ngaychi = Gtk.Label('Ngày tháng')
        self.et_ngaychi = Gtk.Entry()
        self.et_ngaychi.set_text(self.ngayhientai)
        self.bt_capnhat = Gtk.Button('Thêm chi tiêu')
        #Kết nối các sự kiện
        self.bt_capnhat.connect('clicked', self.capnhatchitieu)
        self.et_ngaychi.connect('activate', self.capnhatchitieu)
        self.et_sotien.connect('activate', self.capnhatchitieu)
        #Sắp xếp các thành phần
        grid.add(self.lb_hangmuc)
        grid.attach(self.cbb_hangmuc, 1, 0, 2, 1)
        grid.attach(self.lb_tenchitieu, 0, 1, 1, 1)
        grid.attach(self.cbb_tenchitieu, 1, 1, 2, 1)
        grid.attach(self.lb_sotien, 0, 2, 1, 1)
        grid.attach(self.et_sotien, 1, 2, 2, 1)
        grid.attach(self.lb_ngaychi, 0, 3, 1, 1)
        grid.attach(self.et_ngaychi, 1, 3, 2, 1)
        grid.attach(self.bt_capnhat, 1, 4, 1, 1)

    def laydshangmuc(self):
        ds = ['123', '1213214']
        dshangmuc = Gtk.ListStore(str)
        for i in ds:
            dshangmuc.append([i])
        return dshangmuc

    def laydschitieu(self):
        ds = ['dfsafas', 'sdafasdg', 'gsdafsad']
        dschitieu = Gtk.ListStore(str)
        for i in ds:
            dschitieu.append([i])
        return dschitieu

    def kiemtra(self):
        try:
            iter_hangmuc = self.cbb_hangmuc.get_active_iter()
            model_hangmuc = self.cbb_hangmuc.get_model()
            self.hangmuc = model_hangmuc[iter_hangmuc][0]
            iter_chitieu = self.cbb_tenchitieu.get_active_iter()
            model_chitieu = self.cbb_tenchitieu.get_model()
            self.tenchitieu = model_chitieu[iter_chitieu][0]
            sotien = self.et_sotien.get_text()
            if self.hangmuc != '' and self.tenchitieu != '' and sotien != '':
                try:
                    sotienint = int(sotien)
                    if sotienint > 0:
                        return True
                    else:
                        return False
                except:
                    return False
            else:
                return False
        except:
            return False

    def capnhatchitieu(self, sukien=None):
        if self.kiemtra():
            sotien = int(self.et_sotien.get_text()) * 1000
            self.et_sotien.set_text('{:2,d}'.format(sotien))
            self.thongbao(
                "Bạn đã thêm chi tiêu {0}\n Với số tiền: {1:2,d} nghìn đồng"
                .format(self.tenchitieu, sotien))
            print(self.get_position())
        else:
            self.thongbao('Kiểm tra lại các thông tin')

    def thongbao(self, text=None):
        hopthoai = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK, text)
        hopthoai.run()
        hopthoai.destroy()

if __name__ == '__main__':
    win = nhapchitieu()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
