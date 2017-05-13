import pandas as pd

def read_csv(file_to_reed, header=True, seperator = ','):
    '''''
    read csv file using specified seperator
    take as argument the file that will be read, the header and the seperator;
    if the header is None, then columns' label are 1,2,3,...
    return a dataframe
    '''''

    with open(file_to_reed) as f:           
        data = f.readlines()

    strip_data = [a.strip() for a in data]

    list_of_rows = []

    # column label
    label_data = (strip_data[0].split(seperator))

    if header == None:
        list_of_rows.append(label_data)

    for i in range(1, len(data)):
        one_row = (strip_data[i].split(seperator))
        list_of_rows.append(one_row)

    df =pd.DataFrame(list_of_rows)

    if header != None:
        df.columns = label_data

    return df