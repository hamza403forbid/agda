
# coding: utf-8

# In[14]:

import numpy as np
def get_CR(A,K):    
    f = open('temp/colortable','r')
    ct = eval(f.read())
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

from PIL import Image
from colorthief import ColorThief
fo = open('test/tkwd','r')
tkwd = eval(fo.read())
fo = open('test/tvis','r')
tcr = eval(fo.read())
tcol=[]



# In[11]:

import os
for file in os.listdir("test"):
    if file.endswith(".jpg"):
        f=os.path.join("test", file)
        color_thief = ColorThief(f)
        tcol.append(color_thief.get_palette(color_count=3))


# In[12]:

print(tcol)


# In[15]:

accr = []
for i in range(len(tcol)):
    rel=[]
    for c in tcol[i]:
        for k in tkwd[i]:
            rel.append(get_CR(np.array(list(c)),k))
    rel = np.array(rel)
    cr = rel.mean()
    accr.append(100-((abs(cr-tcr[i][0])/tcr[i][0])*100))
accr = np.array(accr)
print(accr.mean())


# In[19]:




# In[20]:

print(accr)


# In[15]:




# In[ ]:



