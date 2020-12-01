import numpy as np
import pandas as pd

df = pd.read_csv('/home/yerzh/comp1/results.csv')
dic={}
for j, i in df.iterrows():
    dic[i['seeds']]=[i['#iter_card_est_converged'], i['L1'], i['L2'], i['planning time'], i['execution time'], i['#iter_plan_converged'], i['total_exec_time']]
ls1 = [16, 32]
ls2 = [0.00001, 0.0000316227, 0.0001, 0.00031622]
ls3 = [0.05, 0.1, 0.18]
ls4 = [50, 100, 150]
ls5 = [1, 10000, 1000000]
ls = []
for j in ls1:
    for k in ls2:
        for l in ls3:
            for n in ls4:
                ls.append(["width="+str(j)+"_lr="+str(k)+"_slope="+str(l)+"_iter_obj="+str(n), \
                          [dic["width="+str(j)+"_lr="+str(k)+"_slope="+str(l)+"_iter_obj="+str(n)+"_seed=1.csv"][0],\
                           dic["width="+str(j)+"_lr="+str(k)+"_slope="+str(l)+"_iter_obj="+str(n)+"_seed=10000.csv"][0],\
                           dic["width="+str(j)+"_lr="+str(k)+"_slope="+str(l)+"_iter_obj="+str(n)+"_seed=1000000.csv"][0]],\
                          [dic["width="+str(j)+"_lr="+str(k)+"_slope="+str(l)+"_iter_obj="+str(n)+"_seed=1.csv"][1],\
                           dic["width="+str(j)+"_lr="+str(k)+"_slope="+str(l)+"_iter_obj="+str(n)+"_seed=10000.csv"][1],\
                           dic["width="+str(j)+"_lr="+str(k)+"_slope="+str(l)+"_iter_obj="+str(n)+"_seed=1000000.csv"][1]],\
                           [dic["width="+str(j)+"_lr="+str(k)+"_slope="+str(l)+"_iter_obj="+str(n)+"_seed=1.csv"][2],\
                           dic["width="+str(j)+"_lr="+str(k)+"_slope="+str(l)+"_iter_obj="+str(n)+"_seed=10000.csv"][2],\
                           dic["width="+str(j)+"_lr="+str(k)+"_slope="+str(l)+"_iter_obj="+str(n)+"_seed=1000000.csv"][2]],\
                           [dic["width="+str(j)+"_lr="+str(k)+"_slope="+str(l)+"_iter_obj="+str(n)+"_seed=1.csv"][3],\
                           dic["width="+str(j)+"_lr="+str(k)+"_slope="+str(l)+"_iter_obj="+str(n)+"_seed=10000.csv"][3],\
                           dic["width="+str(j)+"_lr="+str(k)+"_slope="+str(l)+"_iter_obj="+str(n)+"_seed=1000000.csv"][3]],\
                           [dic["width="+str(j)+"_lr="+str(k)+"_slope="+str(l)+"_iter_obj="+str(n)+"_seed=1.csv"][4],\
                           dic["width="+str(j)+"_lr="+str(k)+"_slope="+str(l)+"_iter_obj="+str(n)+"_seed=10000.csv"][4],\
                           dic["width="+str(j)+"_lr="+str(k)+"_slope="+str(l)+"_iter_obj="+str(n)+"_seed=1000000.csv"][4]],\
                           [dic["width="+str(j)+"_lr="+str(k)+"_slope="+str(l)+"_iter_obj="+str(n)+"_seed=1.csv"][5],\
                           dic["width="+str(j)+"_lr="+str(k)+"_slope="+str(l)+"_iter_obj="+str(n)+"_seed=10000.csv"][5],\
                           dic["width="+str(j)+"_lr="+str(k)+"_slope="+str(l)+"_iter_obj="+str(n)+"_seed=1000000.csv"][5]],\
                           [dic["width="+str(j)+"_lr="+str(k)+"_slope="+str(l)+"_iter_obj="+str(n)+"_seed=1.csv"][6],\
                           dic["width="+str(j)+"_lr="+str(k)+"_slope="+str(l)+"_iter_obj="+str(n)+"_seed=10000.csv"][6],\
                           dic["width="+str(j)+"_lr="+str(k)+"_slope="+str(l)+"_iter_obj="+str(n)+"_seed=1000000.csv"][6]],\
                           ])

dff = pd.DataFrame(ls,columns=['hypers','#iter_card_est_converged', 'L1', 'L2', 'planning time', 'execution time', '#iter_plan_converged', 'total_exec_time'])
lsss=[]
for j, i in dff.iterrows():
    ind = np.where(np.median(i['#iter_plan_converged'])==i['#iter_plan_converged'])[0][0]
    lsss.append([i['hypers'], i['#iter_card_est_converged'][ind], i['L1'][ind], i['L2'][ind],\
                i['planning time'][ind], i['execution time'][ind], i['#iter_plan_converged'][ind],\
                i['total_exec_time'][ind]])
dfff = pd.DataFrame(lsss,columns=['hypers','#iter_card_est_converged', 'L1', 'L2', 'planning time', 'execution time', '#iter_plan_converged', 'total_exec_time'])
dfff['#iter_plan_converged'] = dfff['#iter_plan_converged'].astype('float')
dfff = dfff.sort_values(by=['#iter_plan_converged'])
dfff.to_csv('/home/yerzh/comp1/ress.csv', index=False)

