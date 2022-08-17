"""
CSE Project #9 - JSON File Reader

Description

    This program calculates and displays data on images and their categories from
    JSON files. It is implemented using a driver (this file) and functions within
    the Python interpreter. The JSON image file is "small.json" and the categories
    are obtained from "category.txt"
    For a detailed description of the program, read "Project09.pdf"

Notable Concepts

    JSON file reading, data extraction, dictionaries, functions, try-except statements,
    json module, string module

Algorithm

    create master dictionary of images and their category words
        prompt for desired JSON file and ensure it's valid
        initialize file object
        extract each category and its numeric id and add to dictionary
    
    create master dictionary of categories and their numeric ids
        prompt for desired category file and ensure it's valid
        initialize file object
        extract each image and its category data and add to dictionary
    
    calculate desired information
        prompt for desired option and ensure it's value
        if c:
            create alphabetical list of unique categories in JSON file
        if f:
            prompt for desired unique category
            create list, sorted in increasing order, of images in which unique
             category appeared
        if i:
            create tuple of category with max occurrences and its occurence count
        if m:
            create tuple of category that appears in most images and its image count
        if w:
            prompt for desired number of top-occuring categories
            reate list of desired number of top-occuring categories and their counts
        no information caltulation for option q
    
    print results
    
    reprompt for option unless option was q
"""

import json,string

"""
contains uninteresting words
used in count_words
"""
STOP_WORDS = ['a','an','the','in','on','of','is','was','am','I','me','you','and','or','not','this','that','to','with','his','hers','out','it','as','by','are','he','her','at','its']

# list of valid options used in get_option
OPTIONS = ["c", "f", "i", "m", "w", "q"]

# used in get_option()
MENU = '''
    Select from the menu:
        c: display categories
        f: find images by category
        i: find max instances of categories
        m: find max number of images of categories
        w: display the top ten words in captions
        q: quit
        
    Choice: '''

def get_option():
    """
    prompt user for option and return it

    if option not valid, display error message and reprompt until valid option input
    """


    option_str = input(MENU).lower()
   
    while option_str not in OPTIONS:
        
        print("Incorrect choice.  Please try again.")
        
        option_str = input(MENU).lower()
        
    return option_str

def open_file(s):
    """
    return file pointer for desired file

    if file not valid, reprompt for file until valid file input
    """
   
    
    while True:

        try:

            fp = open(input("Enter a {} file name: ".format(s)))
            break
       
        except FileNotFoundError:
            
            print("File not found.  Try again.")
            
    return fp

def read_annot_file(fp1):
    """
    extract data from JSON file and return master dictionary of dictionaries
    """
    
    D_annot = json.load(fp1)
    
    return D_annot

def read_category_file(fp2):
    """
    return dictionary of data from category file

    dictionary keys are integers in each file line
    dictionary values are strings in each file line
    """
    
    # initiale dictioary of categories
    D_cat = {}
    
    # initiate list that holds line data
    line_contents_list = []
    
    # iterate through each line in file
    for line in fp2:
        
        # create list of integer and string in line
        line_contents_list = line.split()
        
        # create variables for desired data to increase readability
        dictionary_key = int(line_contents_list[0])
        dictionary_value = line_contents_list[1] 
        
        # create dictionary entry with integer as key and string as value
        D_cat[dictionary_key] = dictionary_value
        
    return D_cat

def collect_catogory_set(D_annot,D_cat):
    """
    return categories used in JSON file
    """
    
    # sets used for data retrieval
    D_annot_category_ints_set = set()
    D_annot_category_strs_set = set()
    
    # iterate through value of each D_annot key
    for image_dict in D_annot.values():
        
        # iterate through each each nested dictionary
        for key, value in image_dict.items():
            
            # access bbox_category_label list
            if key == "bbox_category_label":
                
                # iterate through each category number in list
                for category_int in value:
                    
                    # add category number to set
                    D_annot_category_ints_set.add(category_int)
    
    # iterate through each category number in set
    for category_int in D_annot_category_ints_set:
        
        # word that corresponds to category number
        category_str_counterpart_str = D_cat[category_int]
        
        # add word to set
        D_annot_category_strs_set.add(category_str_counterpart_str)
    
    return D_annot_category_strs_set

def collect_img_list_for_categories(D_annot,D_cat,cat_set):
    """
    return dictionary that shows what images contained which categories

    dictionary keys are categories in JSON file
    dictionary values are image ids of images that contain category
    """
    
    # dictionary with categories as keys and lists of image ids as values
    imgs_containing_category_dict = {}
    
    # create dictionary keys for each category used in JSON file
    for category_str in cat_set:
        
        imgs_containing_category_dict[category_str] = []

    # iterate through value of each D_annot key
    for image_id, image_dict in D_annot.items():

        # iterate through each each nested dictionary
        for key, value in image_dict.items():
            
            # access bbox_category_label list
            if key == "bbox_category_label":
                
                # iterate through each category number in list
                for category_int in value:
                    
                    # word that corresponds to category number
                    category_str_counterpart_str = D_cat[category_int]
                    
                    # add image id to category's list in dictionary
                    imgs_containing_category_dict[category_str_counterpart_str] \
                    .append(image_id)

    # sort each category's list of image ids in increasing order
    for img_list in imgs_containing_category_dict.values():
        
        img_list.sort()
        
    return imgs_containing_category_dict

def max_instances_for_item(D_image):
    """
    return tuple of most-often-occurring category and its occurrence count

    tuple in form (count (int), category (str))
    """

    return max([(len(value), key) for key, value in D_image.items()])

def max_images_for_item(D_image):
    """
    return tuple of most-often-occurring category and its occurrence count

    only one occurrence counted per image
    tuple in form (count (int), category (str))
    
    """
    
    return max([(len(set(value)), key) for key, value in D_image.items()])

def count_words(D_annot):
    """
    return list of tuples containing caption words and their counts
    
    words in STOP_WORDS and numerals ignored
    list sorted in decreasing order
    """
    
    # used to create word count list
    word_count_dict = {}
    
    # will hold tuples of caption words and their counts
    word_count_list = []
    
    # iterate through value of each D_annot key
    for image_dict in D_annot.values():
        
        # iterate through each each nested dictionary
        for key, string_list in image_dict.items():
            
            # access cap_list
            if key == "cap_list":
                
                # iterate through each string in list
                for caption_str in string_list:
                    
                    # will hold stripped words
                    caption_string_list = []
                    
                    # iterate through each word in string
                    for word in caption_str.split():
                        
                        # strip word of punctuation
                        stripped_word_str = word.strip(string.punctuation)
                        
                        """
                        add word to list if it is interesting, not a numeral,
                         and not an empty string
                        """
                        if not (stripped_word_str in STOP_WORDS \
                                or stripped_word_str.isnumeric()) and \
                            stripped_word_str != "":
                            
                            caption_string_list.append(stripped_word_str)
                    
                    # iterate through each word in caption word list
                    for word in caption_string_list:
                        
                        """
                        if word not in dictionary, add it as a key with a value
                         of 1
                        if word in dictionary, add 1 to its value
                        """
                        if not word in word_count_dict:
                            
                            word_count_dict[word] = 1
                            
                        else:
                            
                            word_count_dict[word] += 1
                            
    # append each word and its count to word count list in (count, word) format
    for word, count in word_count_dict.items():
        
        word_count_list.append((count, word))
    
    # sort list in decreasing order
    word_count_list.sort(reverse=True)
    
    return word_count_list

def main():
    
    # print heading
    print("Images\n")
    
    # create file objects for JSON and category files
    fp1 = open_file("JSON image")
    fp2 = open_file("category")
    
    # dictionary of image ids and their data
    D_annot = read_annot_file(fp1)
    
    # dictionary of categories and their corresponding numbers
    D_cat = read_category_file(fp2)
    
    # set of category words used in JSON file's images
    cat_set = collect_catogory_set(D_annot, D_cat)
    
    # dictionary of categories and the ids of images that contain them
    D_image = collect_img_list_for_categories(D_annot, D_cat, cat_set)
    
    # initial prompt for option
    option_str = get_option()
    
    # contains all non-1 options
    while option_str != "q":
        
        # list of categories words used in JSON file's images
        cat_list = []
            
        # add each category word in cat_set to cat_list
        for category in cat_set:
            
            cat_list.append(category)
        
        # sort list alphabetically
        cat_list.sort()
        
        # string that lists category words in cat_list
        categories_str = ", ".join(cat_list)
        
        # alphabetical category names
        if option_str == "c":
            
            print("\nCategories:")
            print(categories_str)
            
        # list of unique images containing desired category
        if option_str == "f":
            
            # print alphabetical category names
            print("\nCategories:")
            print(categories_str)
            
            # prompt for desired category
            cat_choice_str = \
                input("Choose a category from the list above: ").lower()
            
            """
            ensure desired category appeared in JSON file's images
            
            if it didn't, display error message and reprompt until input is
             category that did
            """
            while not cat_choice_str in categories_str:
                
                print("Incorrect category choice.")
                
                cat_choice_str = \
                    input("Choose a category from the list above: ").lower()
                
            # used to find unique images desired category appeared in
            final_img_int_list = []
            final_img_str_list = []
            
            # iterate through each word-image list pair in dictionary
            for word, img_list in D_image.items():
                
                # find dictionary entry for desired category
                if word == cat_choice_str:
                    
                    # iterate through each image in list
                    for img_id_int in img_list:
                        
                        # append integer of image to list if not already in it
                        if not int(img_id_int) in final_img_int_list:
                        
                            final_img_int_list.append(int(img_id_int))
            
            # sort list in increasing order
            final_img_int_list.sort()
            
            # append string of each image to string-equivalent of list
            for img_id_int in final_img_int_list:
                
                final_img_str_list.append(str(img_id_int))
            
            # print results
            print("\nThe category {} appears in the following images:" \
                  .format(cat_choice_str))
            print(", ".join(final_img_str_list))
            
        # category with max occurrences
        if option_str == "i":
            
            # tuple of category with max occurrences and its count of occurences
            max_instances_tupl = max_instances_for_item(D_image)
            
            # create variables for desired data to increase readability
            max_instances_word_str = max_instances_tupl[1]
            max_instances_count_int = max_instances_tupl[0]
            
            # print results
            print("\nMax instances: the category {} appears {} times in images." \
                  .format(max_instances_word_str, max_instances_count_int))
        
        # category in most pictures
        if option_str == "m":
            
            # tuple of category in most pictures and its count of pictures
            max_images_tupl = max_images_for_item(D_image)
            
            # create variables for desired data to increase readability
            max_images_word_str = max_images_tupl[1]
            max_images_count_int = max_images_tupl[0]
            
            # print results
            print("\nMax images: the category {} appears in {} images." \
                  .format(max_images_word_str, max_images_count_int))
            
        # top-occurring words
        if option_str == "w":
        
            # prompt for desired number of top-occuring words to show
            desired_words_int = int(input("\nEnter number of desired words: "))
            
            """
            ensure desired number is greater than 0
            if it's not, display error message and reprompt until it is
            """
            while desired_words_int <= 0:
            
                print("Error: input must be a positive integer: ")
                
                desired_words_int = int(input("\nEnter number of desired words: "))
        
            # all categories and their counts
            total_word_count_list = count_words(D_annot)
            
            # desired number of categories and their counts
            desired_word_count_list = total_word_count_list[:desired_words_int]
            
            # print results
            print("\nTop {} words in captions.".format(desired_words_int))
            print("{:<14s}{:>6s}".format("word","count"))
            
            for word_tupl in desired_word_count_list:
                
                word_str = word_tupl[1]
                word_count_int = word_tupl[0]
                
                print("{:<14s}{:>6d}".format(word_str, word_count_int))
        
        
        
        # reprompt for option
        option_str = get_option()
        
    # deconstruct file pointers and print closing message if option is q
    else:
        
        fp1.close()
        fp2.close()

        print("\nThank you for running my code.") 
    
# Calls main() if this modules is called by name
if __name__ == "__main__":
    
    main()