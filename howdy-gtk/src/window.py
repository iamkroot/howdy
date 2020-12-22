# Opens and controls main ui window
import cairo
import gi
import signal
import sys
import os
import elevate

# Make sure we have the libs we need
gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")

# Import them
from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk


class MainWindow(gtk.Window):
	def __init__(self):
		"""Initialize the sticky window"""
		# Make the class a GTK window
		gtk.Window.__init__(self)

		self.connect("destroy", self.exit)

		self.builder = gtk.Builder()
		self.builder.add_from_file("./ui.glade")
		self.builder.connect_signals(self)

		self.window = self.builder.get_object("mainwindow")
		self.userlist = self.builder.get_object("userlist")
		self.modellistbox = self.builder.get_object("modellistbox")

		# Create a treeview that will list the model data
		self.treeview = gtk.TreeView()

		# Set the coloums
		for i, column in enumerate(["ID", "Created", "Label"]):
			cell = gtk.CellRendererText()
			col = gtk.TreeViewColumn(column, cell, text=i)

			self.treeview.append_column(col)

		# Add the treeview
		self.modellistbox.add(self.treeview)

		filelist = os.listdir("/lib/security/howdy/models")
		self.active_user = ""

		for file in filelist:
			self.userlist.append_text(file[:-4])

			if not self.active_user:
				self.active_user = file[:-4]

		self.userlist.set_active(0)

		self.window.show_all()
		# self.resize(300, 300)

		# Start GTK main loop
		gtk.main()

	def load_model_list(self):
		"""(Re)load the model list"""

		# Execute the list commond to get the models
		# output = subprocess.check_output(["howdy", "list", "--plain", "-U", self.active_user])
		output = "1,2020-12-05 14:10:22,sd\n2,2020-12-05 14:22:41,\n3,2020-12-05 14:57:37,Model #3" + self.active_user

		# Split the output per line
		# lines = output.decode("utf-8").split("\n")
		lines = output.split("\n")

		# Create a datamodel
		self.listmodel = gtk.ListStore(str, str, str)

		# Add the models to the datamodel
		for i in range(len(lines)):
			self.listmodel.append(lines[i].split(","))

		self.treeview.set_model(self.listmodel)

	def exit(self, widget, context):
		"""Cleanly exit"""
		gtk.main_quit()
		sys.exit()


# Make sure we quit on a SIGINT
signal.signal(signal.SIGINT, signal.SIG_DFL)

# Make sure we run as sudo
elevate.elevate()

import window_tab_models
MainWindow.on_user_change = window_tab_models.on_user_change
MainWindow.on_model_add = window_tab_models.on_model_add
MainWindow.on_model_delete = window_tab_models.on_model_delete

# Open the GTK window
window = MainWindow()