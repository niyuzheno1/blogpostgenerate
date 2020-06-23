# THIS CODE AND INFORMATION IS PROVIDED "AS IS" WITHOUT WARRANTY O
# ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS FOR A
# PARTICULAR PURPOSE.
#
# Copyright 2020-2029 Zach (Yuzhe) Ni All rights reserved

#
# The purpose of this python program is to automatically create web pages (i.e. index.html, <posts>.html, <archivedate>.html). 


import zipfile 
import os, time, datetime

#
# Initialize all the variable
#

zipfilelist = {}
blog_description = open("blog.txt", "r")
blog = blog_description.read().split('\n')
allfile = []
bucket = { }
archive_content = ""
thumbnail = "<a href=\"page\">title</a><p></p>"
strblogpost = "<div class=\"blog-post\"><h2 class=\"blog-post-title\"> <a href=\"as2LINK2sa\"> as2TITLEs2a </a></h2><p class=\"blog-post-meta\">as2DATEs2a by <a href=\"https://github.com/niyuzheno1\">Zach Ni</a></p> as2Content2sa </div>"



#
# filtering metadata 
# 
for i in range(0,len(blog)-1,2):
    modified = os.path.getmtime(blog[i])
    Timestamped = time.ctime(modified).split(' ')[1]+' '+time.ctime(modified).split(' ')[2]+' '+time.ctime(modified).split(' ')[-1]
    Monthyearstamped = time.ctime(modified).split(' ')[1]+' '+time.ctime(modified).split(' ')[-1]
    a = {
        "filename" : blog[i], 
        "title" : blog[i+1],
        "time" : os.stat(blog[i]).st_mtime,
        "Timestamped" : Timestamped,
        "Monthyearstamped" : Monthyearstamped
    }
    allfile.append(a)

#
# Sorting posts based on time in ascending order, allfile[-1] represents the metadata for the latest modified file
#
def sortcomp(e):
    return e["time"]
allfile.sort(key=sortcomp)


#
# Initialize buckets which contain specific month/year and their respective posts
#


for x in allfile:
    bucket[x['Monthyearstamped']] = []


for x in allfile:
    bucket[x['Monthyearstamped']].append(x)



#
# Create Archive Content for different year/month
#
for x in bucket:
    filename = ""
    for i in x.split(' '):
        filename += i
    filename += ".html"
    archive_content += thumbnail.replace("page",filename).replace("title",x)


#
# Read template for blog posts
#

template_file = open("template.html", 'r')
template = template_file.read()

#
# write to specific blog html file
#

for x in allfile:
    title = x['title']
    file = x['filename']
    Timestamped = x['Timestamped']
    Monthyearstamped = x['Monthyearstamped']
    content_file = open(file, 'r')
    content = content_file.read()
    result = template.replace("<!--Content-->", content).replace("<!--TITLE-->", title).replace("<!--DATETIME-->", Timestamped).replace("<!--Archives-->", archive_content)
    html_file = open(file.replace(".txt", ".html"), "w")
    zipfilelist[file.replace(".txt", ".html")] = 1
    html_file.write(result)
    html_file.close()

#
# Read Archives html file for creating specific datetime.html files and create them
# 

content_file = open("Archives.html", 'r')
content = content_file.read()


for x in bucket:
    date = x
    filename = ""
    for i in date.split(' '):
        filename += i
    filename += ".html"
    post = ""
    for y in bucket[x]:
        title = y['title']
        file = y['filename']
        post += thumbnail.replace("page",file.replace(".txt", ".html")).replace("title",title)
    result = content.replace("<!--DATETIME-->",date).replace("<!--POST-->",post).replace("<!--Archives-->",archive_content)
    html_file = open(filename, "w")
    zipfilelist[filename] = 1
    html_file.write(result)
    html_file.close()




#
# Write to index file
#

bp = ""
count = 0
for y in range(len(allfile)-1,-1,-1):
    count = count + 1
    x = allfile[y]
    if count > 3:
        break
    content_file = open(x['filename'], 'r')
    content = content_file.read()
    htmltext = x['filename'].replace(".txt",".html")
    bp += strblogpost.replace("as2TITLEs2a",x['title']).replace("as2DATEs2a",x['Timestamped']).replace('as2Content2sa',content).replace("as2LINK2sa",htmltext )

content_file = open("index32.html", 'r')
content = content_file.read()
result = content.replace("<!--BlogPost-->",bp).replace("<!--Archives-->", archive_content)
html_file = open("index.html", "w")
zipfilelist["index.html"] = 1
html_file.write(result)
html_file.close()


from zipfile import ZipFile

# zip related html pages

with ZipFile('pages.zip', 'w') as myzip:
    for file in zipfilelist: 
        myzip.write(file) 





