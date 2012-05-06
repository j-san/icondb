from google.appengine.ext import db

class Icon(db.Model):
    uri = db.StringProperty(required=True)
    #semantics[]
    def to_dict(self):
        return {
            'uri':self.uri,
            'semantics':[s.to_dict() for s in self.semantics]
        }

class IconSemantic(db.Model):
    icon = db.ReferenceProperty(Icon, required=True, collection_name="semantics")
    description = db.StringProperty(required=True)
    relevant = db.RatingProperty()
    def to_dict(self):
        return { 'description': self.description }
