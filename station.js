/*
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
*/

// Client Side Code for Weather Station Vis Example

WeatherStation = Backbone.Model.extend({
  defaults: {
    name: 'KATT',
    month: null,
    data: null

  },
  url: function() { 
    if(this.get('month') == null) {
      return '/data/' + this.get('name') + '/'; 
    } else {
      return '/data/' + this.get('name') + '/month/' + this.get('month') + '/'; 
    }
  }
});

WeatherPlot = Backbone.View.extend({

  initialize: function() {
    this.model.bind('change', this.render, this);
  }, 
  
  render: function() {
    // Set the extents for the current plot
    el_sel = '#' + this.$el.attr('id');
    margin = {top: 20, right: 20, bottom: 30, left: 50};
    width  = $(el_sel).width() - margin.left - margin.right;
    height = $(el_sel).height() - margin.top - margin.bottom;

    // Create the x/y transforms
    x = d3.scale.linear().range([0, width]);
    y = d3.scale.linear().range([height, 0]);
    
    // Create the axes
    x_axis = d3.svg.axis().scale(x).orient('bottom');
    y_axis = d3.svg.axis().scale(y).orient('left');
    if(height < 120) { 
      y_axis = y_axis.ticks(4);
      x_axis = x_axis.ticks(5);
      x_axis = x_axis.tickFormat(function(d) { return d + 1973; });
    } else {
      x_axis = x_axis.tickFormat(function(d) { return Math.floor(d / 12)  + 1973; });
    }

    // Define a 'line' type for the average temp line
    avg_line = d3.svg.line()
      .x(function(d) { return x(d.index); })
      .y(function(d) { return y(d.avg); });

    // Get the data from the model
    data = this.model.get('data');

    // Scale the transforms based on the data
    x.domain(d3.extent(data, function(d) { return d.index; }));
    y.domain([0, 120]);

    // Get the svg element
    plot = d3.select(el_sel);

    // Set the extents transform
    plot = plot.append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // Add the axes
    plot.append("g")
      .attr("class", "axis")
      .attr("transform", "translate(0," + height + ")")
      .call(x_axis);

    plot.append("g")
      .attr("class", "axis")
      .call(y_axis);

    // Display the min/max bars
    plot_enter = plot.selectAll("line").data(data, function(d) { return d.index; })
      .enter()
      .append("line")
      .attr("class", "temp-bar")
      .attr("x1", function(d) { return x(d.index); })
      .attr("y1", function(d) { return y(d.min); })
      .attr("x2", function(d) { return x(d.index); })
      .attr("y2", function(d) { return y(d.max); });

    // Display the average line
    plot.append("path")
      .datum(data)
      .attr("class", "temp-line")
      .attr("d", avg_line)
      .attr("stroke", "white")
      .attr("fill", "none");
  }
});


$(document).ready(function() {

  // Attach the models and views
  overview_model = new WeatherStation();
  overview_view  = new WeatherPlot({
    model: overview_model,
    el: $('#overview_plot')
  });

  overview_model.fetch()

  for(i = 0; i <= 12; i++) {
    model = new WeatherStation({
      month: i
    });
    view  = new WeatherPlot({
      model: model,
      el: $('#mo_' + i),
    });
    model.fetch();
  }
});



