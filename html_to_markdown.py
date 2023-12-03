'''
TODO: 
- keep "comment" section from existing README.md
- try getting active user session using COOKIES
- read first <article> as Title<h1>, and manually add a "Problem 1" <h2>
    - strip '-' and ' '
- remove spaces from folder name
-------------------------------------
To Run: 
    - Get HTML of Problem's Page, regardless of browser the steps 
    for this should remain relatively the same
        - right click page
        - choose Inspect
        - right click top most element that begins with "<html"
        - copy > copy element
    - paste the contents into the file: "html.txt"
'''

import os
from bs4 import BeautifulSoup # pip install beautifulsoup4
from markdownify import markdownify
import glob
import logging
import re


# Configuration ------------------------------------------------------
year_sub_folder = '2023' + os.sep # leave variable empty if repository is for the year or this script is already in that sub-folder
day = '1'

file_path = os.path.dirname(os.path.abspath(__file__)) + os.sep
input_file_path = file_path + 'html.txt'
output_file = 'README_temp.md'

def re_list_dir(folder_path='.', pattern=r'.*'):
    file_list = []
    pattern_regex = re.compile(pattern)

    # Iterate through all files in the folder
    for dir in os.listdir(folder_path): 
        # Check if the file name matches the pattern
        if pattern_regex.search(dir):
            file_list.append(dir) # os.path.join(folder_path, dir))

    return file_list
print(f'{day=}')
output_folder = re_list_dir(file_path + year_sub_folder, r'^[^a-zA-Z]*(D|d)ay[^a-zA-Z0-9]?0?' + day)
print(output_folder)
quit()
# Input ------------------------------------------------------------
with open(input_file_path) as f:
    html = f.read()
    
soup = BeautifulSoup(html, "html.parser")

h2 = soup.find('h2')
day_title = ''
title = ''
print('Reading HTML')
if h2:
    day = re.findall(r'\d+', h2.text)[0]
    title = h2.text
    for i,char in enumerate(title):
        if char.isalpha(): break
    print('New text: "' + title[:i] + 'Problem 1' + title[-i:] + '"')
    title = '# ' + title[i:-i]
    
    new_h2 = soup.new_tag('h2')
    h2.text = title[:i] + 'Problem 1' + title[:i]


    s = h2.text.split(':')[1]
    day_title = ''.join([c for c in s if c.isalpha() or c==' ']).strip()
    print('\t-' + f'Day found from HTML: {day}')

print(f'{title=}')
quit()
day_correct = not input('\t'+'Is the day found correct? (Leave empty for YES)')
if not day_correct:
    quit()

# Does the Folder already exist -----------------------------------------
day = day.zfill(2)
output_folder = glob.glob(file_path + year_sub_folder + '(D|d)ay' + day + '*')
if output_folder: 
    output_folder = output_folder[0]
else:
    print('Could not find folder for output')
    new_folder = "Day" + day + "-" + day_title
    print(f'Would you like to create the folder? -- "{new_folder}"')
    create_folder = not input('Leave empty for YES ')
    if create_folder:
        output_folder = file_path + year_sub_folder + os.sep + new_folder
        os.mkdir(output_folder)
        with open (output_folder + os.sep + 'day' + day + '.py','w') as f: pass
        with open (output_folder + os.sep + 'day' + day + '_input.txt','w') as f: pass
    else: 
        quit()

# Does the Markdown file exist ----------------------------------------
output_file_path = output_folder + os.sep + output_file
print(output_file_path)

comments = '\n\n## Comments / Notes\n'
if os.path.isfile(output_file_path):
    print('Existing markdown file found')
    with open(output_file_path,'r') as f:
        lines = f.read().split('\n')
        print(f'{type(lines)=}')
        comment_pattern = r'^#+.*comment'
        found_comment=False
        for line in lines:
            if found_comment and re.match(comment_pattern,line.lower()):
                found_comment=True
                print('\t' + '- Comment section found. Remaining markdown will be saved.')
                comments = line
            elif found_comment:
                comments += '\n' + line     

# Remove Answers and non-needed info -------------------------------
output = ''
arts = soup.find_all('article')
for art in arts:
    for elem in art.find_all('p'):
        if elem.find(text=re.compile(f'Your puzzle answer .*')):
            # print(elem)
            elem.decompose()
            # Now find all following elements and remove them
            for sibling in elem.find_next_siblings():
                # if sibling.name == "article":
                #    break
                # print(f'\t-{sibling}')
                sibling.decompose()
    output += markdownify(str(art), heading_style="ATX")

output += comments

quit()

# Output ------------------------------------------------------------
with open (output_file_path,'w') as f:
    f.write(md)
