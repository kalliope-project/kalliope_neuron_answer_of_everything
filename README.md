# kalliope_neuron_answer_of_everything
Get an answer to a question from multiple backend engine like Google, wolframalpha or DuckDuckGo

## Synopsis
Ask a generell question. At the moment only Wolfram Alpha is supported.

## Installation
```bash
kalliope install --git-url https://github.com/kalliope-project/kalliope_neuron_answer_of_everything.git
```

## Example
- Kalliope --> I have a question how tall is the eiffel tower 
- Kalliope --> I have a question what time is it in Tokio
- Kalliope --> I have a question when is albert einstein born
- Kalliope --> I have a question how far away is the moon from earth

## Options
| parameter | required | default | choices & comments |
|-----------|----------|---------|--------------------|
| question  | yes      |         |                    |
| key       | yes      |         | Check [here](https://products.wolframalpha.com/api/) to get a developer key |
| option    | no       | SpokenAnswer | SpokenAnswer, ShortAnswer |
| translate | no       | English | Wolfram Alpha is only available in english, so we need to translate the answer and question with the help of google translator, e.g. "fr", "de", [look here for more](https://cloud.google.com/translate/docs/languages) |


## Synpase
```
  - name: "answer-of-everything-spoken"
    signals: 
      - order: "I have a question {{ query }}"
    neurons:
      - answer_of_everything:
          key: "XXXXXX-XXXXXXXXXX"
          question: "{{ query }}"
          translate: "de"
          file_template: "templates/answers.j2"

  - name: "answer-of-everything-short"
    signals: 
      - order: "I have a question {{ query }}"
    neurons:
      - answer_of_everything:
          key: "XXXXXX-XXXXXXXXXX"
          question: "{{ query }}"
          option: "ShortAnswer"
          file_template: "templates/answers.j2"

```

## File template
```
{% if AnswerFound %} 
    According to alpha: {{ AnswerFound }}
{% elif NoAnswerFound %} 
    Didn’t found an answer to your question {{ NoAnswerFound }} 
{% endif %}

 ```

## Todos
Support different search engines, for example DuckDuckGo or google
