#!/usr/bin/env python
# coding: utf-8

# In[58]:


from nltk.tokenize import  wordpunct_tokenize
from collections import Counter
import math


# In[53]:


from collections import defaultdict, Counter
#from itertools import zip
def to_ngrams( unigrams, length):
    return zip(*[unigrams[i:] for i in range(length)])  


# In[54]:


def ngram_probs(filename="EngArticle.txt"):
    bigram_info = Counter()
    trigram_info = Counter()
    bigram_probs = defaultdict(lambda:0)
    trigram_probs = defaultdict(lambda:0)

    with open('EngArticle.txt') as text_file:
        for index, line in enumerate(text_file): 
            words = wordpunct_tokenize(line.lower())
            #print(words)
            bigrams = to_ngrams(words, 2)
            trigrams = to_ngrams(words, 3)

            for bi in bigrams:
                bigram_info.update([bi])

            for tri in trigrams:
                trigram_info.update([tri])

        bi_sum = sum(bigram_info.values()) 
        tri_sum = sum(trigram_info.values())
        
    for item in bigram_info.elements():
        bigram_probs[item] = bigram_info[item] / bi_sum
    
    for item in trigram_info.elements():
        trigram_probs[item] = trigram_info[item] / tri_sum
        
    return bigram_probs, trigram_probs


# In[55]:


cnt2, cnt3 = ngram_probs()


# In[56]:


print(cnt2[('we', 'are')])
print(cnt3[('we', 'are', 'here')])


# In[89]:


def prob3(bigram, cnt2=cnt2, cnt3=cnt3):
    probs = defaultdict()
    for key, values in cnt3.items():
        probs[key[2]] = math.log(cnt3[key])  - math.log(cnt2[bigram])
    return probs


# In[90]:


p = prob3(('we', 'are'), cnt2, cnt3)


# In[91]:


print(p['family'])


# In[111]:


def predict_max(starting, cnt2= cnt2, cnt3 = cnt3):
    list_of_words = list()
    for i in starting:
        list_of_words.append(i)
    p = prob3(starting, cnt2, cnt3)
    likely_word = sorted(p.items(), key=lambda kv: kv[1], reverse = True)[0][0]
    list_of_words.append(likely_word)
    return list_of_words

sent = predict_max(('we', 'are'), cnt2, cnt3)
assert sent[-1] == '.' or len(sent) <= 15
print(' '.join(sent))


# In[ ]:




