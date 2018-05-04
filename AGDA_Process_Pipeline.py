
# coding: utf-8

# In[1]:

import requests
from PIL import Image
from colorthief import ColorThief


# In[3]:

#Loading Image URL from API
r = requests.get('https://agda-fyp.herokuapp.com/load')
data = r.json()
#print(len(data))


# In[3]:


#Data seperation
imgs = []
syms = []
vis =[]
kwd = []
colors = []
for it,i in enumerate(data[:150]):
    #Loading Images
    try:
        r = requests.get(i['url'],stream=True).raw
        
        try:
            img = Image.open(r).convert('RGBA').resize((50,50))
            imgs.append(img)
            f= 'temp/img'+str(it)+'.jpg';
            img.save(f);
            color_thief = ColorThief(f)
            colors.append(color_thief.get_palette(color_count=3))
            #Labels 
            syms.append([i['align'],i['symmetry'],i['balance']])
            vis.append([i['color_r'],i['font_r']])
            kd = i['keyword'].split(';')
        except IOError:
            print("Load Error")
            colors.append(None)
            #Labels 
            syms.append(None)
            vis.append(None)
            kd = None
        kwd.append(kd)
    except requests.exception.RequestException as e:
        print("Network Error")



# In[7]:

colordic = {}
for i in range(len(colors)):
    if colors[i] is not None:
        for c in colors[i]:
            if not c is None:
                for k in kwd[i]:
                    key = str(c)
                    if not (key in colordic and colordic[key]['keyword']==k):
                        colordic.update({key:{'keyword':k, 'cr':vis[i][0]}})
                    else:
                        icr = (colordic[key]['cr']+vis[i][0])/2
                        colordic.update({key:{'keyword':k, 'cr':icr}})
print(str(colordic))
f = open('temp/colortable', 'w')
f.write(str(colordic))
f = open('temp/syms', 'w')
f.write(str(syms))
f = open('temp/vis', 'w')
f.write(str(vis))
f = open('temp/kwd', 'w')
f.write(str(kwd))




# In[8]:

tkwd=[]
it=0
tsyms=[]
tvis=[]
imgs=[]
for it,i in enumerate(data[150:]):
    try:
    #Loading Images
        r = requests.get(i['url'],stream=True).raw
        try:
            img = Image.open(r).convert('RGBA').resize((50,50))
            imgs.append(img)
            f= 'test/img'+str(it)+'.jpg';
            img.save(f);
            it= it+1
            tsyms.append([i['align'],i['symmetry'],i['balance']])
            tvis.append([i['color_r'],i['font_r']])
            kd = i['keyword'].split(';')
            tkwd.append(kd)
        except IOError:
            print("Load Error")
            #Labels 
            tsyms.append(None)
            tvis.append(None)
            kd = None
        tkwd.append(kd)
    except requests.exception.RequestException as e:
        print("Network Error")
    


# In[15]:

f = open('test/tkwd', 'w')
f.write(str(tkwd))
f = open('test/tsyms', 'w')
f.write(str(tsyms))
fo = open('test/tvis', 'w')
fo.write(str(tvis))


# In[ ]:



