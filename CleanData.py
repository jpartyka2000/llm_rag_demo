import re
import string
import sys

import nltk
from nltk.corpus import stopwords

class CleanData:
    
    def __init__(self, filter_punctuation=True, filter_nonascii_chars=True, filter_pronouns=True, filter_contractions=True):
        
        #fields
        self.stopwords_list = []
        self.filter_punctuation = filter_punctuation
        self.filter_nonascii_chars = filter_nonascii_chars
        self.filter_pronouns = filter_pronouns
        self.filter_contractions = filter_contractions
        
        #method initializations
        self.init_stopword_list(filter_pronouns, filter_contractions)
    
    
    def get_stopword_list(self):
        return self.stopwords_list
        

    def init_stopword_list(self, filter_pronouns, filter_contractions):
        
        #download stopword list if necessary
        nltk.download('stopwords')

        #get the English stopwords list
        english_stopwords_list = stopwords.words('english')
        
        #add pronouns if desired
        if self.filter_pronouns:
        
            english_pronouns = [
                "I", "you", "he", "she", "it", "we", "they",
                "me", "you", "him", "her", "us", "them",
                "my", "your", "his", "her", "its", "our", "their",
                "mine", "yours", "his", "hers", "ours", "theirs",
                "myself", "yourself", "himself", "herself", "itself", "ourselves", "yourselves", "themselves",
                "who", "whom", "whose", "which", "what", "that", "whosever", "whosoever", "whatever", "whichever",
                "this", "these", "those", "each", "every", "either", "neither", "both", "all", "any", "some", "many", "few", "several", "none"]

            english_stopwords_list.extend(english_pronouns)
        
        #add contractions if desired
        if self.filter_contractions:
        
            english_contractions = [
                "ain't", "aren't", "can't", "could've", "couldn't", "didn't", "doesn't", "don't", "hadn't", "hasn't", "haven't",
                "he'd", "he'll", "he's", "how'd", "how'll", "how's", "I'd", "I'll", "I'm", "I've", "isn't", "it'd", "it'll",
                "it's", "might've", "mightn't", "must've", "mustn't", "shan't", "she'd", "she'll", "she's", "should've",
                "shouldn't", "that'll", "that's", "there'd", "there'll", "there's", "they'd", "they'll", "they're", "they've",
                "wasn't", "we'd", "we'll", "we're", "we've", "weren't", "what'd", "what'll", "what're", "what's", "what've",
                "where'd", "where'll", "where's", "who'd", "who'll", "who's", "won't", "would've", "wouldn't", "you'd",
                "you'll", "you're", "you've"]

            english_stopwords_list.extend(english_contractions)
        
        #finalize self.stopword_set
        self.stopwords_list = list(set(english_stopwords_list))
    
    
    def remove_excess_whitespace(self, text_str):

        #all I will do here is 
        #(a): remove any instance of whitespace on a given line that is > 1 characters long 
        #(b): remove newline characters
        
        #(a)
        text_no_whitespace_str = re.sub(r'\s+', ' ', text_str)
        
        #(b)
        text_no_whitespace_str = text_no_whitespace_str.replace('\n','')
        
        return text_no_whitespace_str
    
    
    def remove_punctuation(self, text_str):
                
        punctuation_regex_str = '[' + re.escape(string.punctuation) + ']'
        text_no_punctuation_str = re.sub(punctuation_regex_str, ' ', text_str)
        
        return text_no_punctuation_str

    
    def remove_nonascii_characters(self, text_str):
                
        text_no_ascii_str = re.sub(r'[^\x00-\x7F]', '', text_str)
                
        return text_no_ascii_str
            
        
    def remove_stopwords(self, text_str):
        
        #get text_str as a list of words
        text_word_list = text_str.split()
        
        filtered_text_str = ' '.join([this_word for this_word in text_word_list if this_word.lower() not in self.stopwords_list])
        
        return filtered_text_str
    
    
    def clean_text(self, text_str):

        text_str = self.remove_excess_whitespace(text_str)
        
        if self.filter_punctuation:
            text_str = self.remove_punctuation(text_str)
        
        if self.filter_nonascii_chars:
            text_str = self.remove_nonascii_characters(text_str)
        
        text_str = self.remove_stopwords(text_str)
        

        return text_str