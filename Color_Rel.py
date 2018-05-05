import requests
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
x=20
y=35
for i in data[:x]:
    print(it)
    r = requests.get(i['url'],stream=True).raw
    try:
        color_thief = ColorThief(r)
        colors.append(color_thief.get_palette(color_count=3))
        #Labels
        color_rel.append(i['color_r'])
        kd = i['keyword'].split(';')
        kwd.append(kd)
    except IOError:
        print("Load Error")
        if it>0:
            colors.pop()
            color_rel.pop()
            kwd.pop()
        colors.append(None)
        color_rel.append(None)
        kwd.append(None)
    it=it+1

test_kwd = []
test_colors = []
test_color_rel =[]
it=0
for i in data[x:y]:
    print(it)
    r = requests.get(i['url'],stream=True).raw
    try:
        color_thief = ColorThief(r)
        test_colors.append(color_thief.get_palette(color_count=3))
        #Labels
        test_color_rel.append(i['color_r'])
        kd = i['keyword'].split(';')
        test_kwd.append(kd)
    except IOError:
        print("Load Error")
        if it>0:
            test_colors.pop()
            test_color_rel.pop()
            test_kwd.pop()
        test_colors.append(None)
        test_color_rel.append(None)
        test_kwd.append(None)
    it=it+1

colordic = {}
for i in range(len(colors)):
    if colors[i] is not None:
        for c in colors[i]:
            if not c is None:
                for k in kwd[i]:
                    key = str(c)
                    if not (key in colordic and colordic[key]['keyword']==k):
                        colordic.update({key:{'keyword':k, 'cr':color_rel[i]}})
                    else:
                        icr = (colordic[key]['cr']+color_rel[i])/2
                        colordic.update({key:{'keyword':k, 'cr':icr}})
print(str(colordic))

accr = []
for i in range(len(test_colors)):
    rel=[]
	if test_colors[i] is not None:
		for c in test_colors[i]:
			if test_kwd[i] is not None:
				for k in test_kwd[i]:
					rel.append(get_CR(np.array(list(c)),k))
    if len(rel) > 0:
        rel = np.array(rel)
        cr = rel.mean()
        if test_color_rel[i] is not None and (test_color_rel[i] != 0):
            acc = 100-((abs(cr-test_color_rel[i])/test_color_rel[i])*100)
            if acc != -np.inf and acc != np.inf:   
                accr.append(acc)
accr = np.array(accr)
print(accr.mean())
print(accr)
