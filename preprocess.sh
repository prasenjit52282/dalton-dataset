#!/bin/bash

#households
for n in {1..13}; 
do
    #echo H$n
    python preprocess_data.py --customer H$n --workers 8
done

#Studio Apartments
for n in {1..8}; 
do
    #echo A$n
    python preprocess_data.py --customer A$n --workers 8
done

#Research Labs
for n in {1..5}; 
do
    #echo R$n
    python preprocess_data.py --customer R$n --workers 4
done

#Food Canteens
for n in {1..2}; 
do
    #echo F$n
    python preprocess_data.py --customer F$n --workers 2
done

#Classrooms
for n in {1..2}; 
do
    #echo C$n
    python preprocess_data.py --customer C$n --workers 2
done