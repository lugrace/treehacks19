chart = {
  const svg = d3.select(DOM.svg(width, height));
  
  const bar = svg.append("g")
      .attr("fill", "steelblue")
    .selectAll("rect")
    .data(data)
    .join("rect")
      .style("mix-blend-mode", "multiply")
      .attr("x", d => x(d.name))
      .attr("y", d => y(d.value))
      .attr("height", d => y(0) - y(d.value))
      .attr("width", x.bandwidth());
  
  const gx = svg.append("g")
      .call(xAxis);
  
  const gy = svg.append("g")
      .call(yAxis);

  svg.node().update = () => {
    const t = svg.transition()
        .duration(750);

    bar.data(data, d => d.name)
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