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
import re

uri_reg = re.compile('/api/(.*)')

class MainHandler(webapp2.RequestHandler):
    def get(self):
        action = uri_reg.match(self.request.path).group(1)

        api = AppApi()
        data = None
        if hasattr(api, action):
            data = getattr(api, action)(self.request)

        self.response.out.write(json.dumps(data,default=lambda(o):o.to_dict()))




class AppApi:
    def search(self, request):
        search = request.get('q')
        query = model.IconSemantic.all()
        query.filter('description =', search)
        return query.fetch(5)

    def test(self, request):
        if model.Icon.all().filter("uri", "/favicon.ico").count() == 0:
            i = model.Icon(uri="/favicon.ico")
            i.put()
            s = model.IconSemantic(description="app engine", icon=i, relevant=1)
            s.put()
        
        return self.search(request)


app = webapp2.WSGIApplication([('/api/.*', MainHandler)], debug=True)
