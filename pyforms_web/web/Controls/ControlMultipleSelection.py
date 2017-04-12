from pyforms_web.web.Controls.ControlBase import ControlBase
import simplejson

class ControlMultipleSelection(ControlBase):

	def __init__(self, label = "",  defaultValue = [],helptext=''):
		super(ControlMultipleSelection, self).__init__(label, defaultValue, helptext)
		self._items={}


	def init_form(self): return "new ControlMultipleSelection('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )

	def add_item(self, label, value = None):
		if self._items==None: self._items={}
		
		if value==None:
			self._items[label] = label
		else:
			self._items[label] = value
	   
		self.mark_to_update_client()


	def clear_items(self):
		self._items = {}
		self._value = None
		self.mark_to_update_client()


	def serialize(self):
		data = ControlBase.serialize(self)
		items = []
		for key, value in self._items.items():
			items.append({'text': str(key), 'value': str(value), 'name': str(key)})
		
		#value = str(self._value) if self._value is not None else None
		if isinstance(self._value, list) and len(self._value)>0:
			value = list(map(str,sorted(self._value)))
		else:
			value = None


		data.update({ 'items': items, 'value': value })
		return data
		
	

	def deserialize(self, properties):
		ControlBase.deserialize(self, properties)
		value = properties.get('value', [])
		values = []
		for v in value:
			if len(v.strip())>0:
				values.append(v)
		self._value = values