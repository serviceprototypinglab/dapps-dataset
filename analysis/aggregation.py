import os
import pandas as pd

rootdir = ".."

dfx = {}

datadirs = os.listdir(rootdir)
print(datadirs)
for datadir in sorted(datadirs):
	datestamp = datadir[datadir.find("-") + 1:]
	csvpath = os.path.join(rootdir, datadir, "DappRadar.csv")
	if os.path.isfile(csvpath):
		df = pd.read_csv(csvpath)
		names = []
		for column in df.columns:
			if column == "Name":
				for idx, item in df[column].iteritems():
					names.append(item)
				continue
			if not column in dfx:
				dfx[column] = pd.DataFrame()
			for name, (idx, item) in zip(names, df[column].iteritems()):
				print("{:30s}".format(name), ">>", datestamp, "::", column, "==", item)
				dfx[column].ix[name, datestamp] = item

for column in dfx:
	print(dfx[column])
	dfx[column].to_csv("evolution-" + column + ".csv")
