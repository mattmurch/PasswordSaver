from kivy.app import App
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.listview import ListItemButton
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.listview import ListItemButton
from kivy.adapters.listadapter import ListAdapter

import app


#TODO: RECREATE LISTVIEW WITH BUTTON TO SELECT AND GRIDVIEW FOR TABLE

class AddressListButton(ListItemButton):
	pass

class LoginScreen(Screen):
	def do_login(self, loginText, passwordText):
		if loginText == "Matt" and passwordText=="holla":
			self.manager.current = 'mainscreen'

		
class MainScreen(Screen):
	name_text_input = ObjectProperty()
	p_number_text_input = ObjectProperty()
	addresslist = ObjectProperty()
	
	def submit_entry(self):
		if self.p_number_text_input.text != '' and self.name_text_input.text != '':
			app.add_new_contact(self.name_text_input.text, self.p_number_text_input.text)
			self.refresh_data()
	
	def delete_entry(self, *args):
		if self.addresslist.adapter.selection:
			selection = self.addresslist.adapter.selection[0].text
			selection_id = selection.split(",")[0]
			selection_id = selection_id.split(" ")[-1]
			app.delete_contact_by_field_and_value('id', selection_id)
			self.refresh_data()
	
	def update_entry(self, *args):
		if self.addresslist.adapter.selection:
			selection = self.addresslist.adapter.selection[0].text
			selection_id = selection.split(",")[0]
			selection_id = selection_id.split(" ")[-1]
			if self.name_text_input.text != "":
				app.update_contact('id', selection_id, 'name', self.name_text_input.text)
			if self.p_number_text_input != "":
				app.update_contact('id', selection_id, 'p_number', self.p_number_text_input.text)
			self.refresh_data()
			
	def refresh_data(self):
		new_data_items = []
		contacts = app.search_all()
		for contact in contacts:
			new_data_items.append(str(contact))
		self.addresslist.adapter.data = new_data_items
		self.addresslist._trigger_reset_populate()
		return new_data_items
	
class ScreenManager(ScreenManager):
	pass


class AddressBookApp(App):
	def build(self):
		pass
	
	
if __name__=="__main__":
	AddressBookApp().run()
