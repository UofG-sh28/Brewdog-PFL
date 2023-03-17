function generatePledgeTable(){
  const table = document.getElementById("pledgeTable");

  console.log(json_data);
  for(let i=0; i <json_data.length; i++){
    var row = table.insertRow();
    var cell0 = row.insertCell();
    var cell1 = row.insertCell();
    console.log(json_data[i]);
    cell0.innerHTML = json_data[i];
    cell1.innerHTML = json_data[i];
  }
}



function plot_total_pie(){
  const myDiv = this.document.getElementById("pie");

  var data = [{
    values: [pledge_savings, residual],
    labels: ['Pledged', 'Residual'],
    type: 'pie'
  }];

  var layout = {
    title: "Overall Pledged Reductions",
    height: 400,
    width: 500
  };

  Plotly.newPlot(myDiv, data, layout);
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

  console.log(cat_emissions);
  console.log(cat_reductions);
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
  title: 'Pledged Reduction Breakdown',
  barmode: 'stack',
  margin: {
    l: 200
  }
};

Plotly.newPlot(myDiv, data, layout);
}