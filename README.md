# answer-of-everything

## Synopsis
A search engines to ask all kind of questions, where you can set the priority of the different search engines. If the first engine does not find an answer, it will lookup the next engine.

## Installation
```bash
kalliope install --git-url https://github.com/kalliope-project/kalliope_neuron_answer_of_everything.git
```

## Example
- Kalliope --> I have a question how tall is the eiffel tower 
- Kalliope --> Can you answer me what time is it in Tokio
- Kalliope --> Tell me when albert einstein is born
- Kalliope --> Can you tell me what day was March 31, 1989


## Main options
| parameter        | required | comments                                     |
|------------------|----------|----------------------------------------------|
| question         | yes      |                                              |
| engines          | yes      | Define the search engines you want to use    |
| translate        | no       | Wolfram Alpha and Duckduckgo only support English, [here](https://py-googletrans.readthedocs.io/en/latest/#googletrans-languages) you can find supported languages |

## Wolfram alpha engine
| parameter        | required | comments                                     |
|------------------|----------|----------------------------------------------|
| wolfram_alpha    | yes      |                                              |
| key              | yes      | https://products.wolframalpha.com/api/       |
| unit             | no       | You can choose between metric (default) or imperial |
| priority         | no       | Its only required if you use python2, in python3 it searches in the order you define the engines in your synapses | 
| option           | no       | You can chose between spoken_answer (default) or short_answer. With spoken_answer you get a full sentence back if available, otherwise it returns a short_answer| 

## Google engine
| parameter        | required | comments                                     |
|------------------|----------|----------------------------------------------|
| google           | yes      |                                              |
| priority         | no       | Its only required if you use python2, in python3 it searches in the order you define the engines in your synapses | 

## Duckduckgo engine
| parameter        | required | comments                                     |
|------------------|----------|----------------------------------------------|
| duckduckgo       | yes      |                                              |
| priority         | no       | Its only required if you use python2, in python3 it searches in the order you define the engines in your synapses | 

## Returned values
| name             | description                           | 
|------------------|---------------------------------------|
| wolfram_answer   | Answer found on wolfram alpha         |
| google_answer    | Answer found on google                |
| duckduckgo_answer| Answer found on duckduckgo            |
| NoAnswerFound    | No Answer found, returns the question |


## Synapse example for python 2
```
  
  - name: "answer-of-everything"
    signals: 
      - order: "answer me the question {{ query }}"
    neurons:
      - answer_of_everything:
          question: "{{ query }}"
          language: "de"
          engines:  
                wolfram_alpha: 
                    key: "XXXX-XXXXXXXX"
                    priority: 1
                google:
                    priority: 2
                duckduckgo:
                    priority: 3
          file_template: "templates/answer_of_everything.j2" 

```
## Synapse example for python 3
```
  
  - name: "answer-of-everything"
    signals: 
      - order: "answer me the question {{ query }}"
    neurons:
      - answer_of_everything:
          question: "{{ query }}"
          language: "de"
          engines:  
                wolfram_alpha: 
                    key: "XXXX-XXXXXXXX"
                google:
                duckduckgo:
          file_template: "templates/answer_of_everything.j2" 

```

## Example file template
```
{% if wolfram_answer %} 
   {{ wolfram_answer }}
{% elif google_answer %}
    {{ google_answer }}
{% elif duckduckgo_answer %}
    {{ duckduckgo_answer }}
{% elif NoAnswerFound %} 
    I'm Sorry I have no Answer to the question {{ NoAnswerFound }}
{% endif %}

 ``