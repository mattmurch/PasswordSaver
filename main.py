#Address Book Program


class Songs(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	path_sans_space = db.Column(db.String(120), index=True, unique=True)
	path_with_space = db.Column(db.String(120), index=True, unique=True)
	
	def __repr__(self):
		return '<Song %r>' % (self.path_with_space)
