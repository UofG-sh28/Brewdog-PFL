import json
import plotly.express as px

with open("test_data.json") as testData:
	parsed = json.load(testData)
hf = parsed["categories"]["heating_fuel"]

with open("../pfl_calculator/static/verbose.json") as labels:
	verbose = json.load(labels)

data = {"keys":["Usages"], "parents":[""], "values":[None, ]}

total_usage = 0
for fuel_type in parsed["categories"]:
	fuel_total = 0
	for sub in parsed["categories"][fuel_type]:
		data["keys"].append(verbose["fields"][str(sub)])
		data["parents"].append(verbose["categories"][str(fuel_type)])
		data["values"].append(parsed["categories"][fuel_type][sub])
		fuel_total += parsed["categories"][fuel_type][sub]

	data["keys"].append(verbose["categories"][str(fuel_type)])
	data["parents"].append("Usages")
	data["values"].append(round(fuel_total,2))
	total_usage += fuel_total

data["values"][0] = round(total_usage,2)
fig = px.sunburst(
	data,
	names="keys",
	parents="parents",
	values="values",
	branchvalues="total",
	custom_data=["keys", "values"]
	)
fig.update_traces(
    hovertemplate="<br>".join([
        "Usage: %{customdata[0]}",
        "Emissions: %{customdata[1]}",
    ])
)

print(verbose["categories"]["heating_fuel"])
fig.write_html("plotly-pie.html")
