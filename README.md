pydata-ny-js
============

Pydata NY 2012: Chris Mueller's "Python and JavaScript" Talk Example Code

Overview
--------

This repository contains a simple Web application that demonstrates how to develop a full application stack for visualizing data using Python and JavaScript.  The application was created as an example for Chris Mueller's talk, "Python and JavaScript", at the PyData NY 2012  conference. 

The application displays temperature data for a weather station using montly summaries.  The overview plot shows the arvg/min/max tempartures for all months in the sample.  The monthly plots break up the data by month.  Using the Austin data (katt-all.txt), the fact that it's hot in the summer months and warm the rest of the year is easy to see by how much or how little the montly data varies year-to-year. 

The application is implemented using:
* NumPy for data processing
* the Tornado framework for the Web app and RESTish API
* BackboneJS for the client side models
* D3 and SVG for the visualization
* jQuery to tie things together


Depedencies
-----------

The JavaScript dependencies are all loaded directly from the Google and CloudFlare CDNs.

The Web server requires both [NumPy](http://numpy.scipy.org) and [Tornado](http://tornadoweb.org) be installed locally


Running
-------

To run the application, simply start the Web Server once the dependencies have been installed:

    $ python station.py

Then point your browser at [http://localhost:8001](http://localhost:8001)


Files
-----

The files included are:

* readme.txt - this file
* pydata-js.pdf - the presentation
* station.css - CSS for the plots and HTML elements
* station.html - Static structure for the layout
* station.js - Backbone models, D3 vis code, jQuery 
* station.py - RESTish API and Web App
* temperature.py - data model and Python API


Contact
-------

Contact chris dot mueller at lab7 dot io if you have any questions.

License
-------

BSD