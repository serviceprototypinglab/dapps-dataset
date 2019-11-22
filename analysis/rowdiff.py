import pandas as pd
import os

totalchanges = {}
days = 0

evfiles = os.listdir(".")
for evfile in evfiles:
	if not evfile.endswith(".csv"):
		continue
	column = evfile.replace(".csv", "").split("-")[1]

	df = pd.read_csv(evfile)
	for idx, row in df.iterrows():
		days = len(row) - 2
		#print(idx, row)
		for i in range(1, len(row) - 1):
			if pd.isnull(row[i]):
				row[i] = "null"
			if pd.isnull(row[i + 1]):
				row[i + 1] = "null"
			if row[i] != row[i + 1]:
				if row[i] == "null" or row[i + 1] == "null":
					continue
				print("change", column, row[0], df.columns[i], "to", df.columns[i + 1], ":", row[i], "=>", row[i + 1])
				#print(type(row[i]), type(row[i + 1]), pd.isnull(row[i]), pd.isnull(row[i + 1]))
				totalchanges[column] = totalchanges.get(column, 0) + 1

dapps = 50
print("analysis over", days, "day transitions and", dapps, "dapps")
for column in totalchanges:
	print("total changes", column, totalchanges[column], "per day transition", round(totalchanges[column] / days / dapps, 2))
