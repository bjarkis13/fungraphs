<script>

var histcatexplong = [
{% for key, val in lineplot %}
    { "key" : "{{ key }}", "values" : [
    {% for a,b in val %}
        [{{ a }},{{ b }}],
    {% endfor %}
    ]},
{% endfor %}
];

nv.addGraph(function() {
    var chart = nv.models.lineChart()
        .x(function(d) { return d[0] })
        .y(function(d) { return d[1] === 0 ? 1 : d[1] })
        .yScale(d3.scale.log())
        .color(['#66c2a5','#fc8d62','#8da0cb','#e78ac3','#a6d854','#ffd92f','#e5c494','#b3b3b3'])
        .forceY([1]);
    chart.lines.dispatch.on('elementMouseover.recolor', function(e){
        d3.select(chart.container).select('g.nv-group.nv-series-' + e.seriesIndex).select('path.nv-line').style('stroke-opacity', '1')
    })
    chart.lines.dispatch.on('elementMouseout.recolor', function(e){
        d3.select(chart.container).select('g.nv-group.nv-series-' + e.seriesIndex).select('path.nv-line').style('stroke-opacity', '0.4')

    })
    chart.xAxis
        .axisLabel('Year')
        .tickFormat(d3.format(''));

    chart.yAxis
        .axisLabel('Students (in %)')
        .tickValues([1,10,100,1000,10000,100000])
        .tickFormat(d3.format(''))

    d3.select('#chart1')
        .datum(histcatexplong)
        .transition().duration(500)
        .call(chart);
    chart.rotateLabels(-45);

    nv.utils.windowResize(chart.update);

    return chart;
});
</script>
