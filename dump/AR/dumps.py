import pandas

def generate_diaries_info():
    col_list = ["site", "gender"]

    data = pandas.read_csv('articulos.csv',  usecols=col_list)
    data = data.groupby(['site','gender']).size().unstack(fill_value=0)
    data['percent_f'] = 100*data['F']/(data['F'] + data['M'])
    data['percent_m'] = 100*data['M']/(data['F'] + data['M'])
    data.to_csv('diaries_info.csv')

def generate_authors_info():
    col_list = ["author","gender"]

    data = pandas.read_csv('articulos.csv',  usecols=col_list)
    data['art_published'] = data.groupby(['author'])['author'].transform('count')
    data = data.drop_duplicates()
    data.to_csv('authors_info.csv')

generate_authors_info()
generate_diaries_info()
