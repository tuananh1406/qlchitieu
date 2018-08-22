import sys
import os
import psycopg2
from datetime import date as ngaythang
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class nhapchitieu(Gtk.Window):

    def __init__(self):
        super(nhapchitieu, self).__init__(title='Nhập chi tiêu')
        self.move(700, 300)
        self.ngayhientai = ngaythang.today().strftime('%d/%m/%Y')
        #Khởi tạo lưới tọa độ và thiết lập co giãn theo cửa sổ
        grid = Gtk.Grid()
        grid.set_column_homogeneous('TRUE')
        grid.set_row_homogeneous('TRUE')
        self.add(grid)
        #Khai báo các tiện ích
        self.lb_sohangmuc = Gtk.Label('Số hạng mục')
        tuychinh = Gtk.Adjustment(0, 1, 4, 1, 10, 0)
        self.bt_sohangmuc = Gtk.SpinButton()
        self.bt_sohangmuc.set_adjustment(tuychinh)
        self.lb_ngaycapnhat = Gtk.Label('Ngày cập nhật')
        self.et_ngaycapnhat = Gtk.Entry()
        self.et_ngaycapnhat.set_text(self.ngayhientai)
        self.bt_capnhat = Gtk.Button('Cập nhât')
        #Sắp xếp các tiện ích


if __name__ == '__main__':
    win = nhapchitieu()
    win.connect('destroy', Gtk.main_quit)
    win.show_all()
    Gtk.main()