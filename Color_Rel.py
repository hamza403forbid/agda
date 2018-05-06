import requests
import os
from colorthief import ColorThief
import numpy as np
import random

def get_CR(A,K):    
    ct = colordic
    colors=[]
    for key,val in ct.items():
        colors.append(list(eval(key)))
    X = np.array(colors)
    distance = 1000000000     # better would be : +infinity
    closest = None
    closest = sorted(X, key=lambda p: sum((p - A)**2))
    accr_width=5
    closest = closest[:accr_width]
    c = str(tuple(A))
    cr=0
    if c in ct and ct[c]['keyword']==K:
        cr=ct[c]['cr']
    else:
        i=0
        while i<accr_width:
            c=str(tuple(closest[i]))
            cr+=ct[c]['cr']
            i= i+1
    cr= cr/accr_width
    return cr


# In[10]:


r = requests.get('https://agda-fyp.herokuapp.com/load')
data = r.json()
random.shuffle(data)
kwd = []
colors = []
color_rel =[]
it=0
x=int(os.environ.get('X',5))
y=int(os.environ.get('Y',7))
for i in data[:x]:
    print(it)
    r = requests.get(i['url'],stream=True).raw
    check = False
    try:
        color_thief = ColorThief(r)
        colors.append(color_thief.get_palette(color_count=3))
        check = True
    except IOError:
        print("Load Error")
        check = False
    if check:
        
        color_rel.append(i['color_r'])
        kd = i['keyword'].split(';')
        kwd.append(kd)
        it=it+1       
    
test_kwd = []
test_colors = []
test_color_rel =[]
it=0
for i in data[x:y]:
    print(it)
    r = requests.get(i['url'],stream=True).raw
    check = False
    try:
        color_thief = ColorThief(r)
        test_colors.append(color_thief.get_palette(color_count=3))
        check = True
    except IOError:
        print("Load Error")
        check = False
    if check:
        test_color_rel.append(i['color_r'])
        kd = i['keyword'].split(';')
        test_kwd.append(kd)
        it=it+1
        

colordic = {}
for i in range(len(colors)):
        for c in colors[i]:
                for k in kwd[i]:
                    key = str(c)
                    if not (key in colordic and colordic[key]['keyword']==k):
                        colordic.update({key:{'keyword':k, 'cr':color_rel[i]}})
                    else:
                        icr = (colordic[key]['cr']+color_rel[i])/2
                        colordic.update({key:{'keyword':k, 'cr':icr}})

accr=[]
for i,img in enumerate(test_colors):
    rel=[]
    for color in img:
        for keyword in test_kwd[i]:
            rel.append(get_CR(color,keyword))
    
    calculated_color_rel= np.array(rel).mean()
    if test_color_rel[i]>0:
        acc= 100-((abs(calculated_color_rel-test_color_rel[i])/test_color_rel[i])*100)
        accr.append(acc)
print(np.array(accr).mean())