import json
import os
import psycopg2
import subprocess
import sys
import pandas as pd
import re
import numpy as np

sqlpath = "/home/yerzh/comp1/new/10a.sql/res/"
sqlpath_2 = "/home/yerzh/comp1/new/10a.sql/plans/"

print("Hello!")
onlyfiles = [f for f in os.listdir(sqlpath) if os.path.isfile(os.path.join(sqlpath, f))]
onlyfiles.sort()
onlyfiles_2 = [f for f in os.listdir(sqlpath_2) if os.path.isfile(os.path.join(sqlpath_2, f))]
onlyfiles_2.sort()

ls = []


for filename in onlyfiles:
    print(filename)
    df = pd.read_csv(sqlpath+filename, index_col=0)
    for i in range(195):
        sii=0
        if abs(df.iloc[i]["L1 norm of errors(log) on nodes"]-df.iloc[i+1]["L1 norm of errors(log) on nodes"])<0.01 and abs(df.iloc[i+1]["L1 norm of errors(log) on nodes"]-df.iloc[i+2]["L1 norm of errors(log) on nodes"])<0.01 and abs(df.iloc[i+2]["L1 norm of errors(log) on nodes"]-df.iloc[i+3]["L1 norm of errors(log) on nodes"])<0.01 and abs(df.iloc[i+3]["L1 norm of errors(log) on nodes"]-df.iloc[i+4]["L1 norm of errors(log) on nodes"])<0.01 and abs(df.iloc[i]["L2 norm of errors(log) on nodes"]-df.iloc[i+1]["L2 norm of errors(log) on nodes"])<0.01 and abs(df.iloc[i+1]["L2 norm of errors(log) on nodes"]-df.iloc[i+2]["L2 norm of errors(log) on nodes"])<0.01 and abs(df.iloc[i+2]["L2 norm of errors(log) on nodes"]-df.iloc[i+3]["L2 norm of errors(log) on nodes"])<0.01 and abs(df.iloc[i+3]["L2 norm of errors(log) on nodes"]-df.iloc[i+4]["L2 norm of errors(log) on nodes"])<0.01 and df.iloc[i]["L1 norm of errors(log) on nodes"]<2 and df.iloc[i]["L2 norm of errors(log) on nodes"]<1:
            ls.append([filename, i+1, df.iloc[i]["L1 norm of errors(log) on nodes"], df.iloc[i]["L2 norm of errors(log) on nodes"], df.iloc[i]["planning time"], df.iloc[i]["execution time"]])
            sii+=1
            break
    if i==194 and sii==0:
        ls.append([filename, 'no_convergence', df.iloc[i]["L1 norm of errors(log) on nodes"], df.iloc[i]["L2 norm of errors(log) on nodes"], df.iloc[i]["planning time"], df.iloc[i]["execution time"]])

lss = []

for filename in onlyfiles_2:
    df = pd.read_csv(sqlpath_2+filename, index_col=0)
    a = " ".join(re.findall("[a-zA-Z]+", df['plans'].loc[199]))
    for i in range(198, -1, -1):
        if a != " ".join(re.findall("[a-zA-Z]+", df['plans'].loc[i])):
            s=0
            for j in range(i+1):
                s+=float(df['plans'].loc[j].split('\'Execution Time\': ', 1)[1].split('}', 1)[0])
            lss.append([i+1, s])
            break
        elif i==0:
            lss.append(['plan did not converge', 'inf'])
dff = pd.DataFrame(np.concatenate((np.array(ls),np.array(lss)), axis=1),columns=['seeds','#iter_card_est_converged', 'L1', 'L2', 'planning time', 'execution time', '#iter_plan_converged', 'total_exec_time'])

dff['total_exec_time'] = dff['total_exec_time'].astype('float')

dff = dff.sort_values(by=['total_exec_time'])

dff.to_csv("/home/yerzh/comp1/results.csv", index=False)
        
print("VSE")
