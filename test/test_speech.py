import unittest
import logging

from vectara_speech import SpeechHelper

class MyTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logging.basicConfig(format='%(asctime)s:%(name)-35s %(levelname)s:%(message)s', level=logging.INFO, datefmt='%H:%M:%S %z')
        self.logger = logging.getLogger()

    def test_build_speech_guido(self):
        helper = SpeechHelper("Introduction to Dataclasses",
                              type_of_speech="Presentation to a Local Python Community",
                              corpus_path="resources",
                              example_text="Programming is a wonderful activity. I am a little jealous that you have "
                                           "access to computers at your age; when I grew up I didn’t even know what "
                                           "a computer was! I was an electronics hobbyist though")
        helper.build_speech()

    def test_build_speech_python_blurb(self):
        helper = SpeechHelper("Introduction to Dataclasses",
                              type_of_speech="Presentation to a Local Python Community",
                              corpus_path="resources",
                              example_text="""Often, programmers fall in love with Python because of the increased productivity
it provides. Since there is no compilation step, the edit-test-debug cycle is
incredibly fast.Debugging Python programs is easy: a bug or bad input will never
cause a segmentation fault. Instead, when the interpreter discovers an error, it
raises an exception.When the program doesn't catch the exception, the
interpreter prints a stack trace. A source level debugger allows inspection of
local and global variables, evaluation of arbitrary expressions, setting
breakpoints, stepping through the code a line at a time, and so on. The debugger
is written in Python itself, testifying to Python's introspective power. On the
other hand, often the quickest way to debug a program is to add a few print
statements to the source: the fast edit - test - debug cycle makes this simple
approach very effective.""")
        helper.build_speech()

    def test_build_speech_python_blurb_ar(self):
        helper = SpeechHelper("Introduction to Dataclasses",
                              type_of_speech="Presentation to a Local Python Community",
                              corpus_path="resources",
                              example_text="""Often, programmers fall in love with Python because of the increased productivity
it provides. Since there is no compilation step, the edit-test-debug cycle is
incredibly fast.Debugging Python programs is easy: a bug or bad input will never
cause a segmentation fault. Instead, when the interpreter discovers an error, it
raises an exception.When the program doesn't catch the exception, the
interpreter prints a stack trace. A source level debugger allows inspection of
local and global variables, evaluation of arbitrary expressions, setting
breakpoints, stepping through the code a line at a time, and so on. The debugger
is written in Python itself, testifying to Python's introspective power. On the
other hand, often the quickest way to debug a program is to add a few print
statements to the source: the fast edit - test - debug cycle makes this simple
approach very effective.""",
                              language='ar')
        helper.build_speech()

if __name__ == '__main__':
    unittest.main()
