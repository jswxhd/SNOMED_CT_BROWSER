import pymysql
import csv
from functools import reduce

#connect database
def connect_db():
    db = pymysql.connect("localhost", "root", "980611", "snomedct")
    return db

#user‘s query input
def user_query(text):
    sql = "SELECT DISTINCT conceptid FROM description_f WHERE term LIKE '%s' AND active = '%s'" % ('%'+text+'%','1')
    return sql

#单词去重
def eliminate_dupli(sentence):
    my_sentence = sentence.split(' ')
    my_new_sentence = []
    for each in my_sentence:
        if each not in my_new_sentence:
            my_new_sentence.append(each)
    
    return ' '.join(my_new_sentence)

#为了算法找term
def find_query(number):
    db = connect_db()
    sql="SELECT term FROM description_f WHERE conceptid = '%s'" % (number)
    cursor = db.cursor()
    #temp=[]
    temp = ''
    try:
        cursor.execute(sql)
        results=cursor.fetchall()
        for row in results:
            temp += ''.join(row)+' '

        temp = eliminate_dupli(temp)
        #if result:
            #temp.append(''.join(result[0]))   
        #if not result:
            #temp=[]
    except:
         print('')
    return temp

#为了算法找term
def find_term(mylist):
    n=len(mylist)
    term=[]
    for i in range(0,n):
        tmp=[]
        for j in mylist[i]:
            result=find_query(j)
            tmp.append(result)
        term.append(tmp)
    return term

#搜索第一步       
def partition_match(text):
    db = connect_db()
    sql = user_query(text)
    cursor = db.cursor()
    partition_results_conceptID = []
    
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            partition_results_conceptID.append(row[0])   
        
    except:
        print("Error: unable to fecth data")
                
    return partition_results_conceptID

#为了算法找term
def find_term_2(mylist):
    term = []
    for each in mylist:
        term.append(find_query(each))

    return term

#找同义词和结果
def find_query_2(number):
    db = connect_db()
    sql="SELECT DISTINCT term FROM description_f WHERE conceptid = '%s' AND active = '%s' AND typeid = '%s'" % (number,'1','900000000000013009')
    cursor = db.cursor()
    #temp=[]
    temp = ''
    synonyms = []
    try:
        cursor.execute(sql)
        results=cursor.fetchall()
        temp = ''.join(results[0]) 
        for i in range(1,len(results)):
                synonyms.append(''.join(results[i]))
        #if result:
            #temp.append(''.join(result[0]))   
        #if not result:
            #temp=[]

    except:
         print('')
    return temp, synonyms

#找同义词和结果
def find_term_3(mylist):
    term = []
    synonyms = []
    for each in mylist:
        term.append(find_query_2(each)[0])
        synonyms.append(find_query_2(each)[1])
    
    return term,synonyms

#找attribute relationship
def find_query_3(number):
    db = connect_db()
    sql="SELECT DISTINCT term FROM description_f WHERE conceptid = '%s' " % (number)
    cursor = db.cursor()
    #temp=[]
    temp = ''
    try:
        cursor.execute(sql)
        results=cursor.fetchall()
        temp = ''.join(results[0]) 
            
    except:
         print('')
    return temp

#找attribute relationship
def find_term_4(mylist):
    n=len(mylist)
    term=[]
    for i in range(0,n):
        tmp=[]
        for j in mylist[i]:
            result=find_query_3(j)
            tmp.append(result)
        term.append(tmp)
    return term

#找Fully Specified Name
def find_query_4(number):
    db = connect_db()
    sql="SELECT DISTINCT term FROM description_f WHERE conceptid = '%s' AND active = '%s' AND typeid = '%s'" % (number,'1','900000000000003001')
    cursor = db.cursor()
    #temp=[]
    temp = ''
    try:
        cursor.execute(sql)
        results=cursor.fetchall()
        if results:
            temp = ''.join(results[0]) 

    except:
         print('')
    return temp

#找Fully Specified Name
def find_term_5(mylist):
    term = []
    for each in mylist:
        term.append(find_query_4(each))

    return term


def construct_group(key_words):
    
    group_distance_1=[]
    try:
         
        for key in key_words:
            with open('data.csv')as f:
                f_csv = csv.reader(f)
                list1=[]
                for row in f_csv:       
                    if row[0]==key:
                        list1.append(row[1])
                    elif row[1]==key:
                        list1.append(row[0])
                
                group_distance_1.append(list1)
        
    except:
        print("Error: unable to find distance 1 group")
        
    return group_distance_1
        
    


