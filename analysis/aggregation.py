import os
import pandas as pd

rootdir = ".."

dfx = {}
occurrences = {}

datadirs = os.listdir(rootdir)
print(datadirs)
for datadir in sorted(datadirs):
	datestamp = datadir[datadir.find("-") + 1:]
	csvpath = os.path.join(rootdir, datadir, "DappRadar.csv")
	if os.path.isfile(csvpath) and datadir.startswith("dappRadar-"):
		df = pd.read_csv(csvpath)
		names = []
		for column in df.columns:
			if column == "Name":
				for idx, item in df[column].iteritems():
					names.append(item)
					occurrences[item] = occurrences.get(item, 0) + 1
				continue
			if not column in dfx:
				dfx[column] = pd.DataFrame()
			for name, (idx, item) in zip(names, df[column].iteritems()):
				print("{:30s}".format(name), ">>", datestamp, "::", column, "==", item)
				dfx[column].ix[name, datestamp] = item

for column in dfx:
	print(dfx[column])
	dfx[column].to_csv("evolution-" + column + ".csv")

sum_occ = sum([occurrences[x] for x in occurrences])
print("Occurrences", len(occurrences), "dapps", sum_occ, "total")
eq_1 = 0
lt_7 = 0
lt_14 = 0
lt_21 = 0
lt_28 = 0
for name in occurrences:
	if occurrences[name] == 1:
		eq_1 += 1
	elif occurrences[name] < 7:
		lt_7 += 1
	elif occurrences[name] < 14:
		lt_14 += 1
	elif occurrences[name] < 21:
		lt_21 += 1
	else:
		lt_28 += 1
print("==1", eq_1, "<7", lt_7, "<14", lt_14, "<21", lt_21, "<28", lt_28)
