# -*- coding: utf-8 -*-
from time import*
import numpy as np
import json
import connect_mysql2 as cm
from LSA_test import get_similarity_group
#import os
#os.chdir("D:/python_work/senior_project")

def read_intermediate_file(filename):
    with open(filename,'r') as f:
        content = f.read()
    my_dict = json.loads(content)

    return my_dict


def fetch_intermediate_file(mylist,mydict):
    my_relatives = []
    for each in mylist:
        if each in mydict.keys():
            my_relatives.append(mydict[each])
        else:
            my_relatives.append([])
    
    return my_relatives


def get_relatives(query):
    begin=time()

    dict_children=read_intermediate_file('dict_children.txt')
    dict_parents=read_intermediate_file('dict_parents.txt')
    dict_AM=read_intermediate_file('dict_Associated_morphology.txt')
    dict_CA=read_intermediate_file('dict_Causative_agent.txt')    
    dict_M=read_intermediate_file('dict_method.txt')
    dict_FS=read_intermediate_file('dict_find_site.txt')    

    a=cm.partition_match(query)
    #print(a)
    results_term = cm.find_term_2(a)
    #children=[]
    #parents=[]
    #AM = []
    #CA = []
    #M = []
    #FS = []
    
    children = fetch_intermediate_file(a,dict_children)
    #for k in a:
        #if k in dict_children.keys():
            #children.append(dict_children[k])
        #else:
            #children.append([])
    parents = fetch_intermediate_file(a,dict_parents)
    
    AM = fetch_intermediate_file(a,dict_AM)
 
    CA = fetch_intermediate_file(a,dict_CA)

    M = fetch_intermediate_file(a,dict_M)

    FS = fetch_intermediate_file(a,dict_FS)

    
    #print(FS)
    #print(children)      
    grand_children=[]
    grand_parents=[]

    children_length=len(children)
    for i in range(0,children_length):
        temp=[]
        for j in children[i]:
            if j in dict_children.keys() and j!=a[i]:
                for each in dict_children[j]:
                    temp.append(each)
            #else:
                #temp.append([])
        grand_children.append(temp)
        
    parents_length=len(parents)
    for m in range(0,parents_length):
        temp=[]
        for u in parents[m]:
            if u in dict_parents.keys() and u!=a[m]:
                for each in dict_parents[u]:
                    temp.append(each)
            #else:
                #temp.append([])
        grand_parents.append(temp)

    middle=time()
    results_term_2, results_synonmys = cm.find_term_3(a)
    results_FSN = cm.find_term_5(a)
    children_term=cm.find_term(children)
    parents_term=cm.find_term(parents)
    grand_children_term=cm.find_term(grand_children)
    grand_parents_term=cm.find_term(grand_parents)
    AM_term = cm.find_term_4(AM)
    CA_term = cm.find_term_4(CA)
    M_term = cm.find_term_4(M)
    FS_term = cm.find_term_4(FS)
    end=time()
    #print(parents)
    #print(grand_parents)
    #print(grand_parents_term[:3],len(grand_parents_term))
    #print(results_FSN)
    print(middle-begin)
    print(end-middle)

    return results_term_2,results_synonmys,results_FSN,results_term,children_term, parents_term, grand_children_term, grand_parents_term, AM_term, CA_term, M_term, FS_term
    #运行时间18.64s

#xx = get_relatives('headache')[0]
#a = cm.partition_match('cough')
#get_relatives('headache')

def get_relatives_2(query):
    begin=time()

    dict_children=read_intermediate_file('dict_children.txt')
    dict_parents=read_intermediate_file('dict_parents.txt')
  
    a=cm.partition_match(query)
    #print(a)
    results_term = cm.find_term_2(a)
    children = fetch_intermediate_file(a,dict_children)
    parents = fetch_intermediate_file(a,dict_parents)
    
    grand_children=[]
    grand_parents=[]

    children_length=len(children)
    for i in range(0,children_length):
        temp=[]
        for j in children[i]:
            if j in dict_children.keys() and j!=a[i]:
                for each in dict_children[j]:
                    temp.append(each)
            #else:
                #temp.append([])
        grand_children.append(temp)
        
    parents_length=len(parents)
    for m in range(0,parents_length):
        temp=[]
        for u in parents[m]:
            if u in dict_parents.keys() and u!=a[m]:
                for each in dict_parents[u]:
                    temp.append(each)
            #else:
                #temp.append([])
        grand_parents.append(temp)

    middle=time()
    children_term=cm.find_term(children)
    parents_term=cm.find_term(parents)
    grand_children_term=cm.find_term(grand_children)
    grand_parents_term=cm.find_term(grand_parents)
    end=time()

    print(middle-begin)
    print(end-middle)

    return a,results_term,children_term, parents_term, grand_children_term, grand_parents_term

#results_term=get_relatives_2('headache')[1]
#print(results_term)


def grouping(results_term,children_term, parents_term, grand_children_term, grand_parents_term):
    #results_term, children_term, parents_term, grand_children_term, grand_parents_term = get_relatives(query)
    total_group = []
    total_group_index =[]
    for i,j,k,m,n in zip(results_term, children_term, parents_term, grand_children_term, grand_parents_term):
        temp = []
        temp = j+k+m+n

        if temp:
            simlarity_group = get_similarity_group(temp, i)
            total_group.append(simlarity_group)
        else:
            total_group.append([])
    #a = children_term[0]+parents_term[0]+grand_children_term[0]+grand_parents_term[0]
    #similarity_group = get_similarity_group(a,results_term[0])
    #print(total_group[:4])
    #print(results_term[0], children_term[0],parents_term[0],grand_children_term[0],grand_parents_term[0])
    for i,j,k,m,n in zip(results_term, children_term, parents_term, grand_children_term, grand_parents_term):
        temp_index = []
        if j:
            for x in range(len(j)):
                temp_index.append(1)
        if k:
            for x in range(len(k)):
                temp_index.append(1)
        if m:
            for x in range(len(m)):
                temp_index.append(2)
        if n:
            for x in range(len(n)):
                temp_index.append(2)
     
        if temp_index:
            total_group_index.append(temp_index)
        else:
            total_group_index.append([])

    #print(total_group_index[:4])
    #print(similarity_group)

    return total_group, total_group_index

#grouping('cough')


def weighted_similarity(x,y):
    weighted_sim = 0
    for a,b in zip(x,y):
        if a > 0:
            weighted_sim += a*b
        if a < 0:
            weighted_sim += a/b
    
    return weighted_sim


def grouping_similarity_2(total_group, total_group_index):
    #total_group,total_group_index = grouping(query)
    scores = []
    for i,j in zip(total_group,total_group_index):
        if i and j:
            scores.append(weighted_similarity(i,j))
        else:
            scores.append(0)

    return scores

#xx=grouping_similarity_2('cough')
#print(xx[:10],len(xx))

def sorting_list(a,b):
    for i in range(len(a)-1):
        max_index = i
        for j in range(i+1,len(a)):
            if a[max_index] < a[j]:
                max_index = j
    
        b[i],b[max_index] = b[max_index], b[i]

    return b


def sorted_results(query):
    results_term_2, results_synonmys, results_FSN, results_term, children_term, parents_term, grand_children_term, grand_parents_term, AM_term, CA_term, M_term, FS_term = get_relatives(query)
    total_group,total_group_index = grouping(results_term, children_term, parents_term, 
                                                grand_children_term, grand_parents_term)
    scores = grouping_similarity_2(total_group, total_group_index)
    #my_results = cm.partition_match(query)
    #results_term = cm.find_term_2(my_results)
    #scores = grouping_similarity_2(query)
    #sorted_results_id = sorting_list(scores, results_id)
    begin=time()
    sorted_results_term = sorting_list(scores,results_term_2)
    sorted_results_synonmys = sorting_list(scores, results_synonmys)
    sorted_results_FSN = sorting_list(scores, results_FSN)
    sorted_children_term = sorting_list(scores,children_term)
    sorted_parents_term = sorting_list(scores,parents_term)
    sorted_grandchildren_term = sorting_list(scores,grand_children_term)
    sorted_grandparents_term = sorting_list(scores,grand_parents_term)
    sorted_AM_term = sorting_list(scores, AM_term)
    sorted_CA_term = sorting_list(scores, CA_term)
    sorted_M_term = sorting_list(scores, M_term)
    sorted_FS_term = sorting_list(scores, FS_term)
    end=time()
    print(end-begin)
    
    return sorted_results_term, sorted_results_synonmys, sorted_results_FSN, sorted_children_term, sorted_parents_term, sorted_grandchildren_term, sorted_grandparents_term, sorted_AM_term, sorted_CA_term, sorted_M_term, sorted_FS_term
    
#sorted_results_term, sorted_results_synonmys, sorted_results_FSN, sorted_children_term, sorted_parents_term, sorted_grandchildren_term, sorted_grandparents_term, sorted_AM_term, sorted_CA_term, sorted_M_term, sorted_FS_term = sorted_results('cough')
#print(sorted_results_term)
#xx = sorted_results('cough')[3]
#print(xx[:10], len(xx))

def sorted_results_2(query):
    results_conceptid, results_term, children_term, parents_term, grand_children_term, grand_parents_term = get_relatives_2(query)
    total_group,total_group_index = grouping(results_term, children_term, parents_term, 
                                                grand_children_term, grand_parents_term)
    scores = grouping_similarity_2(total_group, total_group_index)
    #print(scores)
    begin=time()
    dict_AM=read_intermediate_file('dict_Associated_morphology.txt')
    dict_CA=read_intermediate_file('dict_Causative_agent.txt')    
    dict_M=read_intermediate_file('dict_method.txt')
    dict_FS=read_intermediate_file('dict_find_site.txt')

    length = len(results_conceptid)
    sorted_results_conceptid= sorting_list(scores,results_conceptid)
    middle=time()

    if length<50:
        AM = fetch_intermediate_file(sorted_results_conceptid,dict_AM)
        CA = fetch_intermediate_file(sorted_results_conceptid,dict_CA)
        M = fetch_intermediate_file(sorted_results_conceptid,dict_M)
        FS = fetch_intermediate_file(sorted_results_conceptid,dict_FS)
        sorted_AM_term = cm.find_term_4(AM)
        sorted_CA_term = cm.find_term_4(CA)
        sorted_M_term = cm.find_term_4(M)
        sorted_FS_term = cm.find_term_4(FS)
        sorted_results_term, sorted_results_synonmys = cm.find_term_3(sorted_results_conceptid)
        sorted_results_FSN = cm.find_term_5(sorted_results_conceptid)
        sorted_children_term = sorting_list(scores,children_term)
        sorted_parents_term = sorting_list(scores,parents_term)
        sorted_grandchildren_term = sorting_list(scores,grand_children_term)
        sorted_grandparents_term = sorting_list(scores,grand_parents_term)

    else:
        sorted_results_conceptid50 = sorted_results_conceptid[:50]
        AM = fetch_intermediate_file(sorted_results_conceptid50,dict_AM)
        CA = fetch_intermediate_file(sorted_results_conceptid50,dict_CA)
        M = fetch_intermediate_file(sorted_results_conceptid50,dict_M)
        FS = fetch_intermediate_file(sorted_results_conceptid50,dict_FS)
        sorted_AM_term = cm.find_term_4(AM)
        sorted_CA_term = cm.find_term_4(CA)
        sorted_M_term = cm.find_term_4(M)
        sorted_FS_term = cm.find_term_4(FS)
        sorted_results_term, sorted_results_synonmys = cm.find_term_3(sorted_results_conceptid50)
        sorted_results_FSN = cm.find_term_5(sorted_results_conceptid50)
        sorted_children_term = sorting_list(scores,children_term)
        sorted_parents_term = sorting_list(scores,parents_term)
        sorted_grandchildren_term = sorting_list(scores,grand_children_term)
        sorted_grandparents_term = sorting_list(scores,grand_parents_term)

    end=time()
    print(middle-begin)
    print(end-middle)
    
    return length, sorted_results_term, sorted_results_synonmys, sorted_results_FSN, sorted_children_term, sorted_parents_term, sorted_grandchildren_term, sorted_grandparents_term, sorted_AM_term, sorted_CA_term, sorted_M_term, sorted_FS_term

#length, sorted_results_term, sorted_results_synonmys, sorted_results_FSN, sorted_children_term, sorted_parents_term, sorted_grandchildren_term, sorted_grandparents_term, sorted_AM_term, sorted_CA_term, sorted_M_term, sorted_FS_term=sorted_results_2('cough')
#print(sorted_results_term)
#sorted_resuts_term=sorted_results_2('headache')[1]
#print(sorted_resuts_term)
#sorted_results_2('headache')