# -*- coding: iso-8859-1 -*-
from kalliope.core.NeuronModule import NeuronModule, MissingParameterException
from kalliope import Utils
from googletranslate import translator
import wolframalpha # Only need for FullResults
import requests
import re
import os


class Answer_of_everything(NeuronModule):
    def __init__(self, **kwargs):
        super(Answer_of_everything, self).__init__(**kwargs)
        # the args from the neuron configuration
        self.query = kwargs.get('question', None)
        self.key = kwargs.get('key', None)
        self.option = kwargs.get('option', None)
        self.translate = kwargs.get('translate', None)
        self.tell_more = kwargs.get('tell_me_more', False)
        
        self.SR_ROOT = 'https://api.wolframalpha.com/v2/spoken'
        self.SA_ROOT = 'http://api.wolframalpha.com/v2/result'
        
        self.option_list = ['ShortAnswer', 'SpokenAnswer', 'FullResults', 'All']
        answer = None
        stop = False
        answers = []
        #self.more = None
        
        if self._is_parameters_ok():
            if self.tell_more:
                with open('temp') as f:
                    data = f.read()
                more = ({('TellMeMore' if not self.file_is_empty('temp') else 'NothingMoreToTell') : (data if not self.file_is_empty('temp') else ' ')})
                self.say(more)

            
            # http://products.wolframalpha.com/spoken-results-api/documentation/ 
            # release of the simpons =  The answer is Sunday, December 17, 1989
            # who is deadpool = Returns a biographie 
            # what is the weather in New york = None
            # what is water made of =  None
            # what is the answer to everything = 42
            # How old is the sun = The Sun is about 4.57 billion years old
            # what time is it in tokio = The answer is 11:08:30 P.M. JST; Monday, May 21, 2018
            if self.option == 'SpokenAnswer': 
                answer = self.spoken_answer(self.query)
            
            # http://products.wolframalpha.com/short-answers-api/documentation/
            # release of the simpons =  Sunday, December 17, 1989
            # who is deadpool = Returns a biographie
            # what is the weather in New york = None
            # what is water made of =  None
            # what is the answer to everything = 42
            # How old is the sun = 4.57 billion years
            # what time is it in tokio = 11:08:31 P.M. JST, Monday, May 21, 2018
            if self.option == 'ShortAnswer': 
                answer = self.short_answer(self.query)
                
            # http://products.wolframalpha.com/api/documentation/
            # release of the simpons = Sunday, December 17, 1989 | more: None
            # who is deadpool = alternate names | Wade "Winston" Wilson  |  Jack  |  The Merc With a Mouth  | ...  more: None
            # what is the weather in New york = temperature | 18 °Cconditions | clearrelative humidity | 61%  (dew point: 11 °C)wind speed | 0 m/s(54 minutes ago) | more: dew point: 11 °C) wind speed, 0 m/s (54 minutes ago
            # what is water made of =  | number of atoms | mass fraction | atom fraction H (hydrogen) | 2 | 11.191% | 66.7% O (oxygen) | 1 | 88.809% | 33.3% | more: hydrogen), 2, 11.191%, 66.7% O (oxygen), 1, 88.809%, 33.3%
            # what is the answer to everything = 42 more: according to the book The Hitchhiker's Guide to the Galaxy, by Douglas Adams
            # How old is the sun = Nothing
            # what time is it in tokio = Nothing
            if self.option == 'FullResults':
                result = self.full_results(self.query)
                if result[0]:
                    if result[1] is not None:
                        more = result[1]
                    else:
                        more = '' 
                    # Idea: 
                    # How tall is the eiffeltower = 324 meters  (city rank: 1st  |  national rank: 1st  |  world rank: 60th)  write the content of the brackets as extra/more infomation in file to use it later e.g Kalliope -->   tell me more
                    # What is the answer to everything =  42 (according to the book The Hitchhiker's Guide to the Galaxy, by Douglas Adams)
                    with open('temp', 'w') as f:
                        f.write(more)      
                    
                    answer = ({('AnswerFound' if result[0] else 'NoAnswerFound') : (result[0]  if result[0] else ' ')})

                    stop = True
                    self.say(answer)
                    
            # Just for testing and to compare all the results
            if self.option == 'All':
                short_a = self.short_answer(self.query)
                spoken_a = self.spoken_answer(self.query)
                full_r = self.full_results(self.query)

                if short_a:
                    short_a_a = ({('ShortAnswer' if short_a else 'NoShortAnswer') : (short_a if short_a else ' ')})
                    answers.append(short_a_a)
                if spoken_a:    
                    spoken_a_a = ({('SpokenAnswer' if spoken_a else 'NoSpokenAnswer') : (spoken_a if spoken_a else ' ')})
                    answers.append(spoken_a_a)
                
                if full_r[0]:
                    full_r_a = ({('FullResults' if full_r[0] else 'NoFullResults') : (full_r[0]  if full_r[0] else ' ')})
                    answers.append(full_r_a)
                    full_r_more = ({('FullResultsMore' if full_r[1] else 'NoFullResultsMore') : (full_r[1] if full_r[1] else ' ')})
                    answers.append(full_r_more)

                stop = True
                for a in answers:
                    self.say(a)

                
            if answer and not stop:
                answer = ({'AnswerFound' : answer})
            else:
                answer = ({'NoAnswerFound' : self.query})
            
            if not stop:    
                self.say(answer)
    
    def file_is_empty(self, path):
        return os.stat(path).st_size==0
        
    def translate_question(self, text):
        text = translator.translate(text, dest='en', src=self.translate).text
        Utils.print_info('Translated question to: %s' % text)
        return text
    
    def translate_answer(self, text):
        text = translator.translate(text, dest=self.translate, src='en').text
        Utils.print_info('Translated answer to: %s' % text)
        return text    
    
    # Using the library from https://github.com/jaraco/wolframalpha   
    def full_results(self, text):
        if self.translate:
            text = self.translate_question(text)
        
        client = wolframalpha.Client(self.key)
        res = client.query(text)
        results = []
        more = None
        
        if res['@success'] == 'true':
            #pod0 = res['pod'][0] # Our question
            pod1 = res['pod'][1] # Our answers
            Utils.print_info('Full results found: %s' % pod1['subpod']['plaintext'] )
            result = pod1['subpod']['plaintext']
            
            if '(' in result:
                answer = result.split('(', 1)[0]
                answer = re.sub(r" \| ", r", ", answer)
                more = result.split('(', 1)[1].rstrip(')')
                more = re.sub(r" \| ", r", ", more)
            else:
                answer = result
                more = None
            if self.translate:
                answer = self.translate_answer(answer)
                if more is not None:
                    more = self.translate_answer(more)

   
        else:
            Utils.print_info('No full results found for %s' % text)        
            answer = None
        
        results.append(answer)   
        results.append(more)     
        return results
            
    # Function spoken_answer and short_answer orginal from https://github.com/fishbb/wolfram-alpha-api/blob/master/waapi.py
    def spoken_answer(self, text):
        """
        Calls the API and returns a string of text
                                
        :param key: a developer key. Defaults to key given when the waAPI class was initialized.
        
        :query examples:
            i = 'How many megabytes are in a gigabyte'			        
        """
        if self.translate:
            text = self.translate_question(text)
        
        url = '%s?i=%s&appid=%s' % (
        self.SR_ROOT, text.encode('utf8').lower(), self.key
        )
        r = requests.get(url)			
        if r.text == 'No spoken result available' or r.text == 'Wolfram Alpha did not understand your input':
            Utils.print_info('No spoken answer found for %s' % text)        
            result = None
        else:
            Utils.print_info('Spoken answer found: %s' % r.text)
            result = r.text
            if self.translate:
                result = self.translate_answer(result)
                
        return result 

                        
    def short_answer(self, text):
        """
        Calls the API and returns a string of text
                                
        :param key: a developer key. Defaults to key given when the waAPI class was initialized.
        
        :query examples:
            i = 'How many megabytes are in a gigabyte'			        
        """
        if self.translate:
            text = self.translate_question(text)
        
        url = '%s?i=%s&appid=%s' % (
            self.SA_ROOT, text.encode('utf8').lower(), self.key
            )
        r = requests.get(url)
        
        if r.text == 'No short answer available' or r.text == 'Wolfram|Alpha did not understand your input': 
            Utils.print_info('No Short answer found for: %s' % text)
            result = None
        else:
            Utils.print_info('Short answer found: %s' % r.text)
            result = r.text
            if self.translate:
                result = self.translate_answer(result)
        return result



        
    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise

        .. raises:: MissingParameterException
        """
        if self.query is None and not self.tell_more:
            raise MissingParameterException("You must set a query")     
        if self.option not in self.option_list and not self.tell_more:
            raise MissingParameterException("Option %s not in list" % self.option)
        return True
