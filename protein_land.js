chart = {
  const svg = d3.select(DOM.svg(width, height));
  
  
  var color = ["#23BF00",
"#23BF00",
"#23BF00",
"#23BF00",
"#23BF00",
"#23BF00", "#2EBE00",
"#2EBE00",
"#2EBE00",
"#2EBE00","#9DBB00","#B62600","#B50005",];
  
  var bar = svg.append("g")
    .selectAll("rect")
    .data(data)
    .join("rect")
      .style("mix-blend-mode", "multiply")
      .attr("x", d => x(d.name))
      .attr("y", d => y(d.value))
      // .attr("height", d => y(0) - y(d.value))
    .attr("fill", function(d, i) {
      // i = i + 1;
      return color[i] // here it is picking up colors in sequence
    })
      .attr("width", x.bandwidth());
  
  bar = svg.append("g")
    .selectAll("rect")
    .data(data)
    .join("rect")
      .style("mix-blend-mode", "multiply").transition().delay((d, i) => i * 60)
        .attr("x", d => x(d.name))
  .duration(750)
      // .attr("x", d => x(d.name))
      .attr("y", d => y(d.value))
      .attr("height", d => y(0) - y(d.value))
    .attr("fill", function(d, i) {
      // i = i + 1;
      return color[i] // here it is picking up colors in sequence
    })
      .attr("width", x.bandwidth());

  const gx = svg.append("g")
      .call(xAxis);
  
  const gy = svg.append("g")
      .call(yAxis);

  svg.node().update = () => {
    const t = svg.transition()
        .duration(750);

    svg.data(data, d => d.name).sort((a, b) => b.value - a.value)
        .order()
      .transition(t)
        .delay((d, i) => i * 20)
        .attr("x", d => x(d.name));

    gx.transition(t)
        .call(xAxis)
      .selectAll(".tick")
        .delay((d, i) => i * 20);
  };

  return svg.node();
}


{
    data.sort((a, b) => a.value - b.value);

//   data.sort((a, b) => a.value - b.value).transition();
  x.domain(data.map(d => d.name));
  // chart.update();
}

data = d3.csv("https://raw.githubusercontent.com/lugrace/treehacks19/master/classifierdemo/sust_proteins.csv?token=AeHYxSzq6N781lGq0Wu0grJGVgBwryi2ks5cci03wA%3D%3D", ({food, score}) => ({name: food, value: score}))

x = d3.scaleBand()
    .domain(data.map(d => d.name))
    .range([margin.left, width - margin.right])
    .padding(0.1)

y = d3.scaleLinear()
.domain([0, 3*d3.max(data, d => d.value)]).nice()
.range([height - margin.bottom, margin.top])

xAxis = g => g
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x).tickSizeOuter(0))

    yAxis = g => g
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y))
    .call(g => g.select(".domain").remove())

    height = 500

    margin = ({top: 20, right: 0, bottom: 30, left: 40})

    d3 = require("d3@5")