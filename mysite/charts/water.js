chart = {
  const svg = d3.select(DOM.svg(width, height));
  
  var color = ["#23BF00", "#23BF00", "#23BF00", "#23BF00", "#23BF00", "#23BF00", "#23BF00", "#23BF00", "#23BF00", "#23BF00", "#23BF00", "#23BF00", "#2EBE00", "#2EBE00", "#39BE00", "#39BE00", "#39BE00", "#44BE00", "#44BE00", "#44BE00", "#5BBD00", "#71BC00", "#71BC00", "#7CBC00", "#87BC00", "#87BC00", "#A7BB00", "#B2BA00", "#B50005"];
  
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
  
  svg.append("text")
        .attr("x", (width / 2))             
        .attr("y", 2 * (margin.top))
        .attr("text-anchor", "middle")  
        .style("font-size", "24px") 
        .style("text-decoration", "underline")  
        .text("Freshwater Used for different foodstuffs");
  
  svg.append("text")
    .attr("class", "x label")
    .attr("text-anchor", "end")
    .attr("x", width / 2)
    .attr("y", height)
    .style("font-size", "12px")
    .text("Food items");
  
  svg.append("text")
    .attr("class", "y label")
    .attr("text-anchor", "end")
    .attr("x", -108)
    .attr("y", 12)
    .attr("dy", "-0.25em")
    .attr("transform", "rotate(-90)")
    .style("font-size", "12px")
    .text("Freshwater Used per Serving (Thousands of Liters)");
  
  const gx = svg.append("g")
      .call(xAxis)
      .selectAll("text")
          .style("text-anchor", "end")
          .attr("dx", "-.8em")
          .attr("dy", ".15em")
          .attr("transform", function(d) {
              return "rotate(-27)"
          });
  
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

data = d3.csv("https://raw.githubusercontent.com/lugrace/treehacks19/master/classifierdemo/sust_water.csv?token=AeHYxWaDhsigvZ0XM3wYeasxLoEyTWsHks5ccocGwA%3D%3D", ({food, score}) => ({name: food, value: score}))

x = d3.scaleBand()
    .domain(data.map(d => d.name))
    .range([margin.left, width - margin.right])
    .padding(0.1)

y = d3.scaleLinear()
.domain([0, d3.max(data, d => d.value)]).nice()
.range([height - 2 * margin.bottom, margin.top])

xAxis = g => g
    .attr("transform", `translate(0,${height - 2 * margin.bottom})`)
    .call(d3.axisBottom(x).tickSizeOuter(0))

yAxis = g => g
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y))
    .call(g => g.select(".domain").remove())

height = 500

margin = ({top: 20, right: 0, bottom: 30, left: 40})

d3 = require("d3@5")