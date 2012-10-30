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

# Simple API for returning temeprature data

import numpy

YEAR, MONTH, DAY, AVG, MAX, MIN = range(6)

class Station(object):
  def __init__(self, name, data_file):
    self.name = name

    # Load the data for this station
    lines = open(data_file).readlines()[1:]

    # self.dates = numpy.zeros([3,len(lines)], dtype=numpy.int32) # year, month, day
    self.temps = numpy.zeros([6,len(lines)]) # avg, max, min

    # Index structures to get ranges for years and months
    self.years = [] # (year, (start, stop))
    self.months = [] # (year, month, (start, stop))

    # Get the values from the first row
    date, avg, max, min = lines[0].strip().split()
    y, m, d = int(date[:4]), int(date[4:6]), int(date[6:])

    current = [y, m]
    start   = [0, 0]
    
    for i, line in enumerate(lines):
      values = line.strip().split()
      if len(values) == 0: continue
      date, avg, max, min = values

      y, m, d = int(date[:4]), int(date[4:6]), int(date[6:])
      self.temps[:,i] = y, m, d, float(avg), float(max), float(min)

      if current[YEAR] != y:
        self.years.append((current[YEAR], (start[YEAR], i)))
        self.months.append((current[YEAR], current[MONTH], (start[MONTH], i)))        
        start = [i, i]
        current = [y, m]

      elif current[MONTH] != m:
        self.months.append((current[YEAR], current[MONTH], (start[MONTH], i)))        
        start[MONTH] = i
        current[MONTH] = m
    # /for

    self.years.append((current[YEAR], (start[YEAR], i)))
    self.months.append((current[YEAR], current[MONTH], (start[MONTH], i)))        
        
    return

  def daily(self):
    return self.temps
  
  def monthly(self, month = None):
    months = self.months
    if month is not None:
      months = [ms for ms in self.months if ms[MONTH] == month]
      
    results = numpy.zeros((5, len(months)))
    for i, month_slice in enumerate(months):
      s = month_slice[2]
      results[:, i] = (
        self.temps[YEAR, s[0]],
        self.temps[MONTH, s[0]],
        numpy.average(self.temps[AVG, slice(*s)]),
        numpy.max(self.temps[MAX, slice(*s)]),
        numpy.min(self.temps[MIN, slice(*s)]))
    return results

  def yearly(self, year = None):
    years = self.years
    if year is not None:
      years = [ys for ys in self.years if ys[YEAR] == year]
      
    results = numpy.zeros((4, len(years)))
    for i, year_slice in enumerate(years):
      s = year_slice[1]
      results[:, i] = (
        self.temps[YEAR, s[0]],
        numpy.average(self.temps[AVG, slice(*s)]),
        numpy.max(self.temps[MAX, slice(*s)]),
        numpy.min(self.temps[MIN, slice(*s)]))
    return results

  def daily_asdict(self):
    """
    The 'asdict' methods serialize the data into a dictionary that can
    be converted to json for transfer to JavaScript via HTTP.
    """
    data = self.daily()
    
    l = []
    for i in range(data.shape[1]):
      l.append(dict(
        year = int(data[0, i]),
        month = int(data[1, i]),
        day = int(data[2, i]),
        avg = data[3, i],
        max = data[4, i],
        min = data[5, i],
        index = i
        ))

    return {'data': l}

  def monthly_asdict(self, month = None):
    data = self.monthly(month)

    l = []
    for i in range(data.shape[1]):
      l.append(dict(
        year = int(data[0, i]),
        month = int(data[1, i]),
        avg = data[2, i],
        max = data[3, i],
        min = data[4, i],
        index = i
        ))

    return {'data': l}

  def yearly_asdict(self, month = None):
    data = self.yearly()
    l = []
    for i in range(data.shape[1]):
      l.append(dict(
        year = int(data[0, i]),
        avg = data[1, i],
        max = data[2, i],
        min = data[3, i],
        index = i
        ))

    return {'data': l}

      

  
if __name__=='__main__':
  s = Station('KATT', '/Users/cmueller/data/global-temps/katt-all.txt')

