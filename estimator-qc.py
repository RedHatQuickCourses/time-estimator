# Calculate the read speed of Red Hat Training adoc files
# Specifically for Quick Course format
  

import os
import math
import sys
import glob
  
#The average reading speed in words per minute for adults
reading_speed = 180
#The time to 'read' each image in seconds
image_view_time = 60
#The time it takes to read a code block in seconds
code_time = 30
#Paths and patterns
path = './'
module_dir = 'modules/'
chapter_dir = 'chapter*/'
page_dir = 'pages/'
file_type = '*.adoc'
time_estimate_attr = ':time_estimate:'

# Count number of characters, words, spaces and lines in a file

# TODO: split into functions
def element_counter(fname):
    in_code_block = False
    # total word count
    num_words = 0
    # total images
    num_images = 0
    # total code blocks
    num_code_blocks = 0
    # total estimated time
    time_est = 0
    # file that is read, edited, and written
    page_file = []

    # open file
    with open(fname, 'r') as f:
        page_file = f.readlines()

    
    # go through page to count elements for calculation
    for line in page_file:
        # separating a line from \n character and storing again in line
        line = line.strip(os.linesep)

        # split line into word array
        words_list = line.split()
        
        # count elements
        if (len(words_list) > 0):
            if (words_list[0].startswith('image::')):
                # count number of images
                num_images = num_images + 1
            elif (words_list[0].startswith('----')):
                if in_code_block:
                    #End the codeblock and resume counting words
                    num_code_blocks = num_code_blocks + 1
                    in_code_block = False
                else:
                    #First line in code block
                    in_code_block = True
            elif ((not words_list[0].startswith('//')) and (not in_code_block)):
                # add words in this line to total words
                num_words = num_words + len(words_list)
    
    # sum up totals
    time_est = get_time_estimate(num_words, num_images, num_code_blocks)

    # find and remove old time estimate if existing
    for index, line in enumerate(page_file):
        words_list = line.split()
        if (len(words_list)):
            # if found...
            if (words_list[0].startswith(time_estimate_attr)):
                # delete
                del(page_file[index])
            
    # add time estimate (or updated estimate if existing)
    page_file.append(time_estimate_attr + ' ' + time_est + ' min.')

    # open again to write new time estimate
    with open(fname, 'w') as f:
        f.writelines(page_file)

# summ times per section and return time estimate
def get_time_estimate(word_count, image_count, code_block_count):
    # Start with base level word count and average speed
    reading_time = round(word_count/reading_speed, 2)

    #Add time for images, convert seconds to minutes
    image_time = (image_count * image_view_time) / 60

    #add time for code blocks, convert time to minutes
    code_block_time = (code_block_count * code_time) / 60

    reading_time = reading_time + image_time + code_block_time

    # round up
    return repr(math.ceil(reading_time))


# Find relevant files
def directory_process():
    # find chapters in modules/
    chapter_list = glob.glob(path + module_dir + chapter_dir, recursive=False)

    # iterate through chapter modules
    for chapter in chapter_list:
        # find adoc files but exclude index.adoc
        adoc_list = [f for f in glob.glob(
            chapter + page_dir + file_type) if 'index' not in f]
        if (len(adoc_list) <= 0):
            print('No relevant files found in directory')
        else:
            for doc in adoc_list:
                element_counter(doc)

if __name__ == '__main__':
    try:
        directory_process()
    except Exception as e: 
        print(e)