#Required libraries
from collections import Counter
#Our class
class AutoCorrection():
    def __init__(self,words,alphabets):
        self.words=words
        self.alphabets=alphabets
        self.probs={}
        self.words_cnt={}
        self.vocabs=set(words)
    '''
    This method for getting each word frequency
    '''
    def get_count(self):
        self.words_cnt=Counter(self.words)
        return self.words_cnt
    '''
    This method for calculating the probability for each word
    '''
    def get_probs(self):
        sm=sum(self.words_cnt.values())
        for key,value in self.words_cnt.items():
            self.probs[key]=value/sm
        return self.probs
    '''
    This method support some operations that's need for editing words
    '''
    def transform(self,word):
        delete=[]
        switch=[]
        replace=[]
        insert=[]
        #Delete 
        for i in range(len(word)):
            delete.append(word[:i]+word[i+1:])
        #Switch
        for i in range(len(word)):
            if len(word[i:])>=2:
                switch.append(word[:i]+word[i+1]+word[i]+word[i+2:])
        #Replace
        for i in range(len(word)):
            for c in self.alphabets:
                if len(word)-i>=1 and word[i]!=c:
                    replace.append(word[:i]+c+word[i+1:])
            _replace=sorted(replace)
        #Insert
        for i in range(len(word)):
            for c in self.alphabets:
                insert.append(word[:i]+c+word[i:])
        return delete+switch+_replace+insert
    '''
    Lets suppose our words need to edit in one letter
    '''
    def edit_one_letter(self,word):
        edit_set=set(self.transform(word))
        return edit_set
    '''
    Lets suppose our words need to edit in two letters
    '''
    def edit_two_letters(self,word):
        edit_set=set()
        for w1 in self.edit_one_letter(word):
            for w2 in self.edit_one_letter(word):
                edit_set.add(w2)
        return edit_set
    '''
    Lets get our words correction
    '''
    def get_correction(self,word):
        best_sug=[]
        #Lets check if this word in our vocabs
        in_vocabs=self.vocabs.intersection([word])
        #Lets see if this word in our editing method for one letter
        st_1_letter=self.edit_one_letter(word)
        one_letter=self.vocabs.intersection(st_1_letter)
        #Lets see if our word in our editing method for two letters
        st_2_letters=self.edit_two_letters(word)
        two_letters=self.vocabs.intersection(st_2_letters)
        #Lets obtain our suggestions words from in_vocabs,one_letter and two letters
        suggestion={word:self.probs.get(word,0) for word in in_vocabs or one_letter or two_letters}
        #Lets sort our suggestions by using values and obtain best two suggestions
        best_sug=sorted(suggestion.items(),key=lambda item:item[1],reverse=True)[:2]
        return best_sug