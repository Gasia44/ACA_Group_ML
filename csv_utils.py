import pandas as pd

def hasNumbers(inputString):
    return all(char.isdigit() for char in inputString)

def read_csv(file_to_reed, header=None):
    #file_to_reed = "SPECTF.dat"
    with open(file_to_reed) as f:           
        data = f.readlines() 
        #print(data)
    temp=''   
    flag = 0
    if header != None:
        flag = 1
    df =pd.DataFrame( index=range(len(data)), columns=range(len(data[0]))) 
    row=0
    
    for i in range(len(data)):
        temp=''
        col = 0
        for j in range(len(data[i])):
            if(data[i][j] !=','):
                temp=temp + str(data[i][j])
                tempfinal =temp
            else:  

                if flag == 1 and i == 0:
                    df = df.rename(columns = {str(col): temp})
                    col = col + 1
                    row =-1
                    temp =''
                  
                    
                else:
                    if(hasNumbers(temp)):
                        df.loc[row, col]= int(temp)
                    else: 
                        df.loc[row, col] = temp
                    col = col+1
                temp=''
        
        if(tempfinal[-1] =='\n'):
            tempfinal = tempfinal[0:len(tempfinal)-1]
        if(hasNumbers(tempfinal) and row !=-1):
                df.loc[row, col]= int(tempfinal)
        else: 
            if(row !=-1):
                df.loc[row, col] = tempfinal
                col = col+1
                temp=''
        row = row +1
        
    df=df.dropna(axis=1, how='all')
    df=df.dropna(axis=0, how='all')
    return df
    