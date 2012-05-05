from google.appengine.ext import db

class Icon(db.Model):
    uri = db.StringProperty(required=True)
    #semantics[].sementic
    def to_dict(self):
        return {
            'uri':self.uri,
            'semantics':[s.semantic.to_dict() for s in self.semantics]
        }

class Semantic(db.Model):
    description = db.StringProperty(required=True)
    #icons[].icon
    def to_dict(self):
        return {
            'description':self.description
        }

class IconSemantics(db.Model):
    icon = db.ReferenceProperty(Icon, required=True, collection_name="semantics")
    semantic = db.ReferenceProperty(Semantic, required=True, collection_name="icons")
    relevant = db.RatingProperty()
