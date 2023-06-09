

function plot_total_pie(){
  const myDiv = this.document.getElementById("pie");

  var data = [{
    values: [pledge_savings, residual],
    labels: ['Pledged', 'Residual'],
    type: 'pie'
  }];

  var layout = {
    title: "<b>Overall Pledged Reductions</b>",
    height: 400,
    width: 500,
    paper_bgcolor:"#f6f6f6"
  };

  Plotly.newPlot(myDiv, data, layout, {displaylogo:false});
}

function plot_category_bar(){
  const myDiv = this.document.getElementById('plot');

  var pledged_x = [];
  var pledged_y = [];
  for(const key of Object.keys(cat_reductions)){
    pledged_x.push(cat_reductions[key]);
    pledged_y.push(verbose_json["categories"][key]);
  }

  var res_x = [];
  var res_y = [];
  for(const key of Object.keys(cat_emissions)){
    res_x.push(cat_emissions[key] - cat_reductions[key]);
    res_y.push(verbose_json["categories"][key]);
  }
  var residual = {
    x: res_x,
    y: res_y,
    name: 'Residual',
    orientation: 'h',
    marker: {
      color: 'rgba(55,128,191,0.6)',
      width: 1
    },
    type: 'bar'
  };

var pledged = {
  x: pledged_x,
  y: pledged_y,
  name: 'Pledged',
  orientation: 'h',
  type: 'bar',
  marker: {
    color: 'rgba(255,153,51,0.6)',
    width: 1
  }
};

var data = [residual, pledged];

var layout = {
  title: '<b>Pledged Reduction Breakdown</b>',
  barmode: 'stack',
  margin: {
    l: 200
  },
  paper_bgcolor:"#f6f6f6"
};

Plotly.newPlot(myDiv, data, layout, {displaylogo: false});
}