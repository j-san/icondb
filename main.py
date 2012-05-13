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


class MainHandler(webapp2.RequestHandler):
    def get(self):
        parts = self.request.path.strip('/').split('/')
        parts.pop(0) # api
        action = parts.pop(0)

        api = AppApi()
        data = []
        if hasattr(api, action):
            data = getattr(api, action)(self.request, parts)

        self.response.out.write(json.dumps(data,default=lambda(o):o.to_dict()))




class AppApi:
    def search(self, request, parts):
        term = request.get('q') or parts and parts.pop(0)
        return model.Semantic.all().fetch(5)#.search(term).fetch(5)

    def icon(self, request, parts):
        key = parts.pop(0)
        return model.Icon.get_by_id(int(key))

    def test(self, request, parts):
        if model.Icon.all().filter("uri", "/favicon.ico").count() == 0:
            i = model.Icon(uri="/favicon.ico")
            i.put()
            i.add_semantic('hello')
            i.add_semantic('world')
        
        return self.search(request, parts)


app = webapp2.WSGIApplication([('/api/.*', MainHandler)], debug=True)
