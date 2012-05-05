#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import model
import json

class MainHandler(webapp2.RequestHandler):
    def get(self):
        if self.request.path == '/api/test':
            self.create_tests()
        data = self.icon_list()
        self.response.out.write(json.dumps(data,default=lambda(o):o.to_dict()))

    def icon_list(self):
        q = model.Icon.all()
        return q.fetch(5)
        
    def create_tests(self):
        if model.Icon.all().filter("uri", "/favicon.ico").count() == 0:
            i = model.Icon(uri="/favicon.ico")
            i.put()
            s = model.Semantic(description="app engine")
            s.put()
            l = model.IconSemantics(semantic=s,icon=i,relevant=1)
            l.put()




app = webapp2.WSGIApplication([('/api/.*', MainHandler)],
                              debug=True)
