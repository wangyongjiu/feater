// https://observablehq.com/@d3/grouped-bar-chart@432
import define1 from "./a33468b95d0b15b0@808.js";
import define2 from "./7a9e12f9fb3d8e06@459.js";

function _1(md){return(
md`# Grouped Bar Chart

Compare to a [stacked bar chart](/@d3/stacked-bar-chart). Data: [American Community Survey](/@mbostock/working-with-the-census-api)`
)}

function _key(Legend,chart){return(
Legend(chart.scales.color, {title: "Age (years)"})
)}

function _chart(GroupedBarChart,stateages,d3,ages,width){return(
GroupedBarChart(stateages, {
  x: d => d.state,
  y: d => d.population / 1e6,
  z: d => d.age,
  xDomain: d3.groupSort(stateages, D => d3.sum(D, d => -d.population), d => d.state).slice(0, 6), // top 6
  yLabel: "↑ Population (millions)",
  zDomain: ages,
  colors: d3.schemeSpectral[ages.length],
  width,
  height: 500
})
)}

function _states(FileAttachment){return(
FileAttachment("us-population-state-age.csv").csv({typed: true})
)}

function _ages(states){return(
states.columns.slice(1)
)}

function _stateages(ages,states){return(
ages.flatMap(age => states.map(d => ({state: d.name, age, population: d[age]})))
)}

function _7(howto){return(
howto("GroupedBarChart")
)}

function _8(altplot){return(
altplot(`Plot.plot({
  x: {axis: null, domain: ages},
  y: {tickFormat: "s"},
  color: {scheme: "spectral", domain: ages},
  facet: {data: stateages, x: "state"},
  marks: [
    Plot.barY(stateages, {
      x: "age", 
      y: "population",
      title: "age",
      fill: "age", 
      sort: {fx: "y", reduce: "sum", limit: 6, reverse: true}
    }),
    Plot.ruleY([0])
  ]
})`)
)}

function _GroupedBarChart(d3){return(
function GroupedBarChart(data, {
  x = (d, i) => i, // given d in data, returns the (ordinal) x-value
  y = d => d, // given d in data, returns the (quantitative) y-value
  z = () => 1, // given d in data, returns the (categorical) z-value
  title, // given d in data, returns the title text
  marginTop = 30, // top margin, in pixels
  marginRight = 0, // right margin, in pixels
  marginBottom = 30, // bottom margin, in pixels
  marginLeft = 40, // left margin, in pixels
  width = 640, // outer width, in pixels
  height = 400, // outer height, in pixels
  xDomain, // array of x-values
  xRange = [marginLeft, width - marginRight], // [xmin, xmax]
  xPadding = 0.1, // amount of x-range to reserve to separate groups
  yType = d3.scaleLinear, // type of y-scale
  yDomain, // [ymin, ymax]
  yRange = [height - marginBottom, marginTop], // [ymin, ymax]
  zDomain, // array of z-values
  zPadding = 0.05, // amount of x-range to reserve to separate bars
  yFormat, // a format specifier string for the y-axis
  yLabel, // a label for the y-axis
  colors = d3.schemeTableau10, // array of colors
} = {}) {
  // Compute values.
  const X = d3.map(data, x);
  const Y = d3.map(data, y);
  const Z = d3.map(data, z);

  // Compute default domains, and unique the x- and z-domains.
  if (xDomain === undefined) xDomain = X;
  if (yDomain === undefined) yDomain = [0, d3.max(Y)];
  if (zDomain === undefined) zDomain = Z;
  xDomain = new d3.InternSet(xDomain);
  zDomain = new d3.InternSet(zDomain);

  // Omit any data not present in both the x- and z-domain.
  const I = d3.range(X.length).filter(i => xDomain.has(X[i]) && zDomain.has(Z[i]));

  // Construct scales, axes, and formats.
  const xScale = d3.scaleBand(xDomain, xRange).paddingInner(xPadding);
  const xzScale = d3.scaleBand(zDomain, [0, xScale.bandwidth()]).padding(zPadding);
  const yScale = yType(yDomain, yRange);
  const zScale = d3.scaleOrdinal(zDomain, colors);
  const xAxis = d3.axisBottom(xScale).tickSizeOuter(0);
  const yAxis = d3.axisLeft(yScale).ticks(height / 60, yFormat);

  // Compute titles.
  if (title === undefined) {
    const formatValue = yScale.tickFormat(100, yFormat);
    title = i => `${X[i]}\n${Z[i]}\n${formatValue(Y[i])}`;
  } else {
    const O = d3.map(data, d => d);
    const T = title;
    title = i => T(O[i], i, data);
  }

  const svg = d3.create("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [0, 0, width, height])
      .attr("style", "max-width: 100%; height: auto; height: intrinsic;");

  svg.append("g")
      .attr("transform", `translate(${marginLeft},0)`)
      .call(yAxis)
      .call(g => g.select(".domain").remove())
      .call(g => g.selectAll(".tick line").clone()
          .attr("x2", width - marginLeft - marginRight)
          .attr("stroke-opacity", 0.1))
      .call(g => g.append("text")
          .attr("x", -marginLeft)
          .attr("y", 10)
          .attr("fill", "currentColor")
          .attr("text-anchor", "start")
          .text(yLabel));

  const bar = svg.append("g")
    .selectAll("rect")
    .data(I)
    .join("rect")
      .attr("x", i => xScale(X[i]) + xzScale(Z[i]))
      .attr("y", i => yScale(Y[i]))
      .attr("width", xzScale.bandwidth())
      .attr("height", i => yScale(0) - yScale(Y[i]))
      .attr("fill", i => zScale(Z[i]));

  if (title) bar.append("title")
      .text(title);

  svg.append("g")
      .attr("transform", `translate(0,${height - marginBottom})`)
      .call(xAxis);

  return Object.assign(svg.node(), {scales: {color: zScale}});
}
)}

export default function define(runtime, observer) {
  const main = runtime.module();
  function toString() { return this.url; }
  const fileAttachments = new Map([
    ["us-population-state-age.csv", {url: new URL("./files/81d7bd5e9551f005d7a4764e2dcb46c44f04b5918551ce19dba191a8799b498beddb5ef2da994047586fc7231749e8911c825b1967f22814a57bee58c590c86e.csv", import.meta.url), mimeType: "text/csv", toString}]
  ]);
  main.builtin("FileAttachment", runtime.fileAttachments(name => fileAttachments.get(name)));
  main.variable(observer()).define(["md"], _1);
  main.variable(observer("key")).define("key", ["Legend","chart"], _key);
  main.variable(observer("chart")).define("chart", ["GroupedBarChart","stateages","d3","ages","width"], _chart);
  main.variable(observer("states")).define("states", ["FileAttachment"], _states);
  main.variable(observer("ages")).define("ages", ["states"], _ages);
  main.variable(observer("stateages")).define("stateages", ["ages","states"], _stateages);
  main.variable(observer()).define(["howto"], _7);
  main.variable(observer()).define(["altplot"], _8);
  main.variable(observer("GroupedBarChart")).define("GroupedBarChart", ["d3"], _GroupedBarChart);
  const child1 = runtime.module(define1);
  main.import("Legend", child1);
  main.import("Swatches", child1);
  const child2 = runtime.module(define2);
  main.import("howto", child2);
  main.import("altplot", child2);
  return main;
}
