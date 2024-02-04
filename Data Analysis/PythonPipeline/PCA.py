#Import Necessary Libraries
import pandas as pd
import General_Functions
import numpy as np
import Smoothing_Functions
import Frequency_Domain
from matplotlib import pyplot as plt
import Actigraph_Metrics
import random
import tsfresh
from tsfresh.utilities.dataframe_functions import impute
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.lines as mlines


#Load all 20 csv files
SBSneg1_1 = pd.read_csv(r"C:\Users\jakes\Documents\DT 6 Analysis\PatientData\Patient9Analysis\SBSneg1_num1.csv")
General_Functions.create_time_column(SBSneg1_1)
General_Functions.create_absMag_Column(SBSneg1_1)
SBSneg1_2 = pd.read_csv(r"C:\Users\jakes\Documents\DT 6 Analysis\PatientData\Patient9Analysis\SBSneg1_num2.csv")
General_Functions.create_time_column(SBSneg1_2)
General_Functions.create_absMag_Column(SBSneg1_2)
SBSneg1_3 = pd.read_csv(r"C:\Users\jakes\Documents\DT 6 Analysis\PatientData\Patient9Analysis\SBSneg1_num3.csv")
General_Functions.create_time_column(SBSneg1_3)
General_Functions.create_absMag_Column(SBSneg1_3)
SBSneg1_4 = pd.read_csv(r"C:\Users\jakes\Documents\DT 6 Analysis\PatientData\Patient9Analysis\SBSneg1_num4.csv")
General_Functions.create_time_column(SBSneg1_4)
General_Functions.create_absMag_Column(SBSneg1_4)
SBSneg1_5 = pd.read_csv(r"C:\Users\jakes\Documents\DT 6 Analysis\PatientData\Patient9Analysis\SBSneg1_num5.csv")
General_Functions.create_time_column(SBSneg1_5)
General_Functions.create_absMag_Column(SBSneg1_5)

SBS0_1 = pd.read_csv(r"C:\Users\jakes\Documents\DT 6 Analysis\PatientData\Patient9Analysis\SBS1_num1.csv")
General_Functions.create_time_column(SBS0_1)
General_Functions.create_absMag_Column(SBS0_1)
SBS0_2 = pd.read_csv(r"C:\Users\jakes\Documents\DT 6 Analysis\PatientData\Patient9Analysis\SBS1_num2.csv")
General_Functions.create_time_column(SBS0_2)
General_Functions.create_absMag_Column(SBS0_2)
SBS0_3 = pd.read_csv(r"C:\Users\jakes\Documents\DT 6 Analysis\PatientData\Patient9Analysis\SBS1_num3.csv")
General_Functions.create_time_column(SBS0_3)
General_Functions.create_absMag_Column(SBS0_3)
SBS0_4 = pd.read_csv(r"C:\Users\jakes\Documents\DT 6 Analysis\PatientData\Patient9Analysis\SBS1_num4.csv")
General_Functions.create_time_column(SBS0_4)
General_Functions.create_absMag_Column(SBS0_4)
SBS0_5 = pd.read_csv(r"C:\Users\jakes\Documents\DT 6 Analysis\PatientData\Patient9Analysis\SBS1_num5.csv")
General_Functions.create_time_column(SBS0_5)
General_Functions.create_absMag_Column(SBS0_5)

SBS1_1 = pd.read_csv(r"C:\Users\jakes\Documents\DT 6 Analysis\PatientData\Patient9Analysis\SBS1_num1.csv")
General_Functions.create_time_column(SBS1_1)
General_Functions.create_absMag_Column(SBS1_1)
SBS1_2 = pd.read_csv(r"C:\Users\jakes\Documents\DT 6 Analysis\PatientData\Patient9Analysis\SBS1_num2.csv")
General_Functions.create_time_column(SBS1_2)
General_Functions.create_absMag_Column(SBS1_2)
SBS1_3 = pd.read_csv(r"C:\Users\jakes\Documents\DT 6 Analysis\PatientData\Patient9Analysis\SBS1_num3.csv")
General_Functions.create_time_column(SBS1_3)
General_Functions.create_absMag_Column(SBS1_3)
SBS1_4 = pd.read_csv(r"C:\Users\jakes\Documents\DT 6 Analysis\PatientData\Patient9Analysis\SBS1_num4.csv")
General_Functions.create_time_column(SBS1_4)
General_Functions.create_absMag_Column(SBS1_4)
SBS1_5 = pd.read_csv(r"C:\Users\jakes\Documents\DT 6 Analysis\PatientData\Patient9Analysis\SBS1_num5.csv")
General_Functions.create_time_column(SBS1_5)
General_Functions.create_absMag_Column(SBS1_5)

SBS2_1 = pd.read_csv(r"C:\Users\jakes\Documents\DT 6 Analysis\PatientData\Patient9Analysis\SBS2_num1.csv")
General_Functions.create_time_column(SBS2_1)
General_Functions.create_absMag_Column(SBS2_1)
SBS2_2 = pd.read_csv(r"C:\Users\jakes\Documents\DT 6 Analysis\PatientData\Patient9Analysis\SBS2_num2.csv")
General_Functions.create_time_column(SBS2_2)
General_Functions.create_absMag_Column(SBS2_2)
SBS2_3 = pd.read_csv(r"C:\Users\jakes\Documents\DT 6 Analysis\PatientData\Patient9Analysis\SBS2_num3.csv")
General_Functions.create_time_column(SBS2_3)
General_Functions.create_absMag_Column(SBS2_3)
SBS2_4 = pd.read_csv(r"C:\Users\jakes\Documents\DT 6 Analysis\PatientData\Patient9Analysis\SBS2_num4.csv")
General_Functions.create_time_column(SBS2_4)
General_Functions.create_absMag_Column(SBS2_4)
SBS2_5 = pd.read_csv(r"C:\Users\jakes\Documents\DT 6 Analysis\PatientData\Patient9Analysis\SBS2_num5.csv")
General_Functions.create_time_column(SBS2_5)
General_Functions.create_absMag_Column(SBS2_5)

#Feature Extraction

signal = [SBSneg1_1['VecMag'],SBSneg1_2['VecMag'],SBSneg1_3['VecMag'],SBSneg1_4['VecMag'],SBSneg1_5['VecMag'], \
         SBS0_1['VecMag'],SBS0_2['VecMag'],SBS0_3['VecMag'],SBS0_4['VecMag'],SBS0_5['VecMag'], \
         SBS1_1['VecMag'],SBS1_2['VecMag'],SBS1_3['VecMag'],SBS1_4['VecMag'],SBS1_5['VecMag'], \
         SBS2_1['VecMag'],SBS2_2['VecMag'],SBS2_3['VecMag'],SBS2_4['VecMag'],SBS2_5['VecMag']]

SBS = [-1,-1,-1,-1,-1,0,0,0,0,0,1,1,1,1,1,2,2,2,2,2]
abs_energy = []
abs_max = []
count_above_mean = []
count_below_mean = []
std = []
mean = []
number_peaks = []
sample_entropy = []
for i in signal:
    abs_energy.append(tsfresh.feature_extraction.feature_calculators.abs_energy(i))
    abs_max.append(tsfresh.feature_extraction.feature_calculators.absolute_maximum(i))
    count_above_mean.append(tsfresh.feature_extraction.feature_calculators.count_above_mean(i))
    count_below_mean.append(tsfresh.feature_extraction.feature_calculators.count_below_mean(i))
    std.append(np.std(signal))
    mean.append(np.mean(i))
    number_peaks.append(tsfresh.feature_extraction.feature_calculators.number_peaks(i, 1000))

data = {'SBS' : SBS, 'abs_energy' : abs_energy,'abs_max' : abs_max,'count_above_mean' : count_above_mean,'count_below_mean' : count_below_mean,
       'std' : std,'mean' : mean,'number_peaks' : number_peaks}
df = pd.DataFrame(data)

#Normalize the data 
x = df.values
x = StandardScaler().fit_transform(x) # normalizing the features
#visualize normalized data
feat_cols = ['feature'+str(i) for i in range(x.shape[1])]
normalised_df = pd.DataFrame(x,columns=feat_cols)

#PCA
pca_actigraphy = PCA(n_components=2)
principalComponents_actigraphy = pca_actigraphy.fit_transform(x)
principal_actigraphy_Df = pd.DataFrame(data = principalComponents_actigraphy
             , columns = ['principal component 1', 'principal component 2'])
print(principal_actigraphy_Df.head(20))
print('Explained variation per principal component: {}'.format(pca_actigraphy.explained_variance_ratio_))

#Plot PCA
plt.figure(figsize=(12,12))
plt.figure(figsize=(12,12))
plt.xlabel('Principal Component - 1',fontsize=20)
plt.ylabel('Principal Component - 2',fontsize=20)
plt.title("Principal Component Analysis of Actigraphy and SBS",fontsize=20)
targets = ['SBS -1', 'SBS 0','SBS  1','SBS 2']
for i in range(len(signal)):
    if df['SBS'][i] == -1:
        color = 'purple'
    if df['SBS'][i] == 0:
        color = 'blue'
    if df['SBS'][i] == 1:
        color = 'orange'
    if df['SBS'][i] == 2: 
        color = 'red'
    plt.scatter(principal_actigraphy_Df.loc[i, 'principal component 1'], principal_actigraphy_Df.loc[i, 'principal component 2'], c = color, s = 50)
neg1 = mlines.Line2D([], [], color='purple', marker='o', ls='', label='SBS -1')
zero = mlines.Line2D([], [], color='blue', marker='o', ls='', label='SBS 0')
one = mlines.Line2D([], [], color='orange', marker='o', ls='', label='SBS 1')
two = mlines.Line2D([], [], color='red', marker='o', ls='', label='SBS 2')
plt.legend(handles=[neg1, zero, one, two])
plt.show()