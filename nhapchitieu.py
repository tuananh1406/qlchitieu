import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from datetime import date as ngaythang


class nhapchitieu(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title='Nhập chi tiêu')
        
        self.ngayhientai = ngaythang.today().strftime('%d/%m/%Y')
        #Khởi tạo lưới tọa độ
        grid = Gtk.Grid()
        #Thiết lập tự động co giãn cho hàng và cột
        grid.set_column_homogeneous('TRUE')
        grid.set_row_homogeneous('TRUE')
        self.add(grid)
        
        #Khởi tạo các thành phần trong cửa sổ
        self.lb_tenchitieu = Gtk.Label('Tên chi tiêu:')
        self.et_tenchitieu = Gtk.Entry()
        self.lb_sotien = Gtk.Label('Số tiền:')
        self.et_sotien = Gtk.Entry()
        self.et_sotien.set_placeholder_text('Nhập số tiền (*1000)')
        self.lb_ngaychi = Gtk.Label('Ngày tháng')
        self.et_ngaychi = Gtk.Entry()
        self.et_ngaychi.set_text(self.ngayhientai)
        #self.bt_ngaychi = Gtk.Button('Chọn ngày')
        self.bt_capnhat = Gtk.Button('Thêm chi tiêu')
        
        #Kết nối các sự kiện
        #self.bt_ngaychi.connect('clicked', self.hienthilich)
        self.bt_capnhat.connect('clicked', self.capnhatchitieu)
        self.et_ngaychi.connect('activate', self.capnhatchitieu)
        self.et_sotien.connect('activate', self.capnhatchitieu)
        
        #Sắp xếp các thành phần
        grid.add(self.lb_tenchitieu)
        grid.attach(self.et_tenchitieu, 1, 0, 2, 1)
        grid.attach(self.lb_sotien, 0, 1, 1, 1)
        grid.attach(self.et_sotien, 1, 1, 2, 1)
        grid.attach(self.lb_ngaychi, 0, 2, 1, 1)
        grid.attach(self.et_ngaychi, 1, 2, 2, 1)
        #grid.attach(self.bt_ngaychi, 3, 2, 1, 1)
        grid.attach(self.bt_capnhat, 1, 3, 1, 1)
        
    def hienthilich(self, sukien=None): #Hiển thị lịch để chọn, chưa dùng được
        lich = Gtk.Calendar()
        lich.day = 1
        lich.month = 1
        lich.year = 2018
        lich.mark_day(1)
        #lich.run()
        #lich.destroy()
           
    def kiemtra(self):
        try:
            tenchitieu = self.et_tenchitieu.get_text()
            sotien = self.et_sotien.get_text()
            if tenchitieu != '' and sotien != '':
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
            sotien = int(self.et_sotien.get_text())
            self.thongbao(
                "{0}-{1}".format(
                    self.et_tenchitieu.get_text(),
                    sotien * 1000,
                )
            )
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
