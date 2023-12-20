import streamlit as st
import pandas as pd
import numpy as np
import csv
import requests

st.title('Flavor Pairings')

st.text('What ingredient do you have? We\'ll recommend some pairings.')

pairings = None

def loadCSV(pairingsCSV): 
    """
    Takes in a CSV file of ingredient pairings, and returns
    a dictionary where {'MAIN INGREDIENT': [List of Pairings]}.
    
    CSV file should be in string format.
    """
    ingredientMatches = {}
    with open(pairingsCSV, newline='', encoding='utf8') as csvfile:
        ingredientReader = csv.reader(csvfile)
        pairingList = []
        prevKey = 'ACHIOTE SEEDS'
        badKeywords = ('Season:', 'Techniques:', 'Taste:', 'Volume:', 'Weight:', 'Flavor Aff', 'Botanical rel', 'Tips:', 'Function')
        for row in ingredientReader: # for each row in the file
            if row[0] != prevKey: # if current main is a new ingredient
                # update the dictionary with {main: pairing list}
                ingredientMatches.update({prevKey.lower(): pairingList}) 
                # clear the list for new pairings
                pairingList = [] 
            if row[1].startswith(badKeywords):
                pass
            else:
                pairingList.append(row[1]) # add the pairing to the pairingList
            prevKey = row[0] # update prevKey to the current main

    return ingredientMatches

@st.cache_data
def load_data():
    return loadCSV('flavor_bible_full.csv')

ingredientPairings = load_data()

choice = st.chat_input(placeholder='Whatcha got?')

allMains = list(ingredientPairings.keys())


def print_pairings(ingredient):
    pairings = ingredientPairings.get(ingredient)

    if pairings: 
        st.subheader(ingredient.title() + ' go well with...')
        col1, col2, col3 = st.columns(3)
        n = len(pairings)
        per_col = n // 3
        counter = 0
        for ing in pairings:
            counter += 1
            if counter < per_col:
                with col1:
                    st.write(ing)
            elif counter < per_col * 2:
                with col2:
                    st.write(ing)
            else:
                with col3:
                    st.write(ing)
                    


if choice:
    print_pairings(choice)


