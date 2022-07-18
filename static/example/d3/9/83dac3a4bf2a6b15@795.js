// https://observablehq.com/@d3/dot-plot@795
import define1 from "./a33468b95d0b15b0@808.js";
import define2 from "./7a9e12f9fb3d8e06@459.js";

function _1(md){return(
md`# Dot Plot

Percentage of population by age and state. Data: [American Community Survey](/@mbostock/working-with-the-census-api)`
)}

function _order(Inputs,d3,stateage){return(
Inputs.select(["state", ...d3.union(stateage.map(d => d.age))], {label: "Order by"})
)}

function _3(Legend,chart){return(
Legend(chart.color, {title: "Age (years)"})
)}

function _chart(DotPlot,stateage,width){return(
DotPlot(stateage, {
  x: d => d.population,
  y: d => d.state,
  z: d => d.age,
  xFormat: "%",
  xLabel: "Population →",
  width
})
)}

function _stateage(FileAttachment){return(
FileAttachment("us-distribution-state-age.csv").csv({typed: true})
)}

function _6(chart,d3,stateage,order){return(
chart.update(d3.groupSort(stateage, D => order === "state" ? D[0].state : -D.find(d => d.age === order).population, d => d.state))
)}

function _7(howto){return(
howto("DotPlot")
)}

function _8(altplot){return(
altplot(`Plot.plot({
    height: 660,
    grid: true,
    x: {axis: "top", percent: true, zero: true},
    y: {axis: null},
    color: {
      scheme: "spectral",
      domain: [...new Set(stateage.map(d => d.age))]
    },
    marks: [
      Plot.ruleY(stateage, Plot.groupY({x1: "min", x2: "max"}, {x: "population", y: "state"})),
      Plot.dot(stateage, {x: "population", y: "state", fill: "age"}),
      Plot.text(stateage, Plot.selectMinX({z: "state", x: "population", y: "state", textAnchor: "end", dx: -6, text: "state", sort: {y: "x", reduce: "min", reverse: true}}))
    ]
  })`)
)}

function _DotPlot(d3){return(
function DotPlot(data, {
  x = ([x]) => x, // given d in data, returns the (quantitative) value x
  y = ([, y]) => y, // given d in data, returns the (categorical) value y
  z = () => 1, // given d in data, returns the (categorical) value z
  r = 3.5, // (fixed) radius of dots, in pixels
  xFormat, // a format specifier for the x-axis
  marginTop = 30, // top margin, in pixels
  marginRight = 30, // right margin, in pixels
  marginBottom = 10, // bottom margin, in pixels
  marginLeft = 30, // left margin, in pixels
  width = 640, // outer width, in pixels
  height, // outer height, in pixels, defaults to heuristic
  xType = d3.scaleLinear, // type of x-scale
  xDomain, // [xmin, xmax]
  xRange = [marginLeft, width - marginRight], // [left, right]
  xLabel, // a label for the x-axis
  yDomain, // an array of (ordinal) y-values
  yRange, // [top, bottom]
  yPadding = 1, // separation for first and last dots from axis
  zDomain, // array of z-values
  colors, // color scheme
  stroke = "currentColor", // stroke of rule connecting dots
  strokeWidth, // stroke width of rule connecting dots
  strokeLinecap, // stroke line cap of rule connecting dots
  strokeOpacity, // stroke opacity of rule connecting dots
  duration: initialDuration = 250, // duration of transition, if any
  delay: initialDelay = (_, i) => i * 10, // delay of transition, if any
} = {}) {
  // Compute values.
  const X = d3.map(data, x);
  const Y = d3.map(data, y);
  const Z = d3.map(data, z);

  // Compute default domains, and unique them as needed.
  if (xDomain === undefined) xDomain = d3.extent(X);
  if (yDomain === undefined) yDomain = Y;
  if (zDomain === undefined) zDomain = Z;
  yDomain = new d3.InternSet(yDomain);
  zDomain = new d3.InternSet(zDomain);
  
  // Omit any data not present in the y- and z-domains.
  const I = d3.range(X.length).filter(i => yDomain.has(Y[i]) && zDomain.has(Z[i]));

  // Compute the default height.
  if (height === undefined) height = Math.ceil((yDomain.size + yPadding) * 16) + marginTop + marginBottom;
  if (yRange === undefined) yRange = [marginTop, height - marginBottom];

  // Chose a default color scheme based on cardinality.
  if (colors === undefined) colors = d3.schemeSpectral[zDomain.size];
  if (colors === undefined) colors = d3.quantize(d3.interpolateSpectral, zDomain.size);

  // Construct scales and axes.
  const xScale = xType(xDomain, xRange);
  const yScale = d3.scalePoint(yDomain, yRange).round(true).padding(yPadding);
  const color = d3.scaleOrdinal(zDomain, colors);
  const xAxis = d3.axisTop(xScale).ticks(width / 80, xFormat);

  const svg = d3.create("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [0, 0, width, height])
      .attr("style", "max-width: 100%; height: auto; height: intrinsic;");

  svg.append("g")
      .attr("transform", `translate(0,${marginTop})`)
      .call(xAxis)
      .call(g => g.select(".domain").remove())
      .call(g => g.selectAll(".tick line").clone()
          .attr("y2", height - marginTop - marginBottom)
          .attr("stroke-opacity", 0.1))
      .call(g => g.append("text")
          .attr("x", width - marginRight)
          .attr("y", -22)
          .attr("fill", "currentColor")
          .attr("text-anchor", "end")
          .text(xLabel));

  const g = svg.append("g")
      .attr("text-anchor", "end")
      .attr("font-family", "sans-serif")
      .attr("font-size", 10)
    .selectAll()
    .data(d3.group(I, i => Y[i]))
    .join("g")
      .attr("transform", ([y]) => `translate(0,${yScale(y)})`);

  g.append("line")
      .attr("stroke", stroke)
      .attr("stroke-width", strokeWidth)
      .attr("stroke-linecap", strokeLinecap)
      .attr("stroke-opacity", strokeOpacity)
      .attr("x1", ([, I]) => xScale(d3.min(I, i => X[i])))
      .attr("x2", ([, I]) => xScale(d3.max(I, i => X[i])));

  g.selectAll("circle")
    .data(([, I]) => I)
    .join("circle")
      .attr("cx", i => xScale(X[i]))
      .attr("fill", i => color(Z[i]))
      .attr("r", r);

  g.append("text")
      .attr("dy", "0.35em")
      .attr("x", ([, I]) => xScale(d3.min(I, i => X[i])) - 6)
      .text(([y]) => y);

  return Object.assign(svg.node(), {
    color,
    update(yDomain, {
      duration = initialDuration, // duration of transition
      delay = initialDelay, // delay of transition
    } = {}) {
      yScale.domain(yDomain);
      const t = g.transition().duration(duration).delay(delay);
      t.attr("transform", ([y]) => `translate(0,${yScale(y)})`);
    }
  });
}
)}

function _12(md){return(
md`The *trigger* cell below uses a timeout to change the selected value in the *order* input above, triggering an animation on page load for demonstrative purposes. If the user interacts with the menu prior to the timeout, the timeout is cleared. You don’t need this cell to use the chart above.`
)}

function _trigger($0,Event,invalidation)
{
  const input = $0.input;
  const interval = setInterval(() => {
    input.selectedIndex = (input.selectedIndex + 1) % input.length;
    input.dispatchEvent(new Event("input", {bubbles: true}));
  }, 4000);
  const clear = () => clearInterval(interval);
  input.addEventListener("change", clear, {once: true});
  invalidation.then(() => (clear(), input.removeEventListener("change", clear)));
}


export default function define(runtime, observer) {
  const main = runtime.module();
  function toString() { return this.url; }
  const fileAttachments = new Map([
    ["us-distribution-state-age.csv", {url: new URL("./files/data.csv", import.meta.url), mimeType: "text/csv", toString}]
  ]);
  main.builtin("FileAttachment", runtime.fileAttachments(name => fileAttachments.get(name)));
  main.variable(observer()).define(["md"], _1);
  main.variable(observer("viewof order")).define("viewof order", ["Inputs","d3","stateage"], _order);
  main.variable(observer("order")).define("order", ["Generators", "viewof order"], (G, _) => G.input(_));
  main.variable(observer()).define(["Legend","chart"], _3);
  main.variable(observer("chart")).define("chart", ["DotPlot","stateage","width"], _chart);
  main.variable(observer("stateage")).define("stateage", ["FileAttachment"], _stateage);
  main.variable(observer()).define(["chart","d3","stateage","order"], _6);
  // main.variable(observer()).define(["howto"], _7);
  // main.variable(observer()).define(["altplot"], _8);
  main.variable(observer("DotPlot")).define("DotPlot", ["d3"], _DotPlot);
  const child1 = runtime.module(define1);
  main.import("Legend", child1);
  const child2 = runtime.module(define2);
  main.import("howto", child2);
  main.import("altplot", child2);
  // main.variable(observer()).define(["md"], _12);
  main.variable(observer("trigger")).define("trigger", ["viewof order","Event","invalidation"], _trigger);
  return main;
}
