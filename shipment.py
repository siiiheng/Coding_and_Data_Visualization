import pandas as pd
from gurobipy import Model, GRB
def optimizeShipment(inputFile,outputFile):
    I= pd.read_excel(inputFile,sheet_name='Fulfilment Centers',index_col=0).index
    J= pd.read_excel(inputFile,sheet_name='Regions',index_col=0).index
    K= pd.read_excel(inputFile,sheet_name='Items',index_col=0).index
    q= pd.read_excel(inputFile,sheet_name='Fulfilment Centers',index_col=0)['capacity']
    delta= pd.read_excel(inputFile,sheet_name='Distances',index_col=0)
    w= pd.read_excel(inputFile,sheet_name='Items',index_col=0)['shipping_weight']
    s= pd.read_excel(inputFile,sheet_name='Items',index_col=0)['storage_size']
    d= pd.read_excel(inputFile,sheet_name='Demand',index_col=0)

    from gurobipy import Model, GRB
    mod=Model()
    x=mod.addVars(I,J,K,name='x')
    mod.setObjective(sum(1.38*x[i,j,k]*w[k]*delta.loc[j,i] for i in I for j in J for k in K))
    for i in I:
            mod.addConstr(sum(x[i,j,k]*s[k] for j in J for k in K)<=q.loc[i],name=f'Capacity_{i}')
    for j in J:
        for k in K:
            mod.addConstr(sum(x[i,j,k] for i in I)>=d.loc[k,j],name=f'Demand_{j}_{k}')
    mod.setParam('outputflag',False)
    mod.optimize()

    writer=pd.ExcelWriter(outputFile)
    pd.DataFrame([mod.objval],columns=['Minimum Total Cost']).to_excel(writer,sheet_name='Objective',index=False)
    df=pd.DataFrame(columns=[I.name, J.name, K.name, 'Shipment'])
    for i in I:
        for j in J:
            for k in K:
                if x[i,j,k].x > 0:
                    df = df.append(pd.DataFrame({I.name: i, J.name:j, K.name: k, 'Shipment': x[i,j,k].x}, index=[0]))
    df.to_excel(writer,sheet_name='Plan',index = False)
    writer.save()
    
if __name__=='__main__':
    import sys, os
    if len(sys.argv)!=3:
        print('Correct syntax: python shipment.py inputFile outputFile')
    else:
        inputFile=sys.argv[1]
        outputFile=sys.argv[2]
        if os.path.exists(inputFile):
            optimizeShipment(inputFile,outputFile)
            print(f'Successfully optimized. Results in "{outputFile}"')
        else:
            print(f'File "{inputFile}" not found!')