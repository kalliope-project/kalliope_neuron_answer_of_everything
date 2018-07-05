# -*- coding: iso-8859-1 -*-
from kalliope.core.NeuronModule import NeuronModule, MissingParameterException
from kalliope import Utils
from googletranslate import translator
import requests

class Answer_of_everything(NeuronModule):
    def __init__(self, **kwargs):
        super(Answer_of_everything, self).__init__(**kwargs)
        # the args from the neuron configuration
        self.question = kwargs.get('question', None)
        self.option = kwargs.get('option', 'SpokenAnswer')
        self.translate = kwargs.get('translate', None)
        self.key = kwargs.get('key', None)
        
        answer = None
        self.SR_ROOT = 'https://api.wolframalpha.com/v2/spoken'
        self.SA_ROOT = 'http://api.wolframalpha.com/v2/result'
        
        if self._is_parameters_ok():
            question = self.question

            if self.translate:
                question = self.translate_question(question)

            if self.option == "SpokenAnswer":
                answer = self.spoken_answer(question)
                # Sometimes there is no spoken answer, so we try to get the short answer
                if answer is None:
                    answer = self.short_answer(question)  

            if self.option == "ShortAnswer":
                answer = self.short_answer(question) 
            
            # There are some answers, which return irrelevant informations, those we will remove from the answer
            if answer:
                answer = self.check_for_spliting_result(answer)

            if self.translate and answer is not None:
                answer = self.translate_answer(answer)

            answer = ({('AnswerFound' if answer else 'NoAnswerFound') : (answer if answer else self.question)})
            self.say(answer)


    def translate_question(self, text):
        text = translator.translate(text, dest='en', src=self.translate).text
        Utils.print_info('Translated question to: %s' % text)
        return text
    
    def translate_answer(self, text):
        text = translator.translate(text, dest=self.translate, src='en').text
        Utils.print_info('Translated answer to: %s' % text)
        return text    
    
    def spoken_answer(self, text):
        """
        Calls the API and returns a string of text
                                
        :param key: a developer key. Defaults to key given when the waAPI class was initialized.
        
        :query examples:
            i = 'How many megabytes are in a gigabyte'			        
        """
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

        return result 

                        
    def short_answer(self, text):
        """
        Calls the API and returns a string of text
                                
        :param key: a developer key. Defaults to key given when the waAPI class was initialized.
        
        :query examples:
            i = 'How many megabytes are in a gigabyte'			        
        """
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
        return result    
     
    def check_for_spliting_result(self, result):
        # If we ask for a time, we also get the timezones and day e.g The answer is 12:55:45 P.M. EEST; Thursday, July 5, 2018 so we remove everything except the time
        if 'P.M.' in result:
            result = result.split('P.M.', 1)[0] + 'P.M.'
        if 'A.M.' in result:
            result = result.split('A.M.', 1)[0] + 'A.M.'     
        
        return result
        
    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise

        .. raises:: MissingParameterException
        """
        if self.key is None:
            raise MissingParameterException("You need to set a developer key") 
        if self.question is None or self.question is  "":
            raise MissingParameterException("Question is None, please try again")     

        return True
