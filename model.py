from google.appengine.ext import db
from google.appengine.ext import search
from google.appengine.api import apiproxy_stub_map

class Icon(db.Model):
    uri = db.StringProperty(required=True)
    #semantics[]
    
    @property
    def semantics(self):
        return Semantic.all().filter('icons =', self.key())
    
    def add_semantic(self, desc):
        #s = Semantic.all().filter("description", desc).get()
        #if not s:
            #s = Semantic(description=desc, relevant=1)
            
        s = Semantic.get_or_insert(desc, description=desc)

        s.icons.append(self.key())
        s.put()


    def to_dict(self,deps=True):
        rep = {
            'id': self.key().id(),
            'uri': self.uri
        }
        if deps:
            rep['semantics'] = [s.to_dict(False) for s in self.semantics]
        return rep


class Semantic(search.SearchableModel):
    description = db.StringProperty(required=True)
    icons = db.ListProperty(db.Key)
    #icon = db.ReferenceProperty(Icon, collection_name="semantics")
    relevant = db.RatingProperty()
    
    def to_dict(self,deps=True):
        rep = {
            'id': self.key().id(),
            'description': self.description
        }
        if deps:
            rep['icons'] = [Icon.get(i).to_dict(False) for i in self.icons]
        return rep

def clear_cascade(service, call, request, response):
    if call == 'Delete':
        for key in request.key_list():
            if key.path().element_list()[0].type() == 'Icon':
                for s in Semantic.all().filter('icons =', key).fetch(None):
                    s.icons.remove(key)
                    s.put()

apiproxy_stub_map.apiproxy.GetPostCallHooks().Append('clear_cascade', clear_cascade)
