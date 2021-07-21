import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import chi2_contingency

# Null Hypothesis: There is no difference between species and their level of concern.
# Alternative Hypothesis: There is a difference between species and their level of concern.
# Chi-Square test will be conducted.
pd.set_option("display.max_columns", 200)
species_df = pd.read_csv(r"species_info.csv")
clean_df = species_df.dropna(subset=["conservation_status"], inplace=False)
observation_df = pd.read_csv(r"observations.csv")

# Cross-tab to analyze conservation status.
species_xtab = pd.crosstab(clean_df.category, clean_df.conservation_status)
amphibian_list = species_xtab.iloc[0]
bird_list = species_xtab.iloc[1]
fish_list = species_xtab.iloc[2]
mammal_list = species_xtab.iloc[3]
nv_plant_list = species_xtab.iloc[4]
reptile_list = species_xtab.iloc[5]
v_plant_list = species_xtab.iloc[6]

# Cross-tab to find sum of each national parks observations.
observation_xtab = pd.crosstab(observation_df.park_name, sum(observation_df.observations))

# Bar graph.
colors = ["lightcoral", "lightskyblue", "darkseagreen", "gold"]
sns.set_style("whitegrid")
axs = sns.barplot(data=species_xtab, estimator=sum, palette=colors, ci=None)
axs.set_title("Threat Level Among Endangered Species")
axs.set_xlabel("Conservation Status")
axs.set_ylabel("Number of Species")

# Title for pir chart.
def chart_title(species_list, species_name):
    species_name_list = []
    species_list = species_list.sum()
    for items in species_df.category:
        if items == species_name:
            num_replace = items.replace(items, "1")
            num_int = int(num_replace)
            species_name_list.append(num_int)
    return f"{species_name}: {species_list} out of {np.sum(species_name_list)} species are at risk."

# Pie charts.
legend_labels = ["Endangered", "In Recovery", "Species of Concern", "Threatened"]

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2)
fig.suptitle("Level of Risk Between Species")
explode_a = (0, 0, 0.05, 0)
ax1.pie(amphibian_list, autopct='%d%%', pctdistance= 1.15, colors=colors, explode=explode_a)
ax1.legend(legend_labels, loc="lower left")
ax1.axis('equal')
ax1.set_title(chart_title(amphibian_list, "Amphibian"))

explode_b = (0, 0, 0.1, 0)
ax2.pie(bird_list, autopct='%d%%', pctdistance= 1.16, startangle=345, colors=colors, explode=explode_b)
ax2.legend(legend_labels, loc="lower left")
ax2.axis('equal')
ax2.set_title(chart_title(bird_list, "Bird"))

explode_f = (0, 0, 0.05, 0.05)
ax3.pie(fish_list, autopct='%d%%', pctdistance= 1.15, startangle=-45, colors=colors, explode=explode_f)
ax3.legend(legend_labels, loc="lower left")
ax3.axis('equal')
ax3.set_title(chart_title(fish_list, "Fish"))

ax4.pie(mammal_list, autopct='%d%%', pctdistance= 1.15, startangle=330, colors=colors, explode=explode_a)
ax4.legend(legend_labels, loc="lower left")
ax4.axis('equal')
ax4.set_title(chart_title(mammal_list, "Mammal"))
plt.tight_layout()

fig = plt.figure()
ax5 = fig.add_subplot(221)
ax6 = fig.add_subplot(222)
ax7 = fig.add_subplot(212)
fig.suptitle("Level of Risk Between Species")
explode_a = (0, 0, 0.05, 0)
ax5.pie(nv_plant_list, autopct='%d%%', pctdistance= 1.15, colors=colors)
ax5.legend(legend_labels, loc="lower left")
ax5.axis('equal')
ax5.set_title(chart_title(amphibian_list, "Nonvascular Plant"))

explode_d = (0, 0.15, 0, 0)
ax6.pie(v_plant_list, autopct='%d%%', pctdistance= 1.15, colors=colors, explode=explode_d)
ax6.legend(legend_labels, loc="lower left")
ax6.axis('equal')
ax6.set_title(chart_title(v_plant_list, "Vascular Plant"))

ax7.pie(reptile_list, autopct='%d%%', pctdistance= 1.15, colors=colors)
ax7.legend(legend_labels, loc="lower left")
ax7.axis('equal')
ax7.set_title(chart_title(reptile_list, "Reptile"))
plt.tight_layout()

# Chi-Square test.
def sig_level(pval):
    if pval < 0.05:
        return(f"The p-value is {round(pval, 3)}, there is a statistical significance. The null hypothesis is rejected, while the alternative hypothesis is accepted.")
    else:
        return(f"The p-value is {round(pval, 3)}, there is no statistical significance. The null hypothesis is accepted.")

chi2, pval, dof, expected = chi2_contingency(species_xtab)

# The p-value is 0.0, there is a statistical significance. The null hypothesis is rejected, while the alternative hypothesis is accepted.
# Significance Value: 1.8909788349761653e-05.
