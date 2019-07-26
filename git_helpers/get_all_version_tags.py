#!/usr/bin/env python3
import os
import re
import sys

from . import git_utils as git
from . import regex_obj as ro

from ..gpkgs import message as msg

from ..utils import shell_helpers as shell
from ..utils.prompt import prompt_boolean


def get_all_version_tags():
    results=shell.cmd_get_value("git tag")
    versions=[]
    if results:
        for result in results.splitlines():
            if result:
                if result[0] == "v":
                    regex_version=ro.Version_regex(result[1:])

                    if regex_version.match:
                        versions.append(regex_version.major_minor_patch)
    
        if versions:
            return tag_sort(versions)
        else:
            return ""
    else:
        return ""

# # bubble sort
def bubble_sort_array(array, size):
    temp="" # int
    swap=True # boolean
    index_array=[]

    for i in range(0, size):
        index_array.append(i)

    index_order=[]

    while swap:
        swap=False
        count2=0
        for count in range(0, size-1):
            if array[count] > array[count + 1]:
                temp = array[count]
                array[count] = array[count + 1]
                array[count + 1] = temp

                temp_index = index_array[count]
                index_array[count] = index_array[count+1]
                index_array[count +1] = temp_index

                swap = True

    return index_array

def get_dotted_group_num(array_element):
    count=0
    for elem in array_element.split("."):
        count+=1

    return count

def tag_sort(array, group_num=0):
    num_dotted_elem=get_dotted_group_num(array[0])
    arr_of_dict=[]
    for elem in array:
        tmp_dict={}
        for i, value in enumerate(elem.split(".")):
            tmp_dict[i]=int(value)

        arr_of_dict.append(tmp_dict)

    # extract group according to the dotted_group_number
    group_array=[]
    for elem in arr_of_dict:
        if group_num == 0:
            group_array.append(elem[group_num])
        elif group_num == 1:
            group_array.append(elem[group_num-1])
        else:
            tmp_elem=""
            for i, value in enumerate(elem):
                if i < group_num-1:
                    tmp_elem+= str(elem[i])+"."
                elif i < group_num:
                    tmp_elem+= str(elem[i])
            
            group_array.append(tmp_elem)

    tmp_group=[]
    group_count=0
    for i, elem in enumerate(group_array):
        if group_num == 0:
            tmp_group=group_array
            break
        else:
            if i == 0:
                tmp_group.append([])
            elif i < len(group_array):
                if group_array[i] == group_array[i-1]:
                    pass
                else:
                    group_count+=1
                    tmp_group.append([])

            tmp_group[group_count].append(arr_of_dict[i][group_num])

    index_acc=0
    tmp_arr=[]
    if group_num == 0:
        index_array=bubble_sort_array(tmp_group[:], len(tmp_group))

        for i in range(0, len(array)):
            tmp_arr.append(i)

        for i, value in enumerate(index_array):
            tmp_arr[i]=array[value]
    else:
        for group in tmp_group:
            for index in bubble_sort_array(group[:], len(group)):
                tmp_arr.append(array[index_acc+index])

            index_acc+=len(group)

    array=tmp_arr[:]

    if group_num < num_dotted_elem-1:
        group_num+=1
        return tag_sort(array, group_num)
    else:
        return(array) 

# index is returned instead of values
def tag_sort_index(array, arr_of_dict=[], group_num=0):
    num_dotted_elem=get_dotted_group_num(array[0])
    if not arr_of_dict:
        arr_of_dict=[]
        for i, elem in enumerate(array):
            tmp_dict={}
            for j, value in enumerate(elem.split(".")):
                tmp_dict[j]=int(value)

            arr_of_dict.append({ i: tmp_dict })

    # extract group according to the dotted_group_number
    group_array=[]

    for obj in arr_of_dict:
        elem = obj[next(iter(obj))]
        if group_num == 0:
            group_array.append(elem[group_num])
        elif group_num == 1:
            group_array.append(elem[group_num-1])
        else:
            tmp_elem=""
            for i, value in enumerate(elem):
                if i < group_num-1:
                    tmp_elem+= str(elem[i])+"."
                elif i < group_num:
                    tmp_elem+= str(elem[i])
            
            group_array.append(tmp_elem)

    # create group with of concatened dotted value. for instance group of 1.2 in order to sort 1.2.3 with 1.2.5
    # then it returns an array of [3, 5]
    tmp_group=[]
    group_count=0
    for i, elem in enumerate(group_array):
        if group_num == 0:
            tmp_group=group_array
            break
        else:
            if i == 0:
                tmp_group.append([])
            elif i < len(group_array):
                if group_array[i] == group_array[i-1]:
                    pass
                else:
                    group_count+=1
                    tmp_group.append([])

            index_obj=next(iter(arr_of_dict[i]))
            tmp_group[group_count].append(arr_of_dict[i][index_obj][group_num]) 
             
    index_acc=0
    tmp_arr=[]
    tmp_arr_of_dict=[]
    if group_num == 0:
        index_array=bubble_sort_array(tmp_group[:], len(tmp_group))
        for i in range(0, len(array)):
            tmp_arr.append(i)
            tmp_arr_of_dict.append(i)

        for i, value in enumerate(index_array):
            tmp_arr[i]=array[value]
            tmp_arr_of_dict[i]=arr_of_dict[value]

    else:
        for group in tmp_group:
            index_array=bubble_sort_array(group[:], len(group))
            for index in index_array:
                tmp_arr.append(array[index_acc+index])
                tmp_arr_of_dict.append(arr_of_dict[index_acc+index])

            index_acc+=len(group)

    array=tmp_arr[:]
    arr_of_dict=tmp_arr_of_dict[:]

    if group_num < num_dotted_elem-1:
        group_num+=1
        return tag_sort_index(array, arr_of_dict, group_num)
    else:
        array=[]
        for obj in arr_of_dict:
            array.append(next(iter(obj)))
        return(array) 
