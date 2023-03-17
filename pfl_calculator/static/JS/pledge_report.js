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