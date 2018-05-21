# kalliope_neuron_answer_of_everything-
Get an answer to a question from multiple backend engine like Google, wolframalpha or DuckDuckGo
## Synopsis

Currently in alpha stage and only for WolframAlpha search. 

## Example
Kalliope --> Ask alpha how tall is the eiffel tower 
Kalliope --> Ask alpha what time is it in Tokio
Kalliope --> Ask alpha when albert einstein is born
Kalliope --> Ask alpha how far is the moon from earth away

## Options
| parameter        | required | comments                                                  |
|----------------|---------|----------------------------------------------|
| question          | yes       |                                                                 |
| key                 | yes       | https://products.wolframalpha.com/api/           |
| translate         | no         | Google translator, default english no need to translate, e.g. "fr" , "de"|
| option            | yes        | 'ShortAnswer', 'SpokenAnswer', 'FullResults', 'All' |
| tell_me_more   | no         | If you have FullDetails you get 2 results, the answer and a definition, If tell_me_more is True you can ask a second time, to tell you more |



## Synpase
```
  - name: "answer-of-everything-short"
    signals: 
      - order: "ask alpha_short {{ query }}"
    neurons:
      - answer_of_everything:
          key: "XXXXXX-XXXXXXXXXX"
          question: "{{ query }}"
          option: "ShortAnswer"
          #translate: "de"
          file_template: "templates/answers.j2"

  - name: "answer-of-everything-spoken"
    signals: 
      - order: "ask alpha_spoken {{ query }}"
    neurons:
      - answer_of_everything:
          key: "XXXXXX-XXXXXXXXXX"
          question: "{{ query }}"
          option: "SpokenAnswer"   
          #translate: "de"
          file_template: "templates/answers.j2"
          
  - name: "answer-of-everything-full"
    signals: 
      - order: "ask alpha_full {{ query }}"
    neurons:
      - answer_of_everything:
          key: "XXXXXX-XXXXXXXXXX"
          question: "{{ query }}"
          option: "FullResults"   
          #translate: "de"
          file_template: "templates/answers.j2"
          
  - name: "answer-of-everything-all"
    signals: 
      - order: "ask alpha_all {{ query }}"
    neurons:
      - answer_of_everything:
          key: "XXXXXX-XXXXXXXXXX"
          question: "{{ query }}"
          option: "All"   
          #translate: "de"
          file_template: "templates/answers.j2"          
   
  - name: "answer-of-everything-tell-more"
    signals: 
      - order: "tell me more"
    neurons:
      - answer_of_everything:
          tell_me_more: True
          file_template: "templates/answers.j2"    
```

## File template
```
{% if AnswerFound %} 
    According to alpha: {{ AnswerFound }}
{% elif NoAnswerFound %} 
    Didn’t found an answer to your question {{ NoAnswerFound }} 

{% elif TellMeMore %} 
    {{ TellMeMore }}
{% elif NothingMoreToTell %} 
    Could not find more information

{% elif ShortAnswer %} 
    Short answer: {{ ShortAnswer }}
{% elif SpokenAnswer %} 
    Spoken answer: {{ SpokenAnswer }}
{% elif FullResults %} 
    Full results: {{ FullResults }}
{% elif FullResultsMore %} 
    full results and more: {{ FullResultsMore }} 
    
{% elif NoShortAnswer %} 
    no short answer found
{% elif NoSpokenAnswer %} 
    No spoken answer found
{% elif NoFullResults %} 
    No full results found
{% elif NoFullResultsMore %} 
    Nothing more for full results
 ```

## To Do & Ideas
- Find out which wolframalpha api we use as default to support a high quality of answer.
- Making it modular to use different engines e.g. duckduckgo, google.
- Coding a wolframalpha engine (Idea:  FullResults only and spoken/short answer in the main code as default)
