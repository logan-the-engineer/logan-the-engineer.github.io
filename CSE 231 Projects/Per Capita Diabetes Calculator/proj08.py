"""
CSE Project #8

Description

    This program extracts and display diabetes data of regions and their countries 
    from "IDF_type1_and_demographics.csv". It is implemented using a driver (this file) and
    is meant to function within the Python interpreter.
    For a detailed description of the program, read "Project08.pdf"

Notable Concepts

    CSV file reading, data extraction, nested lists, dictionaries, functions, try-except statements,
    csv module, operator module

Algorithm

    create master dictionary of regions and list of lists of region and
     its countries' diabetes data
        prompt for desired file and ensure it's valid
        extract desired data and create dictionary where keys are regions
         in file and values are lists of lists of countries within respective
         region
            nested lists contain diabetes data for each country
            
    calculate per capita diabetes for each country and append to
     country's list
     
    determine countries with highest and lowest per capita diabetes
     for each region
     
    print results
    
    print closing message

"""

import csv
from operator import itemgetter

def open_file():
    """
    prompt user for input file and return its pointer
    
    display error message and reprompt if the file name doesn't exist
    """
    
    while True:
    
        try:
        
            fp = open(input("Input a file: "), encoding = "utf-8")
            break
    
        except FileNotFoundError:
        
            print("Error: file does not exist. Please try again.")

    return fp

def max_in_region(master_dictionary,region):
    """
    return name and per capita diabetes cases of country with highest per capita diabetes
    """
    
    # extract country with max per capita diabetes from master dicitonary
    max_in_region_list = max(master_dictionary[region], key=itemgetter(3))
    
    return (max_in_region_list[0], max_in_region_list[3])
    
def min_in_region(master_dictionary,region):
    """
    return name and per capita diabetes cases of country with lowest per capita diabetes
    """
    
    """
    extract country with min per capita diabetes from master dicitonary
    ignore countries with 0 for per capita diabetes
    """
    min_in_region_list = min([element for element in master_dictionary[region] \
                              if element[3] != 0], key=itemgetter(3))
    
    return (min_in_region_list[0], min_in_region_list[3])

def read_file(fp):
    """
    read input file and return dicitonary of countries' diabetes and population data
    
    organize data as dictionary of lists of lists, with regions as
     dictionary keys and countries and their population and diabetes data
     within nested lists
    """
    
    # initialize master dictionary
    master_dictionary = {}
    
    # initialize csv reader
    reader = csv.reader(fp)
    
    # skip header line
    next(reader)
    
    # iterate through each line in file
    for line_list in reader:
        
        # create variables for desired data to improve readability
        region_str = line_list[1]
        country_str = line_list[2]
        
        
        """
        create variables for desired data to improve readability
        if desired data not a number, skip entire line
        """
        try:
            
            # remove commas from numbers
            population_float = float(line_list[5].replace(",", ""))
            
            diabetes_float = float(line_list[9])
            
        
        except ValueError:
            
            continue
        
        """
        add extracted data to nested list in dictionary according to region
        if region not in dictionary, add it
        """
        if not region_str in master_dictionary:
            
            master_dictionary[region_str] = \
                [[country_str, diabetes_float, population_float]]
        
        else:
            
            master_dictionary[region_str].append( \
                            [country_str, diabetes_float, population_float])
    
    # sort each list of lists in dictionary alphabetically according to country names
    for region in master_dictionary:
        
        master_dictionary[region].sort()
        
    return master_dictionary

def add_per_capita(master_dictionary):
    """
    calculate per capita diabetes for each country and append to country's list
    
    per capita diabetes calculated by dividing country's cases of diabetes by
     its population
    """
    
    # iterate through each region in master dictionary
    for region in master_dictionary.values():
        
        # iterate through each nested country list within overall region list
        for country_list in region:
            
            # create variables for desired data to increase readability
            diabetes_float = country_list[1]
            population_float = country_list[2]
            
            """
            calculate per capita diabetes
            if population is 0 (unknown), make per capita diabetes 0
            """
            try:
                
                diabetes_per_capita_float = diabetes_float/population_float
                
            except ZeroDivisionError:
                
                diabetes_per_capita_float = 0.0
            
            # append per capita diabetes to end of country list
            country_list.append(diabetes_per_capita_float)

    return master_dictionary

def display_region(master_dictionary, region):
    """
    print region and country diabetes data for desired region
    
    print total diabetes cases, population, and per capita diabetes for region
     and its countries
    print name and per capita diabetes of countries with highest and lowest
     per capita diabetes
    """
    
    # extract overall region data from master dictionary
    region_list = [element for element in master_dictionary[region] \
                   if element[0] == region]
    
    # create variables for desired data to increase readability
    region_str = region_list[0][0]
    region_cases_int = region_list[0][1]
    region_population_int = region_list[0][2]
    region_per_capita_int = region_list[0][3]
    
    """
    extract country lists (excluding overall region data) from master dictionary
    sort in decreasing order by per capita diabetes
    """
    country_list = sorted([element for element in master_dictionary[region] \
                    if element[0] != region], key=itemgetter(3), reverse=True)
    
    # calculate countries with max and min per capita diabetes in region
    maximum_in_region_tupl = max_in_region(master_dictionary, region)
    minimum_in_region_tupl = min_in_region(master_dictionary, region)
    
    # print region data
    print("{:<37s} {:>9s} {:>12s} {:>11s}".format("Region","Cases",\
                                                  "Population","Per Capita"))
    print("{:<37s} {:>9.0f} {:>12,.0f} {:>11.5f}".format(region_str, \
                        region_cases_int, region_population_int, \
                            region_per_capita_int))
    
    # print header for countries data
    print()
    print("{:<37s} {:>9s} {:>12s} {:>11s}".format("Country","Cases",\
                                                  "Population","Per Capita"))
    
    # iterate through each country in country list
    for country in country_list:
        
        # create variables for desired data to increase readability
        country_str = country[0]
        cases_int = country[1]
        population_int = country[2]
        per_capita_int = country[3]
        
        # print country data
        print("{:<37s} {:>9.1f} {:>12,.0f} {:>11.5f}".format(country_str, \
                                    cases_int, population_int, per_capita_int))
    
    # print max and min per capita diabetes countries data
    print("\nMaximum per-capita in the {} region".format(region))
    print("{:<37s} {:>11s}".format("Country","Per Capita"))
    print("{:<37s} {:>11.5f}".format(maximum_in_region_tupl[0], \
                                     maximum_in_region_tupl[1]))
    
    print("\nMinimum per-capita in the {} region".format(region))
    print("{:<37s} {:>11s}".format("Country","Per Capita"))
    print("{:<37s} {:>11.5f}".format(minimum_in_region_tupl[0], \
                                     minimum_in_region_tupl[1]))

def main():
    
    # initialize file object
    fp = open_file()
    
    # create master dictionary
    master_dictionary = read_file(fp)
    
    # append per capita diabetes data to aech country in master dictionary
    master_dicitonary = add_per_capita(master_dictionary)
    
    # iterate through each region in master dictionary
    for region in master_dictionary:
        
        # print region's diabetes data using display_region function
        print("Type1 Diabetes Data (in thousands)")
        display_region(master_dictionary, region)
        print("-" * 72)
    
    # print thank you message after printing data
    print('\n Thanks for using this program!\nHave a good day!')

# These two lines allow this program to be imported into other code
# such as our function_test code allowing other functions to be run
# and tested without 'main' running.  However, when this program is
# run alone, 'main' will execute.  
if __name__ == "__main__": 
    
    main()