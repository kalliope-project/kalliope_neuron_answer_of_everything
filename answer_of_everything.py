# -*- coding: iso-8859-1 -*-
from kalliope.core.NeuronModule import NeuronModule, MissingParameterException
from kalliope import Utils
from googletrans import Translator

import re
import sys
import os 

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from engines.WolframAlpha.wolfram_alpha import WolframAlpha
from engines.GoogleAnswers.google_answer import GoogleAnswer
from engines.DuckDuckGo.duckduckgo import DuckDuckGo

class Answer_of_everything(NeuronModule):
    def __init__(self, **kwargs):
        super(Answer_of_everything, self).__init__(**kwargs)
        # the args from the neuron configuration
        self.question = kwargs.get('question', None)
        self.engines = kwargs.get('engines', None)
        self.language = kwargs.get('language', None)

        if self._is_parameters_ok():
            sorted_engines = self.engines
            answer = None
            result = None
            
            for engine in sorted_engines: #Python 3 preserves the order of a dictionary
                if engine == "wolfram_alpha":
                    result = self.wa_engine(self.question)
                    if result:
                        answer = ({"wolfram_answer": result})
                        break
                if engine == "google":
                    result = self.google_engine(self.question)
                    if result:
                        answer = ({"google_answer": result})
                        break
                if engine == "duckduckgo":
                    result = self.ddg_engine(self.question)
                    if result:
                        answer = ({"duckduckgo_answer": result})
                        break

            if not answer:
                answer = ({"NoAnswerFound": self.question})
            self.say(answer)

    def google_engine(self, question):
        result = None
        g_a = GoogleAnswer(question)
        result = g_a.get_answer()
        if result:
            Utils.print_info('Found answer on Google')
            result = self.format_result(result[0])  
        else:
            Utils.print_info('No answer found on Google')
        return result

    def wa_engine(self, question):
        result = None
        try:
            key =  self.engines['wolfram_alpha']['key']
        except KeyError:
            raise MissingParameterException("API key is missing or is incorrect. Please set a valid API key.")  

        try:
            option = self.engines['wolfram_alpha']['option']
            if option not in ["spoken_answer", "short_answer"]:
                raise MissingParameterException("%s is not a valid option. Valid options are short_answer or spoken_answer." % option)  
        except KeyError:
            option = "spoken_answer"

        try:
            unit = self.engines['wolfram_alpha']['unit']
            if unit.lower() not in ["metric", "imperial"]:
                raise MissingParameterException("%s is not a valid unit. Valid units are metric or imperial." % unit)  
        except KeyError:
            unit = "metric"

        if self.language:
            question = self.translate_question(question, self.language)

        w_a = WolframAlpha(question, key, unit.lower())
        if option == "spoken_answer":
            result = w_a.spoken_answer()
            if result is None:
                result = w_a.short_answer()  
        
        if option == "short_answer":
            result = w_a.short_answer()       
        
        if result:
            if self.language:
                result = self.translate_answer(result, self.language)
            result = self.format_result(result)
            Utils.print_info('Found answer on Wolfram Alpha') 
        else:
            Utils.print_info('No answer found on Wolfram Alpha')

        return result

    def ddg_engine(self, question):
        result = None
        if self.language:
            question = self.translate_question(question, self.language)

        ddg = DuckDuckGo(question)
        result = ddg.get_answer()
        if result:
            if self.language:
                result = self.translate_answer(result, self.language)        
            result = self.format_result(result)
            Utils.print_info('Found answer on DuckDuckGo') 
        else:
            Utils.print_info('No answer found on DuckDuckGo')

        return result

    def translate_question(self, text, language):
        text = Translator().translate(text, dest='en', src=language).text
        return text
    
    def translate_answer(self, text, language):
        text = Translator().translate(text, dest=language, src='en').text
        return text    

    def format_result(self, result):
        result = re.sub(r'\([^)]*\)|/[^/]*/', '', result)
        result = re.sub(r" \s+", r" ", result)
        return result

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise

        .. raises:: MissingParameterException
        """ 
        if not self.question:
            raise MissingParameterException("Question parameter is missing.")
        if self.engines is None:
            raise MissingParameterException("Engines parameter is missing. Please define the search engine you want to use.")
        
        return True
