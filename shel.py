import os
import numpy as np
import pandas as pd
from importt import make_query
import os.path
import sys

sqlpath = "/home/yerzh/comp1/queries/join-order-benchmark/"

ls1 = [64]
ls2 = [0.0001]
ls3 = [0.1]
ls4 = [100]
ls5 = [1, 10000, 1000000]


print("Hello!")
onlyfiles = [f for f in os.listdir(sqlpath) if os.path.isfile(os.path.join(sqlpath, f))]
onlyfiles.sort()

if len(sys.argv) > 1:
    onlyfiles = sys.argv[1:]
    
for filename in onlyfiles:

    f = open(sqlpath + filename, "r")
    print("Use file", sqlpath + filename)
    query = f.read()
    query = "EXPLAIN (ANALYZE ON, VERBOSE ON, FORMAT JSON) " + query
    f.close()
    for j in ls1:
        for k in ls2:
            for l in ls3:
                for n in ls4:
                    for t in ls5:
                        if os.path.isfile("/home/yerzh/comp1/new/"+filename+"/res/width="+str(j)+"_lr="+str(k)+"_slope="+str(l)+"_iter_obj="+str(n)+"_seed="+str(t)+".csv"):
                            continue
                        list1 = []
                        list2 = []

                        os.system("clear")
                        print(filename)
                        os.system("rm -rf /home/yerzh/sandbox/postgres/contrib/aqo")

                        os.system("cp -R /home/yerzh/Downloads/aqo /home/yerzh/sandbox/postgres/contrib")

                        os.system("sed -i -e 's/{}/{}/g' /home/yerzh/sandbox/postgres/contrib/aqo/aqo.h".format("WIDTH_1 (100)", "WIDTH_1 ("+str(j)+")"))

                        os.system("sed -i -e 's/{}/{}/g' /home/yerzh/sandbox/postgres/contrib/aqo/aqo.h".format("WIDTH_2 (100)", "WIDTH_2 ("+str(j)+")"))

                        os.system("sed -i -e 's/{}/{}/g' /home/yerzh/sandbox/postgres/contrib/aqo/aqo.h".format("lr (0.0001)", "lr ("+str(k)+")"))

                        os.system("sed -i -e 's/{}/{}/g' /home/yerzh/sandbox/postgres/contrib/aqo/aqo.h".format("slope (0.01)", "slope ("+str(l)+")"))

                        os.system("sed -i -e 's/{}/{}/g' /home/yerzh/sandbox/postgres/contrib/aqo/aqo.h".format("N_ITERS (100)", "N_ITERS ("+str(n)+")"))

                        os.system("sed -i -e 's/{}/{}/g' /home/yerzh/sandbox/postgres/contrib/aqo/postprocessing.c".format("srand(0);", "srand ("+str(t)+");"))

                        os.system("sed -i -e 's/{}/{}/g' /home/yerzh/sandbox/postgres/contrib/aqo/postprocessing.c".format("srand(1);", "srand ("+str(t+1)+");"))

                        os.system("sed -i -e 's/{}/{}/g' /home/yerzh/sandbox/postgres/contrib/aqo/cardinality_estimation.c".format("srand(1);", "srand ("+str(t+1)+");"))

                        os.system("pg_ctl -D $HOME/pg12data/data/ -l logfile stop")

                        os.system("cd /home/yerzh/sandbox/postgres/contrib/aqo && make | tail && make install | tail")
                        os.system("pg_ctl -D $HOME/pg12data/data/ -l logfile start")
                        a = ls1.index(j)
                        b = ls2.index(k)
                        c = ls3.index(l)
                        d = ls4.index(n)
                        e = ls5.index(t)
                        print(str((a*(1/len(ls1))+b*(1/len(ls1))*(1/len(ls2))+c*(1/len(ls1))*(1/len(ls2))*(1/len(ls3))+d*(1/len(ls1))*(1/len(ls2))*(1/len(ls3))*(1/len(ls4))+e*(1/len(ls1))*(1/len(ls2))*(1/len(ls3))*(1/len(ls4))*(1/len(ls5)))*100)+" percent:)")
                        make_query(list1, list2, query)
                        df = pd.DataFrame(list1, columns =["#iteration", "L1 norm of errors(log) on nodes", "L2 norm of errors(log) on nodes", "planning time", "execution time"])
                        dff = pd.DataFrame(list2, columns =["#iteration", "plans"])
                        df.to_csv("/home/yerzh/comp1/new/res/"+filename.split('.')[0]+"_width="+str(j)+"_lr="+str(k)+"_slope="+str(l)+"_iter_obj="+str(n)+"_seed="+str(t)+".csv")
                        dff.to_csv("/home/yerzh/comp1/new/plans/"+filename.split('.')[0]+"_width="+str(j)+"_lr="+str(k)+"_slope="+str(l)+"_iter_obj="+str(n)+"_seed="+str(t)+".csv")
