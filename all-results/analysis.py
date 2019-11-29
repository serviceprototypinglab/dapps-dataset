import pandas as pd
import os

threeway = False

df_dr = pd.read_csv("DappRadar.csv")
df_sd = pd.read_csv("StateDapps.csv")
df_dc = pd.read_csv("dappcomall.csv")

df_dr_name = list(df_dr["Name"])
df_sd_name = list(df_sd["dappNAme"])
df_dc_name = list(df_dc["names"])

print("DR [dappradar.com       ] total", len(df_dr_name), "uniq across platforms", len(set(df_dr_name)))
print("SD [stateoffthedapps.com] total", len(df_sd_name), "uniq across platforms", len(set(df_sd_name)))
print("DC [dapp.com            ] total", len(df_dc_name), "uniq across platforms", len(set(df_dc_name)))

intersect_drsd = list(set(df_dr_name) & set(df_sd_name))
intersect_drdc = list(set(df_dr_name) & set(df_dc_name))
intersect_sddc = list(set(df_sd_name) & set(df_dc_name))

dr_pct_drsd = round(100 * len(intersect_drsd) / len(set(df_dr_name)), 2)
sd_pct_drsd = round(100 * len(intersect_drsd) / len(set(df_sd_name)), 2)
dr_pct_drdc = round(100 * len(intersect_drdc) / len(set(df_dr_name)), 2)
dc_pct_drdc = round(100 * len(intersect_drdc) / len(set(df_dc_name)), 2)
sd_pct_sddc = round(100 * len(intersect_sddc) / len(set(df_sd_name)), 2)
dc_pct_sddc = round(100 * len(intersect_sddc) / len(set(df_dc_name)), 2)

print("Intersection DR/SD", len(intersect_drsd), "=", dr_pct_drsd, "/", sd_pct_drsd, "%")
print("Intersection DR/DC", len(intersect_drdc), "=", dr_pct_drdc, "/", dc_pct_drdc, "%")
print("Intersection SD/DC", len(intersect_sddc), "=", sd_pct_sddc, "/", dc_pct_sddc, "%")

mappings_drsd = {}
mapped_drsd = 0
unmapped_drsd = 0
for entry in intersect_drsd:
	cat_dr = set(df_dr[df_dr["Name"] == entry]["category"])
	cat_sd = set(df_sd[df_sd["dappNAme"] == entry]["category"])
	#print("> Check", entry, cat_dr, "vs.", cat_sd)
	for item_dr in cat_dr:
		for item_sd in cat_sd:
			if item_dr.lower() != item_sd.lower():
				mappings_drsd[(item_dr, item_sd)] = mappings_drsd.get((item_dr, item_sd), 0) + 1
				mapped_drsd += 1
			else:
				unmapped_drsd += 1
print(mappings_drsd)
print("Mapped DR/SD", mapped_drsd, "unmapped/samecategory DR/SD", unmapped_drsd)

mappings_sddc = {}
mapped_sddc = 0
unmapped_sddc = 0
for entry in intersect_sddc:
	cat_sd = set(df_sd[df_sd["dappNAme"] == entry]["category"])
	cat_dc = set(df_dc[df_dc["names"] == entry]["cats"])
	#print("> Check", entry, cat_sd, "vs.", cat_dc)
	for item_sd in cat_sd:
		for item_dc in cat_dc:
			if item_sd.lower() != item_dc.lower():
				mappings_sddc[(item_sd, item_dc)] = mappings_sddc.get((item_sd, item_dc), 0) + 1
				mapped_sddc += 1
			else:
				unmapped_sddc += 1
print(mappings_sddc)
print("Mapped SD/DC", mapped_sddc, "unmapped/samecategory SD/DC", unmapped_sddc)

if threeway:
	mappings_dcdr = {}
	mapped_dcdr = 0
	unmapped_dcdr = 0
	for entry in intersect_drdc:
		cat_dc = set(df_dc[df_dc["names"] == entry]["cats"])
		cat_dr = set(df_dr[df_dr["Name"] == entry]["category"])
		#print("> Check", entry, cat_dc, "vs.", cat_dr)
		for item_dc in cat_dc:
			for item_dr in cat_dr:
				if item_dc.lower() != item_dr.lower():
					mappings_dcdr[(item_dc, item_dr)] = mappings_dcdr.get((item_dc, item_dr), 0) + 1
					mapped_dcdr += 1
				else:
					unmapped_dcdr += 1
	print(mappings_dcdr)
	print("Mapped DC/DR", mapped_dcdr, "unmapped/samecategory DC/DR", unmapped_dcdr)

f = open("plot.dot", "w")
print("digraph mappings {", file=f)
for mappingsource, mappingtarget in mappings_sddc:
	mappingsourcex = mappingsource.replace("-", "").replace(" ", "")
	mappingtargetx = mappingtarget.replace("-", "").replace(" ", "")
	print("{} -> {} [penwidth={}];".format(mappingsourcex, mappingtargetx, int(mappings_sddc[(mappingsource, mappingtarget)] / 5) + 1), file=f)
	print("{} [color=\"#6060b0\",style=filled,label=\"{}\",fontsize=22];".format(mappingsourcex, mappingsource), file=f)
	print("{} [color=\"#90ff90\",style=filled,label=\"{}\",fontsize=22];".format(mappingtargetx, mappingtarget), file=f)
for mappingsource, mappingtarget in mappings_drsd:
	mappingsourcex = mappingsource.replace("-", "").replace(" ", "")
	mappingtargetx = mappingtarget.replace("-", "").replace(" ", "")
	print("{} -> {} [penwidth={}];".format(mappingsourcex, mappingtargetx, int(mappings_drsd[(mappingsource, mappingtarget)] / 5) + 1), file=f)
	print("{} [color=\"#ff9090\",style=filled,label=\"{}\",fontsize=22];".format(mappingsourcex, mappingsource), file=f)
	print("{} [color=\"#9090ff\",style=filled,label=\"{}\",fontsize=22];".format(mappingtargetx, mappingtarget), file=f)
if threeway:
	for mappingsource, mappingtarget in mappings_dcdr:
		mappingsourcex = mappingsource.replace("-", "").replace(" ", "")
		mappingtargetx = mappingtarget.replace("-", "").replace(" ", "")
		print("{} -> {} [penwidth={}];".format(mappingsourcex, mappingtargetx, int(mappings_dcdr[(mappingsource, mappingtarget)] / 5) + 1), file=f)
		#print("{} [color=\"#ff2020\",style=filled,label=\"{}\",fontsize=22];".format(mappingsourcex, mappingsource), file=f)
		#print("{} [color=\"#2020ff\",style=filled,label=\"{}\",fontsize=22];".format(mappingtargetx, mappingtarget), file=f)
print("}", file=f)
f.close()

os.system("dot -Tpng plot.dot > plot.png")
