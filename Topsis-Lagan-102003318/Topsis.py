import pandas as pd
import os
import sys

#Lagan Garg

def main():
    
    if len(sys.argv) != 5:
        print("ERROR : NUMBER OF PARAMETERS")
        print("USAGE : python topsis.py inputfile.csv '1,1,1,1' '+,+,-,+' result.csv ")
        exit(1)

   
    elif not os.path.isfile(sys.argv[1]):
        print(f"ERROR : {sys.argv[1]} Don't exist!!")
        exit(1)

   
    elif ".csv" != (os.path.splitext(sys.argv[1]))[1]:
        print(f"ERROR : {sys.argv[1]} is not csv!!")
        exit(1)

    else:
        dataset, temp_dataset = pd.read_csv(
            sys.argv[1]), pd.read_csv(sys.argv[1])
        nc = len(temp_dataset.columns.values)

        
        if nc < 3:
            print("ERROR : Input file have less then 3 columns")
            exit(1)

        
        for i in range(1, nc):
            pd.to_numeric(dataset.iloc[:, i], errors='coerce')
            dataset.iloc[:, i].fillna(
                (dataset.iloc[:, i].mean()), inplace=True)

        
        try:
            w = [int(i) for i in sys.argv[2].split(',')]
        except:
            print("ERROR : In w array please check again")
            exit(1)
        impct = sys.argv[3].split(',')
        for i in impct:
            if not (i == '+' or i == '-'):
                print("ERROR : In impct array please check again")
                exit(1)

        
        if nc != len(w)+1 or nc != len(impct)+1:
            print(
                "ERROR : Number of w, number of impcts and number of columns not same")
            exit(1)

        if (".csv" != (os.path.splitext(sys.argv[4]))[1]):
            print("ERROR : Output file extension is wrong")
            exit(1)
        if os.path.isfile(sys.argv[4]):
            os.remove(sys.argv[4])
        
        topsis_pipy(temp_dataset, dataset, nc, w, impct)


def Normalize(temp_dataset, nc, w):
    
    for i in range(1, nc):
        temp = 0
        for j in range(len(temp_dataset)):
            temp = temp + temp_dataset.iloc[j, i]**2
        temp = temp**0.5
        for j in range(len(temp_dataset)):
            temp_dataset.iat[j, i] = (
                temp_dataset.iloc[j, i] / temp)*w[i-1]
    return temp_dataset


def Calc_Values(temp_dataset, nc, impct):
   
    pos_sol = (temp_dataset.max().values)[1:]
    neg_sol = (temp_dataset.min().values)[1:]
    for i in range(1, nc):
        if impct[i-1] == '-':
            pos_sol[i-1], neg_sol[i-1] = neg_sol[i-1], pos_sol[i-1]
    return pos_sol, neg_sol


def topsis_pipy(temp_dataset, dataset, nc, w, impct):
   
    temp_dataset = Normalize(temp_dataset, nc, w)

   
    pos_sol, neg_sol = Calc_Values(temp_dataset, nc, impct)

   
    score = []
    for i in range(len(temp_dataset)):
        temp_p, temp_n = 0, 0
        for j in range(1, nc):
            temp_p = temp_p + (pos_sol[j-1] - temp_dataset.iloc[i, j])**2
            temp_n = temp_n + (neg_sol[j-1] - temp_dataset.iloc[i, j])**2
        temp_p, temp_n = temp_p**0.5, temp_n**0.5
        score.append(temp_n/(temp_p + temp_n))
    dataset['Topsis Score'] = score

    
    dataset['Rank'] = (dataset['Topsis Score'].rank(
        method='max', ascending=False))
    dataset = dataset.astype({"Rank": int})

   
    dataset.to_csv(sys.argv[4], index=False)
    

if __name__ == "__main__":
    main()
