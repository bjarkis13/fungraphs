<script>

var histcatexplong = [
{% for key, val in lineplot.values %}
    { "key" : "{{ key }}", "values" : [
    {% for a,b in val %}
        [{{ a }},{{ b }}],
    {% endfor %}
    ]},
{% endfor %}
];

nv.addGraph(function() {
    var chart = nv.models.lineChart()
        .showLegend({% if lineplot.hidelegend %}false{% else %}true{% endif %})
        .x(function(d) { return d[0] })
    {% if lineplot.log %}
        .y(function(d) { return d[1] === 0 ? 1 : d[1] })
        .yScale(d3.scale.log())
        .forceY([1])
    {% else %}
        .y(function(d) { return d[1] })
    {% endif %}
    {% if lineplot.y.range %}
        .yDomain([{{ lineplot.y.range.0 }},{{ lineplot.y.range.1 }}])
    {% endif %}
        .color(['#66c2a5','#fc8d62','#8da0cb','#e78ac3','#a6d854','#ffd92f','#e5c494','#b3b3b3']);
    chart.lines.dispatch.on('elementMouseover.recolor', function(e){
        d3.select(chart.container).select('g.nv-group.nv-series-' + e.seriesIndex).select('path.nv-line').style('stroke-opacity', '1')
    })
    chart.lines.dispatch.on('elementMouseout.recolor', function(e){
        d3.select(chart.container).select('g.nv-group.nv-series-' + e.seriesIndex).select('path.nv-line').style('stroke-opacity', '{{ lineplot.opacity|default:"0.3" }}')

    })
    chart.xAxis
        .axisLabel('Year')
        .tickFormat(d3.format(''));

    chart.yAxis
        .axisLabel('{{ lineplot.y.name }}')
    {% if lineplot.log %}
        .tickValues([1,10,100,1000,10000,100000])
    {% endif %}
        .tickFormat(d3.format('{{ lineplot.y.format }}'));


    d3.select('#chart1')
        .datum(histcatexplong)
        .transition().duration(500)
        .call(chart);

    function moveYaxis() {
        d3.select(".nv-y").select("text.nv-axislabel")
            .attr({"transform":null, x:"-50px", y:"-1.3em"})
            .style("text-anchor","start");
    }
    function my_update() {
        chart.update();
        moveYaxis();
    }
    moveYaxis();
    nv.utils.windowResize(my_update);
    return chart;
});
</script>
