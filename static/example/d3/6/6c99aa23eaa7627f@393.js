// https://observablehq.com/@mbostock/electric-usage-2019@393
import define1 from "./a33468b95d0b15b0@808.js";

function _1(md){return(
md`# Electricity Usage, 2019

During sunny days in the summer, my home’s solar cells typically produce more energy than we consume. However, at night, on cloudy days, and during the winter when the sun is lower in the sky, we pull energy from PG&E’s grid.

We also have an electric car and a fast charger that can draw 10 kW! The frequent 4-6 hour evening spikes in energy consumption show the car charging. You can also see our electric furnace warming up the house on cold February mornings. And you can see our four-day power outage in October. 😣

You can visualize your own data from PG&E, too! Follow the instructions below.`
)}

function _chart(d3,width,height,legend,color,xAxis,yAxis,data,x,y,formatDate,formatUsage)
{
  const svg = d3.create("svg")
      .attr("viewBox", [0, 0, width, height])
      .style("background", "white");

  svg.append("g")
    .append(() => legend({
      color,
      title: "Net power consumption (kW)", 
      tickFormat: "+d"
    }));

  svg.append("g")
      .call(xAxis);

  svg.append("g")
      .call(yAxis);

  svg.append("g")
    .selectAll("rect")
    .data(data)
    .join("rect")
      .attr("x", d => x(d.date.getHours()))
      .attr("y", d => y(d3.timeDay(d.date)))
      .attr("width", x.bandwidth() - 1)
      .attr("height", y.bandwidth() - 1)
      .attr("fill", d => color(d.usage))
    .append("title")
      .text(d => `${formatDate(d.date)}
${formatUsage(d.usage)} kW`);

  return svg.node();
}


function _3(md){return(
md`To incorporate your own data into this chart:

1. Go to your [PG&E account](https://pge.com)
1. Under *Your Account*, click *Your Energy Use*
1. Under *Understand your energy use*, click *View Your Energy Use*
1. Scroll down and click the *Green Button* (Download my data)
1. Select *Export usage for a range of days* and *CSV* format
1. Expand the downloaded ZIP file
1. Open the CSV file in a text editor
1. *Delete the first five lines* including your account numbers ⚠️
1. Save the file
1. *Rename the file* to remove your account number ⚠️
1. Hover the *data* cell below
1. Click the <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke-width="2"><path d="M7.19855 2.52175L7.88131 1.79111L7.19855 2.52175ZM12.6 11.7764L13.2581 11.0234L12.6 11.7764ZM5.34191 6.76078L11.9419 12.5293L13.2581 11.0234L6.65809 5.2549L5.34191 6.76078ZM10.8958 13.6864L3.35462 6.63385L1.98852 8.09459L9.52965 15.1472L10.8958 13.6864ZM6.51578 3.25238L13.8172 10.0755L15.1828 8.61419L7.88131 1.79111L6.51578 3.25238ZM3.08395 3.55474C3.91017 2.45311 5.50967 2.31219 6.51578 3.25238L7.88131 1.79111C6.0058 0.0384695 3.02413 0.301162 1.48395 2.35474L3.08395 3.55474ZM3.35462 6.63385C2.49183 5.82695 2.37516 4.49978 3.08395 3.55474L1.48395 2.35474C0.162683 4.11642 0.380169 6.59044 1.98852 8.09459L3.35462 6.63385ZM11.993 13.6551C11.6977 13.9647 11.2082 13.9786 10.8958 13.6864L9.52965 15.1472C10.6432 16.1886 12.3878 16.1388 13.4402 15.0356L11.993 13.6551ZM11.9419 12.5293C12.2764 12.8216 12.2996 13.3337 11.993 13.6551L13.4402 15.0356C14.5328 13.8903 14.4499 12.0651 13.2581 11.0234L11.9419 12.5293Z" fill="currentColor"></path></svg> file icon
11. Click *Replace* and select your file`
)}

async function _data(d3,FileAttachment,parseData){return(
d3.csvParse(await FileAttachment("pge-electric-data.csv").text(), parseData)
)}

function _parseData(parseDate){return(
d => ({date: parseDate(`${d["DATE"]}T${d["START TIME"]}`), usage: +d["USAGE"]})
)}

function _parseDate(d3){return(
d3.timeParse("%Y-%m-%dT%H:%M")
)}

function _dateExtent(d3,data){return(
d3.extent(data, d => d.date)
)}

function _x(d3,margin,width){return(
d3.scaleBand(d3.range(24), [margin.left, width - margin.right]).round(true)
)}

function _y(d3,dateExtent,margin,height){return(
d3.scaleBand(d3.timeDays(...dateExtent), [margin.top, height - margin.bottom]).round(true)
)}

function _color(d3,data)
{
  let [min, max] = d3.extent(data, d => d.usage);
  if (min < 0) {
    max = Math.max(-min, max);
    return d3.scaleDiverging([-max, 0, max], t => d3.interpolateRdBu(1 - t));
  }
  return d3.scaleSequential([0, max], d3.interpolateReds);
}


function _xAxis(margin,d3,x,formatHour){return(
g => g
    .attr("transform", `translate(0,${margin.top})`)
    .call(d3.axisTop(x).tickFormat(formatHour))
    .call(g => g.select(".domain").remove())
)}

function _yAxis(margin,d3,y,formatDay){return(
g => g
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y).tickFormat(formatDay))
    .call(g => g.select(".domain").remove())
)}

function _formatUsage(d3){return(
d3.format(".2f")
)}

function _formatDate(d3){return(
d3.timeFormat("%B %-d, %-I %p")
)}

function _formatDay(d3)
{
  const formatMonth = d3.timeFormat("%b %-d");
  const formatDate = d3.timeFormat("%-d");
  return d => (d.getDate() === 1 ? formatMonth : formatDate)(d);
}


function _formatHour()
{
  return d => d === 0 ? "12 AM" : d === 12 ? "12 PM" : (d % 12) + "";
}


function _width(){return(
954
)}

function _height(margin,d3,dateExtent){return(
margin.top + margin.bottom + (d3.timeDay.count(...dateExtent) + 1) * 10
)}

function _margin(){return(
{top: 70, right: 0, bottom: 0, left: 40}
)}

function _d3(require){return(
require("d3@6")
)}

export default function define(runtime, observer) {
  const main = runtime.module();
  function toString() { return this.url; }
  const fileAttachments = new Map([
    ["pge-electric-data.csv", {url: new URL("./files/data.csv", import.meta.url), mimeType: "text/csv", toString}]
  ]);
  main.builtin("FileAttachment", runtime.fileAttachments(name => fileAttachments.get(name)));
  main.variable(observer()).define(["md"], _1);
  main.variable(observer("chart")).define("chart", ["d3","width","height","legend","color","xAxis","yAxis","data","x","y","formatDate","formatUsage"], _chart);
  // main.variable(observer()).define(["md"], _3);
  main.variable(observer("data")).define("data", ["d3","FileAttachment","parseData"], _data);
  main.variable(observer("parseData")).define("parseData", ["parseDate"], _parseData);
  main.variable(observer("parseDate")).define("parseDate", ["d3"], _parseDate);
  main.variable(observer("dateExtent")).define("dateExtent", ["d3","data"], _dateExtent);
  main.variable(observer("x")).define("x", ["d3","margin","width"], _x);
  main.variable(observer("y")).define("y", ["d3","dateExtent","margin","height"], _y);
  main.variable(observer("color")).define("color", ["d3","data"], _color);
  main.variable(observer("xAxis")).define("xAxis", ["margin","d3","x","formatHour"], _xAxis);
  main.variable(observer("yAxis")).define("yAxis", ["margin","d3","y","formatDay"], _yAxis);
  main.variable(observer("formatUsage")).define("formatUsage", ["d3"], _formatUsage);
  main.variable(observer("formatDate")).define("formatDate", ["d3"], _formatDate);
  main.variable(observer("formatDay")).define("formatDay", ["d3"], _formatDay);
  main.variable(observer("formatHour")).define("formatHour", _formatHour);
  main.variable(observer("width")).define("width", _width);
  main.variable(observer("height")).define("height", ["margin","d3","dateExtent"], _height);
  main.variable(observer("margin")).define("margin", _margin);
  main.variable(observer("d3")).define("d3", ["require"], _d3);
  const child1 = runtime.module(define1);
  main.import("legend", child1);
  return main;
}
