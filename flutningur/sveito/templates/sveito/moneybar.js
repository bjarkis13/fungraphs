<style>

.axis path,
.axis line {
  fill: none;
  stroke: #000;
  shape-rendering: crispEdges;
}

.legend {
	font-size: 16px;
}

.barbarbar {
  fill: steelblue;
}

.x.axisbar path {
  display: none;
}

.y.axisbar path {
  stroke: black;
  //stroke-width: 100;
  fill: none;
}

.lines .tick {
  stroke: #888;
  stroke-width: 0.5;
  opacity: 0.5;
}

.lines .path {
  stroke-width: 0;
}

</style>
<script>

var margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var x0 = d3.scale.ordinal()
    .rangeRoundBands([0, width], .1);

var x1 = d3.scale.ordinal();

var y = d3.scale.linear()
    .range([height, 0]);

var color = d3.scale.ordinal()
    .range(['#66c2a5','#fc8d62','#8da0cb','#e78ac3','#a6d854']);

var xAxis = d3.svg.axis()
    .scale(x0)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")
  	//.tickFormat(d3.format(".2s"));

var svg = d3.select("span.moneybar").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


var data = [
{% for i in spending %}
{
	{% for val,name in i %}
	'{{ name }}' : '{{ val }}',
	{% endfor %}
},
{% endfor %}
];

  var ageNames = d3.keys(data[0]).filter(function(key) { return key !== "Sveito"; });

  data.forEach(function(d) {
    d.ages = ageNames.map(function(name) { return {name: name, value: +d[name]}; });
  });


  x0.domain(data.map(function(d) { return d.Sveito; }));
  x1.domain(ageNames).rangeRoundBands([0, x0.rangeBand()]);
  y.domain([0, d3.max(data, function(d) { return d3.max(d.ages, function(d) { return d.value; }); })]);

  svg.append("g")
      .attr("class", "x axisbar")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  svg.append("g")
      .attr("class", "y axisbar")
      .call(yAxis)
    .append("text")
      //.attr("transform", "rotate(-90)")
      .attr("y", -20)
      .attr("x", -margin.left)
      .attr("dy", ".71em")
      .style("text-anchor", "start")
      .text("Thousands of ISK per capita");

  var state = svg.selectAll(".state")
      .data(data)
    .enter().append("g")
      .attr("class", "g")
      .attr("transform", function(d) { return "translate(" + x0(d.Sveito) + ",0)"; });

  state.selectAll("rect")
      .data(function(d) { return d.ages; })
    .enter().append("rect")
      .attr("width", x1.rangeBand())
      .attr("x", function(d) { return x1(d.name); })
      .attr("y", function(d) { return y(d.value); })
      .attr("height", function(d) { return height - y(d.value); })
      .style("fill", function(d) { return color(d.name); });


//HERE!
function make_y_axis() {        
    return d3.svg.axis()
        .scale(y)
        .orient("left")
        .ticks(10)
}

svg.append("g")         
        .attr("class", "lines")
        .call(make_y_axis()
            .tickSize(-width, 0, 0)
            .tickFormat("")
        )



svg.append("rect")
	.attr("x",width-170)
    .attr("width", 170)
    .attr("height", 95)
    .attr("fill", "white")
	.style("fill-opacity", 1);


  //All things legend
  var legend = svg.selectAll(".legend")
      .data(ageNames.slice())
    .enter().append("g")
      .attr("class", "noneofyourbusiness")
      .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

  legend.append("rect")
      .attr("x", width - 18)
	  .attr("y", 10 - margin.top)
      .attr("width", 18)
      .attr("height", 18)
      .style("fill", color) 

  legend.append("text")
      .attr("x", width - 24)
      .attr("y", 10 - margin.top + 9)
      .attr("dy", ".35em")
      .style("text-anchor", "end")
      .text(function(d) { return d; });



</script>
