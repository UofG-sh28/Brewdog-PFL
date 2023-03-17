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



function plot_pie(){
    const plot = this.document.getElementById("plot");

    var data = [{

    }]
}