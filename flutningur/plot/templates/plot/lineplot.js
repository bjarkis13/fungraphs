<style>
.nvd3 g.nv-groups path.nv-line {
      stroke-width: {{ lineplot.linewidth }};
}
.nvtooltip {
    font: inherit;
}
.nvd3 .nv-axis .nv-axisMaxMin text {
    font-weight: 400;

}
.nvd3 * text {
    font: inherit;
}
g.nv-y g.nv-axis g text.nv-axislabel {
    //transform: translate(160px,34px) rotate(0deg) !important;
    transform-origin: 0px 00px !important;
    transform: translate(160px,34px) rotate(0deg) !important;
    text-anchor: start !important;
}
</style>
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
        .forceY([{{lineplot.y.force}}])
    {% if lineplot.log %}
        .y(function(d) { return d[1] === 0 ? 1 : d[1] })
        .yScale(d3.scale.log())
    {% else %}
        .yScale(d3.scale.linear())
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
    chart.tooltip.valueFormatter(d3.format("{{ lineplot.valformat|default:","}}"));
    chart.legend.margin({top: 2, right:25, left:50, bottom: 0});
    chart.xAxis
        .axisLabel('Year')
        .tickFormat(d3.format(''));

    chart.yAxis
        .axisLabel('{{ lineplot.y.name }}')
    {% if lineplot.log %}
        .tickValues([1,10,100,1000,10000])
    {% endif %}
        .tickFormat(d3.format('{{ lineplot.y.format }}'));

    d3.select('#chart1')
        .datum(histcatexplong)
        .transition().duration(500)
        .call(chart);

    nv.utils.windowResize(chart.update);
    return chart;
});
</script>
