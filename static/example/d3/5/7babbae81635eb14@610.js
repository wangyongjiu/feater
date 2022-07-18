// https://observablehq.com/@mbostock/revenue-by-music-format-1973-2018@610
import define1 from "./a33468b95d0b15b0@808.js";

function _1(md){return(
md`# Revenue by Music Format, 1973–2018

Data: [RIAA](https://www.riaa.com/u-s-sales-database/)`
)}

function _legend(swatches,color,margin){return(
swatches({color, columns: "130px 4", marginLeft: margin.left})
)}

function _chart(d3,width,height,series,color,x,y,formatRevenue,xAxis,yAxis)
{  
  const svg = d3.create("svg")
      .attr("viewBox", [0, 0, width, height]);

  svg.append("g")
    .selectAll("g")
    .data(series)
    .join("g")
      .attr("fill", ({key}) => color(key))
      .call(g => g.selectAll("rect")
        .data(d => d)
        .join("rect")
          .attr("x", d => x(d.data.year))
          .attr("y", d => y(d[1]))
          .attr("width", x.bandwidth() - 1)
          .attr("height", d => y(d[0]) - y(d[1]))
       .append("title")
          .text(d => `${d.data.name}, ${d.data.year}
${formatRevenue(d.data.value)}`));

  svg.append("g")
      .call(xAxis);

  svg.append("g")
      .call(yAxis);

  return svg.node();
}


async function _data(d3,FileAttachment){return(
Object.assign(d3.csvParse(await FileAttachment("music.csv").text(), ({Format, Year, ["Revenue (Inflation Adjusted)"]: Revenue}) => ({name: Format, year: +Year, value: +Revenue})), {y: "Revenue (billions, adj.)"})
)}

function _colors(){return(
new Map([
  ["LP/EP", "#2A5784"],
  ["Vinyl Single", "#43719F"],
  ["8 - Track", "#5B8DB8"],
  ["Cassette", "#7AAAD0"],
  ["Cassette Single", "#9BC7E4"],
  ["Other Tapes", "#BADDF1"],
  ["Kiosk", "#E1575A"],
  ["CD", "#EE7423"],
  ["CD Single", "#F59D3D"],
  ["SACD", "#FFC686"],
  ["DVD Audio", "#9D7760"],
  ["Music Video (Physical)", "#F1CF63"],
  ["Download Album", "#7C4D79"],
  ["Download Single", "#9B6A97"],
  ["Ringtones & Ringbacks", "#BE89AC"],
  ["Download Music Video", "#D5A5C4"],
  ["Other Digital", "#EFC9E6"],
  ["Synchronization", "#BBB1AC"],
  ["Paid Subscription", "#24693D"],
  ["On-Demand Streaming (Ad-Supported)", "#398949"],
  ["Other Ad-Supported Streaming", "#61AA57"],
  ["SoundExchange Distributions", "#7DC470"],
  ["Limited Tier Paid Subscription", "#B4E0A7"]
])
)}

function _series(d3,colors,data){return(
d3.stack()
    .keys(colors.keys())
    .value((group, key) => group.get(key).value)
    .order(d3.stackOrderReverse)
  (d3.rollup(data, ([d]) => d, d => d.year, d => d.name).values())
    .map(s => (s.forEach(d => d.data = d.data.get(s.key)), s))
)}

function _x(d3,data,margin,width){return(
d3.scaleBand()
    .domain(data.map(d => d.year))
    .rangeRound([margin.left, width - margin.right])
)}

function _y(d3,series,height,margin){return(
d3.scaleLinear()
    .domain([0, d3.max(series, d => d3.max(d, d => d[1]))]).nice()
    .range([height - margin.bottom, margin.top])
)}

function _color(d3,colors){return(
d3.scaleOrdinal()
    .domain(colors.keys())
    .range(colors.values())
)}

function _xAxis(height,margin,d3,x,width){return(
g => g
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x)
        .tickValues(d3.ticks(...d3.extent(x.domain()), width / 80))
        .tickSizeOuter(0))
)}

function _yAxis(margin,d3,y,data){return(
g => g
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y)
        .tickFormat(x => (x / 1e9).toFixed(0)))
    .call(g => g.select(".domain").remove())
    .call(g => g.select(".tick:last-of-type text").clone()
        .attr("x", 3)
        .attr("text-anchor", "start")
        .attr("font-weight", "bold")
        .text(data.y))
)}

function _formatRevenue(){return(
x => (+(x / 1e9).toFixed(2) >= 1) 
    ? `${(x / 1e9).toFixed(2)}B` 
    : `${(x / 1e6).toFixed(0)}M`
)}

function _height(){return(
500
)}

function _margin(){return(
{top: 20, right: 30, bottom: 30, left: 30}
)}

function _d3(require){return(
require("d3@6")
)}

export default function define(runtime, observer) {
  const main = runtime.module();
  function toString() { return this.url; }
  const fileAttachments = new Map([
    ["music.csv", {url: new URL("./files/data.csv", import.meta.url), mimeType: "text/csv", toString}]
  ]);
  main.builtin("FileAttachment", runtime.fileAttachments(name => fileAttachments.get(name)));
  main.variable(observer()).define(["md"], _1);
  main.variable(observer("legend")).define("legend", ["swatches","color","margin"], _legend);
  main.variable(observer("chart")).define("chart", ["d3","width","height","series","color","x","y","formatRevenue","xAxis","yAxis"], _chart);
  main.variable(observer("data")).define("data", ["d3","FileAttachment"], _data);
  main.variable(observer("colors")).define("colors", _colors);
  main.variable(observer("series")).define("series", ["d3","colors","data"], _series);
  main.variable(observer("x")).define("x", ["d3","data","margin","width"], _x);
  main.variable(observer("y")).define("y", ["d3","series","height","margin"], _y);
  main.variable(observer("color")).define("color", ["d3","colors"], _color);
  main.variable(observer("xAxis")).define("xAxis", ["height","margin","d3","x","width"], _xAxis);
  main.variable(observer("yAxis")).define("yAxis", ["margin","d3","y","data"], _yAxis);
  main.variable(observer("formatRevenue")).define("formatRevenue", _formatRevenue);
  main.variable(observer("height")).define("height", _height);
  main.variable(observer("margin")).define("margin", _margin);
  main.variable(observer("d3")).define("d3", ["require"], _d3);
  const child1 = runtime.module(define1);
  main.import("swatches", child1);
  return main;
}
