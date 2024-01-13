# Vectara Speech Helper

This is a set of classes focused around building speech templates with cited
sources. This is designed to be an accelerator (not a final product) in the
creation of speeches. It uses Retrieval Augmented Generation to load relevant information
to the stated topic and build a speech in the provided style.

## Getting Started
This package depends on the `vectara-skunk-client`, please see the setup
required for this here:

[https://github.com/davidglevy/vectara-skunk-client](https://github.com/davidglevy/vectara-skunk-client)

## Usage
Designed to provide a simple interface for building a speech, using the
more advanced capabilities of the "vectara-summary-ext-v1.3.0" summarization
engine. This requires the Scale Plan to be effective.

we create the speech helper, found in `vectara_speech.SpeechHelper` with the following
parameters:

* topic - this is a mandatory parameters
* type_of_speech - Indicate the type of speech being created, the forum and potentially location
* example_path:Union[str,Path] or example_text:str - provide either a path to an example speech or the phrasing of a
  speech to style inline
* length - the desired length of the output speech, default is 300
* language - the desired output language (e.g. 'en', 'ar', 'fr' etc)
* corpus_path/corpus_id - if you want to create a corpus specifically for this with local
  content, use `corpus_path` otherwise if you already have a configured corpus with content, use `corpus_id`
* output - the destination output file (Word Format)

## Example
The following example prepares a speech for our local Python meetup group to discuss Dataclasses. The style
is based on a few sentences from a discussion from Guido van Rossum on the joys of Python.

Full code is available in `test_speech.py` file 

**NB: Output is still a todo item**

```python
from vectara_speech import SpeechHelper

helper = SpeechHelper("Introduction to Dataclasses",
                      type_of_speech="Presentation to a Local Python Community",
                      corpus_path="resources",
                      example_text="Programming is a wonderful activity. I am a little jealous that you have "
                                   "access to computers at your age; when I grew up I didn’t even know what "
                                   "a computer was! I was an electronics hobbyist though")
helper.build_speech()

```

From this we get the following output:

> Ladies and Gentlemen, let me take you back to the days when I was an electronics hobbyist. I didn't have access to computers like you, but the thrill of creating something was equally exciting. Today, I am here to stir that excitement in you by introducing a wonderful concept in Python - Dataclasses [1].
>
> Dataclasses, introduced in Python 3.7, are a decorator and a function in the dataclasses module, which simplifies the creation of classes containing data. These are special classes typically used to store data and do not contain methods, except, perhaps, for __init__(), __repr__(), and __eq__().
>
> In the past, the creation of data-containing classes was laborious and error-prone. The introduction of Dataclasses addressed this issue by automatically adding special methods to the classes. Now, isn't that handy? 
>
> Remember the time when we had to manually write class methods such as __init__ or __repr__? With Dataclasses, Python does that for you. It automatically adds an __init__() method that initializes the class attributes, a __repr__() method to provide a readable string representation of the object, and an __eq__() method for comparing objects for equality. 
>
> But how do we create a Dataclass? Simple. We just need to import the dataclasses module and use the @dataclasses.dataclass decorator above the class definition. It's like magic!
>
> Ladies and Gentlemen, Dataclasses are not just about reducing the amount of code and avoiding redundancy. It's more about the programming elegance and efficiency it introduces. It's about the joy of creating something wonderful with less effort, just like I experienced as an electronics hobbyist.
>
> Learning Python, or any programming language, is a journey. And in this journey, tools like Dataclasses make our life easier and our code cleaner. So, let's embrace these features and keep creating magic with Python [1].
>
> Thank you!
