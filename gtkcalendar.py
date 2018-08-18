import os, sys, gi, datetime, calendar

gi.require_version("Gtk", "3.0")
gi.require_version("Notify", "0.7")

from gi.repository import Gtk, Notify, GLib

APPLICATION_NAME = "Simple Calendar"
GLib.set_prgname(APPLICATION_NAME)

def print_r(message):
    print("[%s] %s" % (datetime.datetime.now().strftime('%X'), message))

class SimpleCalendar(Gtk.Window):

    clickCounter = 0

    def __init__(self):
        Gtk.Window.__init__(self)

        # Initialize the notification system
        Notify.init(APPLICATION_NAME)
        self.notification = None

        self.set_size_request(320, 320)
        self.set_icon_name("application-x-executable")
        self.set_wmclass(APPLICATION_NAME, APPLICATION_NAME)
        self.set_title(APPLICATION_NAME)

        # Define the calendar here
        self.calendar = Gtk.Calendar()

        # Create and set a Gtk.HeaderBar as the windows' titlebar
        self.buildHeaderbar()

        self.box = Gtk.Box( orientation = Gtk.Orientation.VERTICAL )
        self.add(self.box)

        # Create the calendar
        self.buildCalendar()

        # Create the actionbar
        self.buildActionbar()

        self.connect("destroy", Gtk.main_quit)
        self.show_all()

    def buildHeaderbar(self):
        self.headerbar = Gtk.HeaderBar()
        self.headerbar.set_title(self.get_title())
        self.headerbar.set_show_close_button(True)
        self.setSubtitle()

        self.navigationbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(self.navigationbox.get_style_context(), "linked")

        self.buttonBack = Gtk.Button(None, image = Gtk.Image.new_from_icon_name("go-previous-symbolic", Gtk.IconSize.BUTTON))
        self.buttonBack.set_sensitive(not self.calendar.get_property("no-month-change"))
        self.buttonBack.connect("clicked", self.decrementMonth)
        self.navigationbox.add(self.buttonBack)

        self.buttonCurrentDate = Gtk.Button(label="Vandaag")
        self.buttonCurrentDate.connect("clicked", self.resetToCurrentDate)
        self.navigationbox.add(self.buttonCurrentDate)

        self.buttonForward = Gtk.Button(None, image = Gtk.Image.new_from_icon_name("go-next-symbolic", Gtk.IconSize.BUTTON))
        self.buttonForward.set_sensitive(not self.calendar.get_property("no-month-change"))
        self.buttonForward.connect("clicked", self.incrementMonth)
        self.navigationbox.add(self.buttonForward)

        self.headerbar.pack_start(self.navigationbox)

        buttonToggleActionbar = Gtk.Button(None, image = Gtk.Image.new_from_icon_name("go-down-symbolic", Gtk.IconSize.BUTTON))
        buttonToggleActionbar.connect("clicked", self.onToggleActionbar)
        self.headerbar.pack_end(buttonToggleActionbar)

        self.set_titlebar(self.headerbar)

    def buildCalendar(self):
        self.calendar.set_property("show-heading", False)
        self.calendar.connect("day-selected", self.setSubtitle)
        self.box.pack_start(self.calendar, True, True, 0)

    def buildActionbar(self):
        self.revealer = Gtk.Revealer()
        self.revealer.set_reveal_child(False)
        self.box.pack_end(self.revealer, False, False, 0)

        self.actionbar = Gtk.ActionBar()
        self.actionbar.set_hexpand(True)
        self.revealer.add(self.actionbar)

        checkbuttonHeading = Gtk.CheckButton(label = "Toon koppen")
        checkbuttonHeading.set_active(self.calendar.get_property("show-heading"))
        checkbuttonHeading.connect("toggled", self.onShowHeadingChange)
        self.actionbar.pack_start(checkbuttonHeading)

        checkbuttonDayNames = Gtk.CheckButton(label = "Toon dagen")
        checkbuttonDayNames.set_active(self.calendar.get_property("show-day-names"))
        checkbuttonDayNames.connect("toggled", self.onShowDayChange)
        self.actionbar.pack_start(checkbuttonDayNames)

        checkbuttonPreventChange = Gtk.CheckButton(label = "Vergrendel maand/jaar")
        checkbuttonPreventChange.set_active(self.calendar.get_property("no-month-change"))
        checkbuttonPreventChange.connect("toggled", self.onPreventMonthChange)
        self.actionbar.pack_start(checkbuttonPreventChange)

        checkbuttonShowWeeks = Gtk.CheckButton(label = "Toon weeknummers")
        checkbuttonShowWeeks.set_active(self.calendar.get_property("show-week-numbers"))
        checkbuttonShowWeeks.connect("toggled", self.onShowWeeksChange)
        self.actionbar.pack_start(checkbuttonShowWeeks)

    def setSubtitle(self, source = None):
        if source is not None:
            month = calendar.month_name[source.get_date().month + 1]
            year = source.get_date().year
        else:
            month = calendar.month_name[self.calendar.get_date().month + 1]
            year = self.calendar.get_date().year

        self.headerbar.set_subtitle('%s %d' % (month, year))

    def onShowHeadingChange(self, checkbutton):
        self.calendar.set_property("show-heading", checkbutton.get_active())

        if checkbutton.get_active():
            self.navigationbox.hide()
        else:
            self.navigationbox.show()

    def onShowDayChange(self, checkbutton):
        self.calendar.set_property("show-day-names", checkbutton.get_active())

    def onPreventMonthChange(self, checkbutton):
        active = checkbutton.get_active()

        self.calendar.set_property("no-month-change", active)
        self.buttonForward.set_sensitive(not active)
        self.buttonBack.set_sensitive(not active)
        self.buttonCurrentDate.set_sensitive(not active)

    def onShowWeeksChange(self, checkbutton):
        self.calendar.set_property("show-week-numbers", checkbutton.get_active())

    def decrementMonth(self, button):
        month = self.calendar.get_property("month")

        if month == 0:
            self.calendar.set_property("month", 11)
            self.calendar.set_property("year", self.calendar.get_property("year") - 1)
        else:
            self.calendar.set_property("month", month - 1)

        self.setSubtitle()

    def incrementMonth(self, button):
        month = self.calendar.get_property("month")

        if month == 11:
            self.calendar.set_property("month", 0)
            self.calendar.set_property("year", self.calendar.get_property("year") + 1)
        else:
            self.calendar.set_property("month", month + 1)

        self.setSubtitle()

    def resetToCurrentDate(self, button):
        today = datetime.date.today()
        self.calendar.set_property("day", today.day)
        self.calendar.set_property("month", today.month-1)
        self.calendar.set_property("year", today.year)

        self.setSubtitle()

    def onToggleActionbar(self, button):
        reveal = self.revealer.get_reveal_child()
        self.revealer.set_reveal_child(not reveal)

        self.clickCounter += 1

        if self.clickCounter % 2 == True:
            button.set_image(Gtk.Image.new_from_icon_name("go-up-symbolic", Gtk.IconSize.BUTTON))
        else:
            button.set_image(Gtk.Image.new_from_icon_name("go-down-symbolic", Gtk.IconSize.BUTTON))

    def createNotification(self, message, buttons = None, urgency = Notify.Urgency.NORMAL):
        if self.notification:
            self.notification.close()

        self.notification = Notify.Notification.new(APPLICATION_NAME, message, None)
        self.notification.set_urgency(urgency)

        if buttons is not None:
            for name, label, callback in buttons:
                if callback is None:
                    callback = lambda *a: sys.stderr.write('callback yo\n')

                self.notification.add_action(name, label, callback)

        self.notification.show()

if __name__ == "__main__":
    Gtk.init(sys.argv)
    cal = SimpleCalendar()
Gtk.main()
