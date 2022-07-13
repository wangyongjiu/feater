// https://observablehq.com/@d3/radial-area-chart@487
function _1(md){return(
md`# Radial Area Chart

This chart shows the daily average temperature range and recorded extremes at San Francisco International Airport from 1999–2018. This form is useful for showing cyclical temporal patterns, such as seasonal weather.

Data: [National Climatic Data Center](https://www.ncdc.noaa.gov/cdo-web/datatools/findstation)`
)}

function _chart(d3,width,height,area,y,data,line,xAxis,yAxis)
{
  const svg = d3.create("svg")
      .attr("viewBox", [-width / 2, -height / 2, width, height])
      .attr("stroke-linejoin", "round")
      .attr("stroke-linecap", "round");

  svg.append("path")
      .attr("fill", "lightsteelblue")
      .attr("fill-opacity", 0.2)
      .attr("d", area
          .innerRadius(d => y(d.minmin))
          .outerRadius(d => y(d.maxmax))
        (data));

  svg.append("path")
      .attr("fill", "steelblue")
      .attr("fill-opacity", 0.2)
      .attr("d", area
          .innerRadius(d => y(d.min))
          .outerRadius(d => y(d.max))
        (data));
    
  svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "steelblue")
      .attr("stroke-width", 1.5)
      .attr("d", line
          .radius(d => y(d.avg))
        (data));

  svg.append("g")
      .call(xAxis);

  svg.append("g")
      .call(yAxis);

  return svg.node();
}


function _width(){return(
954
)}

function _height(width){return(
width
)}

function _margin(){return(
10
)}

function _innerRadius(width){return(
width / 5
)}

function _outerRadius(width,margin){return(
width / 2 - margin
)}

function _x(d3){return(
d3.scaleUtc()
    .domain([Date.UTC(2000, 0, 1), Date.UTC(2001, 0, 1) - 1])
    .range([0, 2 * Math.PI])
)}

function _y(d3,data,innerRadius,outerRadius){return(
d3.scaleLinear()
    .domain([d3.min(data, d => d.minmin), d3.max(data, d => d.maxmax)])
    .range([innerRadius, outerRadius])
)}

function _xAxis(x,DOM,d3,innerRadius,outerRadius){return(
g => g
    .attr("font-family", "sans-serif")
    .attr("font-size", 10)
    .call(g => g.selectAll("g")
      .data(x.ticks())
      .join("g")
        .each((d, i) => d.id = DOM.uid("month"))
        .call(g => g.append("path")
            .attr("stroke", "#000")
            .attr("stroke-opacity", 0.2)
            .attr("d", d => `
              M${d3.pointRadial(x(d), innerRadius)}
              L${d3.pointRadial(x(d), outerRadius)}
            `))
        .call(g => g.append("path")
            .attr("id", d => d.id.id)
            .datum(d => [d, d3.utcMonth.offset(d, 1)])
            .attr("fill", "none")
            .attr("d", ([a, b]) => `
              M${d3.pointRadial(x(a), innerRadius)}
              A${innerRadius},${innerRadius} 0,0,1 ${d3.pointRadial(x(b), innerRadius)}
            `))
        .call(g => g.append("text")
          .append("textPath")
            .attr("startOffset", 6)
            .attr("xlink:href", d => d.id.href)
            .text(d3.utcFormat("%B"))))
)}

function _yAxis(y){return(
g => g
    .attr("text-anchor", "middle")
    .attr("font-family", "sans-serif")
    .attr("font-size", 10)
    .call(g => g.selectAll("g")
      .data(y.ticks().reverse())
      .join("g")
        .attr("fill", "none")
        .call(g => g.append("circle")
            .attr("stroke", "#000")
            .attr("stroke-opacity", 0.2)
            .attr("r", y))
        .call(g => g.append("text")
            .attr("y", d => -y(d))
            .attr("dy", "0.35em")
            .attr("stroke", "#fff")
            .attr("stroke-width", 5)
            .text((x, i) => `${x.toFixed(0)}${i ? "" : "°F"}`)
          .clone(true)
            .attr("y", d => y(d))
          .selectAll(function() { return [this, this.previousSibling]; })
          .clone(true)
            .attr("fill", "currentColor")
            .attr("stroke", "none")))
)}

function _line(d3,x){return(
d3.lineRadial()
    .curve(d3.curveLinearClosed)
    .angle(d => x(d.date))
)}

function _area(d3,x){return(
d3.areaRadial()
    .curve(d3.curveLinearClosed)
    .angle(d => x(d.date))
)}

async function _rawdata(d3,FileAttachment){return(
d3.csvParse(await FileAttachment("sfo-temperature.csv").text(), d3.autoType)
)}

function _data(d3,rawdata){return(
Array.from(d3.rollup(
  rawdata, 
  v => ({
    date: new Date(Date.UTC(2000, v[0].DATE.getUTCMonth(), v[0].DATE.getUTCDate())),
    avg: d3.mean(v, d => d.TAVG || NaN),
    min: d3.mean(v, d => d.TMIN || NaN),
    max: d3.mean(v, d => d.TMAX || NaN),
    minmin: d3.min(v, d => d.TMIN || NaN),
    maxmax: d3.max(v, d => d.TMAX || NaN)
  }), 
  d => `${d.DATE.getUTCMonth()}-${d.DATE.getUTCDate()}`
).values())
  .sort((a, b) => d3.ascending(a.date, b.date))
)}

export default function define(runtime, observer) {
  const main = runtime.module();
  function toString() { return this.url; }
  const fileAttachments = new Map([
    ["sfo-temperature.csv", {url: new URL("./files/3d5bf947197b197e4d16880d261d141e3e7920df21dfece9aae543ac2628b787db1b84d0b1dbd55fd49a6d740c8375fe14f5d8934732bff6f5e0b99c488073b1", import.meta.url), mimeType: null, toString}]
  ]);
  main.builtin("FileAttachment", runtime.fileAttachments(name => fileAttachments.get(name)));
  main.variable(observer()).define(["md"], _1);
  main.variable(observer("chart")).define("chart", ["d3","width","height","area","y","data","line","xAxis","yAxis"], _chart);
  main.variable(observer("width")).define("width", _width);
  main.variable(observer("height")).define("height", ["width"], _height);
  main.variable(observer("margin")).define("margin", _margin);
  main.variable(observer("innerRadius")).define("innerRadius", ["width"], _innerRadius);
  main.variable(observer("outerRadius")).define("outerRadius", ["width","margin"], _outerRadius);
  main.variable(observer("x")).define("x", ["d3"], _x);
  main.variable(observer("y")).define("y", ["d3","data","innerRadius","outerRadius"], _y);
  main.variable(observer("xAxis")).define("xAxis", ["x","DOM","d3","innerRadius","outerRadius"], _xAxis);
  main.variable(observer("yAxis")).define("yAxis", ["y"], _yAxis);
  main.variable(observer("line")).define("line", ["d3","x"], _line);
  main.variable(observer("area")).define("area", ["d3","x"], _area);
  main.variable(observer("rawdata")).define("rawdata", ["d3","FileAttachment"], _rawdata);
  main.variable(observer("data")).define("data", ["d3","rawdata"], _data);
  return main;
}
