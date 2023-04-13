import csv
import numpy as np
import pandas as pd


def getDF(dataPath):
    with open(dataPath, "r", newline="") as csvfile:
        reader = csv.reader(csvfile)
        header_list = {}
        body = []
        for i, row in enumerate(reader):
            if i == 0:
                header_list = row
            else:
                body.append(row)
    return pd.DataFrame(body, columns=header_list)
# def filter2Class(body, className): 

def probability2amount(df, targets):
    for i in range(len(df)):
        if df.at[i, '樣本數_人'] == '':
            for t in targets:
                df.at[i, t] = 0
            continue
        for t in targets:
            p= df.at[i, t]
            df.at[i, t] = int(np.round(float(p)/100*float(df.at[i, '樣本數_人'])))
    return df

def filterTargets(df, targets):
    filted_df = df[df['類別'].isin(targets)]
    filted_df = filted_df[filted_df['年度'] == '110']
    return filted_df

def sumUpYearly(df):
    keys = df['項目別']
    for i in range(len(keys)):
        key = keys.iat[i]
        row = df[df['項目別'] == key]
        #name = key

    

# Main
L2J_df = getDF("row_data/Location2Job-2.csv")
PPI2J_df = getDF("row_data/PPinfo2Job-2.csv")

job_targets = ['民意代表_主管及經理人員','專業人員','技術員及助理專業人員','事務支援人員','服務及銷售工作人員', '農_林_漁_牧業生產人員', '技藝有關工作人員', '機械設備操作及組裝人員', '基層技術工及勞力工']

L2J_targets = ['縣市']
PPI2J_targets = ['年齡','性別','教育程度','個人每月收入']

print("-----------2 amount-----------")

L2J_df = probability2amount(L2J_df, job_targets)
PPI2J_df = probability2amount(PPI2J_df, job_targets)
print(L2J_df)
print(PPI2J_df)
print("-----------filter-----------")

L2J_df = filterTargets(L2J_df, L2J_targets)
PPI2J_df = filterTargets(PPI2J_df, PPI2J_targets)

job_targets.insert(0,'類別')
job_targets.insert(1,'項目別')
job_targets.insert(0,'年度')
L2J_df = L2J_df[job_targets]
PPI2J_df = PPI2J_df[job_targets]
print(L2J_df)
print(PPI2J_df)


print("------------sum up----------")


# L2J_df = sumUpYearly(L2J_df)
# PPI2J_df = sumUpYearly(PPI2J_df)
print("------------transpose----------")


print("------------output----------")

L2J_df.to_csv(f"result/Location2Job.csv")
PPI2J_df.to_csv(f"result/PeopleInfo2Job.csv")