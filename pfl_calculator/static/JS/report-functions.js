
//error check json data
function getParentsAndSubtotals(labels){
  let parents = [""];
  var cat_totals = {};

  if(cat){
    for(key in category_json){
      cat_totals[key] = 0;
    }
    for(var i=0; i < labels.length; i++){
      for(category in category_json){
        if(category_json[category].includes(labels[i])){
          parents.push(category);
          cat_totals[category] += json_data[labels[i]];
          break;
        }
      }
    }
  }else{
    for(key in scope_json){
      cat_totals[key] = 0;
    }
    for(var i=0;i<labels.length;i++){
      found = false;
      for(scope in scope_json){
        if(scope_json[scope].includes(labels[i])){
          parents.push(scope);
          cat_totals[scope] += json_data[labels[i]];
          found = true;
          break;
        }
      }
    }
  }
  return [parents, cat_totals];
}


function plot_sunburst(){
  try{
    const element = document.getElementById('plot');
    let labelArr = ["Usages"];
    let valueArr = [null];
    let total_emissions = 0
    //labelArr = "Usages" + keys in json_data + categories/scopes
    //valueArr = total + corresponding emissions + category/scope total emissions
    //parentArr = "" + corresponding parents + "Usages" for all categories/scopes
    for(key in json_data){
      labelArr.push(key);
      let val = json_data[key];
      valueArr.push(val);
      total_emissions += val;
    }

    const [parentArr, subtotals]= getParentsAndSubtotals(labelArr.slice(1));

    for(cat in subtotals){
      labelArr.push(cat);
      parentArr.push("Usages");
      valueArr.push(subtotals[cat]);
    }
    console.log("before");
    console.log(labelArr);
    console.log(parentArr);
    for(let i=0; i < labelArr.length; i++){
      var label = labelArr[i];
      if(Object.keys(verbose_json["fields"]).includes(label)){
        labelArr[i] = verbose_json["fields"][label];
      }
      else if(Object.keys(verbose_json["categories"]).includes(label)){
        labelArr[i] = verbose_json["categories"][label];
      }
    }

    for(let i=0; i < parentArr.length; i++){
      if(Object.keys(verbose_json["categories"]).includes(parentArr[i])){
        parentArr[i] = verbose_json["categories"][parentArr[i]];
      }
    }
    console.log("after");
    console.log(labelArr);
    console.log(parentArr);
    valueArr[0] = total_emissions;
    var data = [{
      type: "sunburst",
      labels: labelArr,
      parents: parentArr,
      values: valueArr,
      "branchvalues": 'total',
      leaf: {opacity: 0.4},
      marker: {line: {width: 2}},
    }];

    var layout = {
      margin: {l: 0, r: 0, b: 0, t: 0},
      width: 500,
      height: 500,
      paper_bgcolor:"#f6f6f6"

    };
    Plotly.newPlot(element, data, layout, {displaylogo: false});
    return 1;
  }
  catch{
    return 0;
  }
}

function updateTable(cat) {
  if (cat == 1){
    table_show = document.getElementById("summary-table-category");
    table_hide = document.getElementById("summary-table-scope");
    table_show.style.display = "inline";
    table_hide.style.display = "none";
  } else if (cat == 0) {
    table_show = document.getElementById("summary-table-scope");
    table_hide = document.getElementById("summary-table-category");
    table_show.style.display = "inline";
    table_hide.style.display = "none";
  }
}

function switchGrouping(){
  //is category selected?
  const e = document.getElementById("cat_switch");
  if(e.value == "category"){
    cat = 1;
    updateTable(cat);
  }
  else{
    cat = 0;
    updateTable(cat);
    generateSubTable("scope1");
  }
  plot_sunburst();
}

function generateSubTable(subcat){
  const e = document.getElementById('cat_switch');
  var dict;
  if(e.value == "category"){
    dict = category_json[subcat];
  }else{
    dict = scope_json[subcat];
  }
  const table = document.getElementById("subcategories");
  for(let i=table.rows.length-1;i>0;i--){//clear all but header row
    table.deleteRow(i);
  }
  const head = document.getElementById("subCatHead");
  var verbose_fields = verbose_json["fields"];
  head.innerHTML = verbose_json["categories"][subcat];;
  let total_emissions = 0;
  for(let i=0; i <dict.length; i++){
    total_emissions += json_data[dict[i]];
  }

  for(let i=0; i <dict.length; i++){
    var row = table.insertRow();
    var cell0 = row.insertCell();
    var cell1 = row.insertCell();
    var cell2 = row.insertCell()
    cell0.innerHTML = verbose_fields[dict[i]];
    cell1.innerHTML = json_data[dict[i]];
    cell2.innerHTML = Math.round(json_data[dict[i]]/total_emissions*10000)/100;
  }
  var row = table.insertRow();
  var cell0 = row.insertCell();
  var cell1 = row.insertCell();
  var cell2 = row.insertCell();
  cell0.innerHTML = "Totals";
  cell1.innerHTML = Math.round(total_emissions *100)/100;
  cell2.innerHTML = "100";
  row.style.fontWeight = "bold";
  row.style.backgroundColor = "#fbfbg6";  // Find a <table> element with id="myTable":

  // Create an empty <tr> element and add it to the 1st position of the table:
}

function subRadioClick(field){
  console.log(field.id);
  generateSubTable(field.id);
}