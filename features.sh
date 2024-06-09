#!/bin/bash

#households
for n in {1..13}; 
do
    #echo H$n
    python compute_feat.py --customer H$n --workers 16
done

#Studio Apartments
for n in {1..8}; 
do
    #echo A$n
    python compute_feat.py --customer A$n --workers 16
done

#Research Labs
for n in {1..5}; 
do
    #echo R$n
    python compute_feat.py --customer R$n --workers 16
done

#Food Canteens
for n in {1..2}; 
do
    #echo F$n
    python compute_feat.py --customer F$n --workers 16
done

#Classrooms
for n in {1..2}; 
do
    #echo C$n
    python compute_feat.py --customer C$n --workers 16
done