#!/bin/usr/python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from datetime import date as ngaythang

class nhaphotro(Gtk.Window):
    
    def __init__(self):
        
        Gtk.Window.__init__(self, title='Tạo cơ sở dữ liệu quản lý chi tiêu')
        
