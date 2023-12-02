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
year = 2023
day = '1'

file_path = os.path.dirname(os.path.abspath(__file__)) + os.sep
input_file_path = file_path + 'html.txt'
output_file = 'README_temp.md'

# Input ------------------------------------------------------------
with open(input_file_path) as f:
    html = f.read()
    
soup = BeautifulSoup(html, "html.parser")

h2 = soup.find('h2')
day_title = ''
print('Reading HTML')
if h2:
    day = re.findall(r'\d+', h2.text)[0]
    s = h2.text.split(':')[1]
    day_title = ''.join([c for c in s if c.isalpha() or c==' ']).strip()
    print('\t-' + f'Day found from HTML: {day}')
day_correct = not input('Is the day found correct? (Leave empty for YES)')
if not day_correct:
    quit()

# Does the Folder already exist -----------------------------------------
day = day.zfill(2)
output_folder = glob.glob(file_path + str(year) + os.sep + 'Day' + day + '*')
if output_folder: 
    output_folder = output_folder[0]
else:
    print('Could not find folder for output')
    new_folder = "Day" + day + "-" + day_title
    print(f'Would you like to create the folder? -- "{new_folder}"')
    create_folder = not input('Leave empty for YES ')
    if create_folder:
        output_folder = file_path + str(year) + os.sep + new_folder
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
    with open(output_file_path,'r') as f:
        lines = f.read()
        print(f'{type(lines)=}')

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
