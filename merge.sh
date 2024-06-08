#!/bin/bash

#households
for n in {1..13}; 
do
    #echo H$n
    python merge_replicas.py --customer H$n
done

#Studio Apartments
for n in {1..8}; 
do
    #echo A$n
    python merge_replicas.py --customer A$n
done

#Research Labs
for n in {1..5}; 
do
    #echo R$n
    python merge_replicas.py --customer R$n
done

#Food Canteens
for n in {1..2}; 
do
    #echo F$n
    python merge_replicas.py --customer F$n
done

#Classrooms
for n in {1..2}; 
do
    #echo C$n
    python merge_replicas.py --customer C$n
done