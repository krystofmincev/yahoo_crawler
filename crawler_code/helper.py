#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 00:34:00 2017

@author: mincev
"""
import pickle 
import os.path

class helper(object):
    """
    supports:
        saving and loading python data structures
    """
    def save_obj(filename, obj):
        """
        input:
            filename (str) = name of file excluding .pkl
            obj = data structure to save
        output:
            -
        """
        assert type(filename) is str
        
        overide = False
        while os.path.isfile('obj/' + filename + '.pkl') is True and overide is False:
            print("File already exists:\n")
            input_overide = input("Do you want to overide the file? (y/n)\n")
            if input_overide.lower() == 'y': 
                overide = True 
            else: 
                filename = input("Choose a different filename:\n")
        
        assert filename[-4:] is not ".pkl"
        with open('obj/' + filename + '.pkl', 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)    

    def load_obj(filename):#
        """
        input:
            filename (str) = name of file excluding .pkl
            obj = data structure to save
        output:
            python obj
        """
        assert type(filename) is str
        assert filename[-4:] is not ".pkl"
        
        with open('obj/' + filename + '.pkl', 'rb') as f:
            return pickle.load(f)