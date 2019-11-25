import pandas as pd

df_dr = pd.read_csv("DappRadar.csv")
df_sd = pd.read_csv("StateDapps.csv")

df_dr_name = list(df_dr["Name"])
df_sd_name = list(df_sd["dappNAme"])

intersect = list(set(df_dr_name) & set(df_sd_name))
dr_pct = round(100 * len(intersect) / len(set(df_dr_name)), 2)
sd_pct = round(100 * len(intersect) / len(set(df_sd_name)), 2)

print("DR total", len(df_dr_name), "uniq across platforms", len(set(df_dr_name)))
print("SD total", len(df_sd_name), "uniq across platforms", len(set(df_sd_name)))
print("Intersection", len(intersect), "=", dr_pct, "/", sd_pct, "%")

mappings = {}
mapped = 0
unmapped = 0
for entry in intersect:
	cat_dr = set(df_dr[df_dr["Name"] == entry]["category"])
	cat_sd = set(df_sd[df_sd["dappNAme"] == entry]["category"])
	#print("> Check", entry, cat_dr, "vs.", cat_sd)
	for item_dr in cat_dr:
		for item_sd in cat_sd:
			if item_sd.lower() != item_dr.lower():
				mappings[(item_dr, item_sd)] = mappings.get((item_dr, item_sd), 0) + 1
				mapped += 1
			else:
				unmapped += 1
print(mappings)
print("Mapped", mapped, "unmapped", unmapped)

f = open("plot.dot", "w")
print("digraph mappings {", file=f)
for mappingsource, mappingtarget in mappings:
	mappingsourcex = mappingsource.replace("-", "")
	mappingtargetx = mappingtarget.replace("-", "")
	print("{} -> {} [penwidth={}];".format(mappingsourcex, mappingtargetx, int(mappings[(mappingsource, mappingtarget)] / 5) + 1), file=f)
print("}", file=f)
