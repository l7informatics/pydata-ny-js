__license__ = """
Copyright (c) 2012, Lab7 Systems, Inc.
All rights reserved.

Redistribution and use in source and binary forms, with or without.
modification, are permitted provided that the following conditions are.
met: 

Redistributions of source code must retain the above copyright notice,.
this list of conditions and the following disclaimer. 

Redistributions in binary form must reproduce the above copyright.
notice, this list of conditions and the following disclaimer in the.
documentation and/or other materials provided with the distribution. 

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR 
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT 
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, 
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT 
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY 
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. 
"""

# Simple Web app for viewing data from a weather station
import json
from tornado import web, ioloop
import temperature

katt = temperature.Station('KATT', 'katt-all.txt')

class IndexHandler(web.RequestHandler):
  def get(self):
    self.render('station.html') #, {'station_name': 'KATT'})
 
class DataHandler(web.RequestHandler):
  def get(self, station):
    return self.write(json.dumps(katt.monthly_asdict()))

class MonthlyDataHandler(web.RequestHandler):
  def get(self, station, month):
    return self.write(json.dumps(katt.monthly_asdict(int(month))))

app = web.Application([
  (r'/', IndexHandler),
  (r'/data/([a-zA-Z]+)/', DataHandler),
  (r'/data/([a-zA-Z]+)/month/([0-9]+)/', MonthlyDataHandler),  
  (r'/local_static/(.*)', web.StaticFileHandler, {'path': './'}),
  ],
  debug = True
  )

if __name__=='__main__':
  import logging
  logging.getLogger().setLevel(logging.DEBUG)

  app.listen(8001)
  ioloop.IOLoop.instance().start()
  

