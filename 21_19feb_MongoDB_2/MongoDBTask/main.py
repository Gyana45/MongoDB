"""
1.visit link https://archive.ics.uci.edu/ml/machine-learning-databases/00448/

2.download the dataset
3.insert bulk data(csv file into mongodb)
4.different operations
4.1 insertion
4.2 update
4.3 delete
4.4 find
4.5 filter

code evaluation
1.modular coding
2.exception
3.proper log


"""

from myMongo import mongo_operation

DB = "Carbon"
Collection = "Carbon_col"
file_name = "carbon_nanotubes.csv"
url = "mongodb+srv://test:test@cluster0.1mv2i.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

conn = mongo_operation(url, DB, Collection)

"""show databases"""
print(conn.show_databases())

"""insert single record"""

rec = {'Chiral indice n': 5,
       'Chiral indice m': 4,
       'Initial atomic coordinate u': '0,704904',
       'Initial atomic coordinate v': '0,872491',
       'Initial atomic coordinate w': '0,630191',
       "Calculated atomic coordinates u'": '0,709336',
       "Calculated atomic coordinates v'": '0,880125',
       "Calculated atomic coordinates w'": '0,630465'}

# conn.insert_record(rec)

"""Inserting many records"""

rec_list = [
    {'Chiral indice n': 5,
     'Chiral indice m': 4,
     'Initial atomic coordinate u': '0,129304',
     'Initial atomic coordinate v': '0,277928',
     'Initial atomic coordinate w': '0,050956',
     "Calculated atomic coordinates u'": '0,122792',
     "Calculated atomic coordinates v'": '0,274086',
     "Calculated atomic coordinates w'": '0,050998'},
    {'Chiral indice n': 5,
     'Chiral indice m': 4,
     'Initial atomic coordinate u': '0,145816',
     'Initial atomic coordinate v': '0,221293',
     'Initial atomic coordinate w': '0,089208',
     "Calculated atomic coordinates u'": '0,138865',
     "Calculated atomic coordinates v'": '0,215329',
     "Calculated atomic coordinates w'": '0,089298'}
]

# conn.insert_record(rec_list)

"""insert records from csv file"""
filename = "carbon_nanotubes.csv"
#conn.insert_from_csv(filename)

"""find_one_record"""
query = {"Calculated atomic coordinates w'" : {"$in" : ['0,089298','0,050998']}}
#print(conn.find_one_record(query))

"""no query"""
#print(conn.find_one_record())

"""all records"""
#print(len(conn.find_all_record()))

query={"Calculated atomic coordinates v'": '0,274086'}
#print(conn.find_all_record(query))

#conn.find_all_record([1,2,3,4])

"""Limit"""
#print(len(conn.find_limit_record()))

#print(len(conn.find_limit_record(3)))

#print(conn.find_limit_record('ccc'))

"""update"""
present_data={'Chiral indice n':5,'Chiral indice m':4}
new_data={'Initial atomic coordinate u': 'xxxx','Initial atomic coordinate v': 'yyyy'}
#conn.update_record_with_args(1,present_data,new_data)

#conn.update_record_with_args(present_data,new_data)

#conn.update_record_with_args('mno',present_data,new_data)

"""Delete"""
#query={'Chiral indice m': 4,'Initial atomic coordinate u': '0,704904'}
#query={'Chiral indice m': 4,'Initial atomic coordinate u': '0,129304'}
query={'Chiral indice m': '1','Initial atomic coordinate u': '0,717298'}
#conn.delete_one_record(query)
