import unittest
from vectara_speech.render import WordRenderer, replace_params
from typing import Any
from pathlib import Path
import re

class TestWordRenderer(unittest.TestCase):


    def test_render(self):
        cover_template = Path("resources/templates/basic_cover.mdt")

        values = {
            'topic': 'Joy of Programming',
            'author': 'David Levy',
            'speech': 'A really good speech',
            'example_text': 'How we want the speech to sound',
            'date': '2024/01/15'

        }

        renderer = WordRenderer(cover_template, "output.docx")
        renderer.render(None, values)

    def test_replace_param(self):

        input = "Here's some input text with a param. Hello ${who}. Good ${tod}"
        result = "Here's some input text with a param. Hello World. Good morning"

        value_map = {
            'who': "World", 'tod': "morning"
        }
        self.assertEqual(result, replace_params(input, value_map))



if __name__ == '__main__':
    unittest.main()
