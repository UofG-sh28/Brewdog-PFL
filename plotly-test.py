import json
import plotly.express as px

with open("test_data.json") as testData:
	parsed = json.load(testData)
hf = parsed["categories"]["heating_fuel"]

data = {"keys":["Usages"], "parents":[""], "values":[None, ]}

total_usage = 0
for fuel_type in parsed["categories"]:
	fuel_total = 0
	for sub in parsed["categories"][fuel_type]:
		data["keys"].append(sub)
		data["parents"].append(fuel_type)
		data["values"].append(parsed["categories"][fuel_type][sub])
		fuel_total += parsed["categories"][fuel_type][sub]

	data["keys"].append(fuel_type)
	data["parents"].append("Usages")
	data["values"].append(fuel_total)
	total_usage += fuel_total

data["values"][0] = total_usage
fig = px.sunburst(
	data,
	names="keys",
	parents="parents",
	values="values",
	branchvalues="total"
	)

fig.show()
