<style>
#bargraph  {
    font: 10px sans-serif;
}

.y.axis path {
    display: none;
}

.y.axis line {
    stroke: #fff;
            stroke-opacity: .2;
            shape-rendering: crispEdges;
}

.y.axis .zero line {
    stroke: #000;
            stroke-opacity: 1;
}


.gender {
	font-size: 22px;
	font-weight: bold;
	text-anchor: middle;
	fill: #666
}

.legend {
	font-size: 16px;
}

.birthyear,
    .age {
        text-anchor: middle;
    }

.birthyear {
    fill: #fff;
}

rectbeni {
    fill-opacity: .6;
    fill: #e377c2;
}

rect:first-child {
    fill: #1f77b4;
}

</style>

<script>
// SET UP DIMENSIONS
var w = 500,
    h = 300;

// margin.middle is distance from center line to each y-axis
var margin = {
    top: 20,
    right: 20,
    bottom: 24, //24
    left: 20,
    middle: 28
};

// the width of each side of the chart
var regionWidth = w/2 - margin.middle;

// these are the x-coordinates of the y-axes
var pointA = regionWidth,
    pointB = w - regionWidth;

// dictionary to create y-axis label
var dic = {20:"100+"};
for(i=0;i<20;i++)
{
    dic[i] = (i*5).toString()+"-"+(i*5+4).toString()
}

// data for the current municipality
var muniData = [
{% for i in gpop %}
{group: dic[{{ i.0 }}], male: {{ i.1 }}, female: {{ i.2 }}},
{% endfor %}
];

// data for all of iceland
var allData = [
{% for i in allgpop %}
{group: dic[{{ i.0 }}], male: {{ i.1 }}, female: {{ i.2 }}},
{% endfor %}
];

// GET THE TOTAL POPULATION SIZE AND CREATE A FUNCTION FOR RETURNING THE PERCENTAGE
var totalMuni = d3.sum(muniData, function(d) { return d.male + d.female; });
var totalAll = d3.sum(allData, function(d) { return d.male + d.female; });
percentageMuni = function(d) { return d / totalMuni; };
percentageAll = function(d) { return d / totalAll; };


// CREATE SVG
var svg = d3.select('div.pyramid').append('svg')
.attr('width', margin.left + w + margin.right)
.attr('height', margin.top + h + margin.bottom)
// ADD A GROUP FOR THE SPACE WITHIN THE MARGINS
.append('g')
.attr('transform', translation(margin.left, margin.top));


// Sets some text
svg.append("text").text("male")
.attr("class","gender")
.attr("x", w/5)
.attr("y", 20);

svg.append("text").text("female")
.attr("class","gender")
.attr("x", w-w/5)
.attr("y", 20); //h+38

// Set legend not done
var legendRectSize = 18;
var legendSpacing = 4;

var legend = svg.selectAll('.legend')
//.data(color.domain())
//.enter()
.append('g')
.attr('class', 'legend')
.attr('transform', function(d, i) {
	var height = legendRectSize + legendSpacing;
	var offset =  h / 2;
	var horz = -2 * legendRectSize;
	var vert = i * height - offset;
	return 'translate(' + horz + ',' + vert + ')';
});

legend.append('rect')
.attr('width', legendRectSize)
.attr('height', legendRectSize)
.style('fill', 'red')
.style('stroke', 'red');



// find the maximum data value on either side
//  since this will be shared by both of the x-axes
var maxValue = Math.max(
        d3.max(muniData, function(d) { return percentageMuni(d.male); }),
        d3.max(muniData, function(d) { return percentageMuni(d.female); })
        );

// SET UP SCALES

// the xScale goes from 0 to the width of a region
//  it will be reversed for the left x-axis
    var xScale = d3.scale.linear()
    .domain([0, 0.1])//maxValue])
.range([0, regionWidth])
    .nice();

    var xScaleLeft = d3.scale.linear()
.domain([0, maxValue])
    .range([regionWidth, 0]);

    var xScaleRight = d3.scale.linear()
.domain([0, maxValue])
    .range([0, regionWidth]);

var yScale = d3.scale.ordinal()
    .domain(muniData.map(function(d) { return d.group; }))
    .rangeRoundBands([h,0], 0.1);


    // SET UP AXES
    var yAxisLeft = d3.svg.axis()
.scale(yScale)
    .orient('right')
.tickSize(4,0)
    .tickPadding(margin.middle-4);

    var yAxisRight = d3.svg.axis()
.scale(yScale)
    .orient('left')
.tickSize(4,0)
    .tickFormat('');

    var xAxisRight = d3.svg.axis()
.scale(xScale)
    .orient('bottom')
    .tickFormat(d3.format('%'));


var xAxisLeft = d3.svg.axis()
    // REVERSE THE X-AXIS SCALE ON THE LEFT SIDE BY REVERSING THE RANGE
.scale(xScale.copy().range([pointA, 0]))
    .orient('bottom')
    .tickFormat(d3.format('%'));

    // MAKE GROUPS FOR EACH SIDE OF CHART
    // scale(-1,1) is used to reverse the left side so the bars grow left instead of right
    var leftAllGroup = svg.append('g')
    .attr('transform', translation(pointA, 0) + 'scale(-1,1)');
    var rightAllGroup = svg.append('g')
    .attr('transform', translation(pointB, 0));
    var leftBarGroup = svg.append('g')
    .attr('transform', translation(pointA, 0) + 'scale(-1,1)');
    var rightBarGroup = svg.append('g')
    .attr('transform', translation(pointB, 0));


    // DRAW AXES
    svg.append('g')
    .attr('class', 'axis y left')
    .attr('transform', translation(pointA, 0))
.call(yAxisLeft)
    .selectAll('text')
    .style('text-anchor', 'middle');

    svg.append('g')
    .attr('class', 'axis y right')
    .attr('transform', translation(pointB, 0))
    .call(yAxisRight);

    svg.append('g')
    .attr('class', 'axis x left')
    .attr('transform', translation(0, h))
    .call(xAxisLeft);

    svg.append('g')
    .attr('class', 'axis x right')
    .attr('transform', translation(pointB, h))
    .call(xAxisRight);


    // DRAW BARS
    leftBarGroup.selectAll('.bar.left')
.data(muniData)
    .enter().append('rect')
    .attr('class', 'bar left')
    .attr('x', 0)
    .attr('y', function(d) { return yScale(d.group); })
    .attr('width', function(d) { return xScale(percentageMuni(d.male)); })
    .attr('height', yScale.rangeBand());



    leftAllGroup.selectAll('.bar.all')
.data(allData)
    .enter().append('rect')
    .attr('class', 'bar all')
    .attr('x', 0)
    .attr('y', function(d) { return yScale(d.group); })
    .attr('width', function(d) { return xScale(percentageAll(d.male)); })
    .attr('height', yScale.rangeBand());


    rightBarGroup.selectAll('.bar.right')
.data(muniData)
    .enter().append('rect')
    .attr('class', 'bar right')
    .attr('x', 0)
    .attr('y', function(d) { return yScale(d.group); })
    .attr('width', function(d) { return xScale(percentageMuni(d.female)); })
    .attr('height', yScale.rangeBand());


    rightAllGroup.selectAll('.bar.all')
.data(allData)
    .enter().append('rect')
    .attr('class', 'bar all')
    .attr('x', 0)
    .attr('y', function(d) { return yScale(d.group); })
    .attr('width', function(d) { return xScale(percentageAll(d.female)); })
    .attr('height', yScale.rangeBand());

    // so sick of string concatenation for translations
    function translation(x,y) {
        return 'translate(' + x + ',' + y + ')';
                };

</script>

