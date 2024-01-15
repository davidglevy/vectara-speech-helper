from typing import Union, List
from pathlib import Path
from vectara_client.core import Client, Factory
from vectara_client.util import StandardPromptFactory
from vectara_speech.render import WordRenderer
from datetime import datetime
import os

import logging

# TODO Add response templates for header, footer and title page

class SpeechHelper():

    client: Client

    def __init__(self,
            topic:str,
            type_of_speech:str="Presentation at Innovation Forum",
            example_text:str=None,
            example_path:Union[str,Path]=None,
            length:int=300,
            language='en',
            corpus_path:str="source",
            corpus_id:List[int]=None,
            output="result.doc"):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.topic = topic
        self.type_of_speech = type_of_speech
        self.example_text = example_text
        self.example_path = example_path
        self.length = length
        self.language = language
        self.corpus_path = corpus_path
        self.corpus_id = corpus_id
        self.output = output

    def _make_prompt_safe(self, input):
        if input:
            return input.replace("\n", "\\n ").replace("\\", "").replace("\"", "'")
        else:
            return ""

    def _validate(self):
        # Validate the topic
        if not self.topic or len(self.topic) < 3:
            raise TypeError("The topic is too short")

        if not self.topic or len(self.topic) < 3:
            raise TypeError("The type of sp is too short")

        if self.example_path and self.example_text:
            raise TypeError("You must either use [example_path] or [example_text]")

        if self.example_path:
            # Load the example if provided.
            if isinstance(self.example_path, str):
                path = Path(self.example_path)
            elif isinstance(self.example_path, Path):
                path = self.example_path
            else:
                raise TypeError(f"Unexpected type [{type(self.example_path)}] for example_path")

            with open(path, 'r') as f:
                text = self._make_prompt_safe(f.read())
                words = text.split(" ")
                if len(words) < 20:
                    raise TypeError("Please provide an example sp that is longer")
                elif len(words) > 1000:
                    raise TypeError("Speech example is too long, must be less than 1000 words")

        # TODO Add validation of the output
        # TODO Add validation of corpus id
        # TODO Add validation of corpus path

    def _build_corpus(self):
        if self.corpus_id:
            self.logger.info("Using existing corpus [{self.corpus_id}]")
        elif self.corpus_path:

            corpus_name = f"sp - {self.topic}"[0:50]

            # Create Corpus if it doesn't exist.
            corpora = self.client.admin_service.list_corpora(filter=corpus_name)

            corpus = None
            create = False
            if len(corpora) > 1:
                self.logger.info(f"Found multiple corpus matching name [{corpus_name}]")
                corpus = None
                for potential in corpora:
                    if potential.name == corpus_name:
                        corpus = potential
                        break
                if not corpus:
                    self.logger.info(f"Whilst there were [{len(corpora)}], we could not find an existing corpus with name [{corpus_name}]. Creating new one.")
                    create = True
            elif len(corpora) == 1:
                self.logger.info("Found exactly 1 corpus")
                corpus = corpora[0]
            else:
                create = True

            if create:
                self.corpus_id = self.client.admin_service.create_corpus(corpus_name, "Corpus to store information relevant to sp.")
            else:
                self.corpus_id = corpus.id

            path = Path(self.corpus_path)

            extensions = ["pdf", "docx", "txt", "json"]
            files = []
            for extension in extensions:
                files.extend(path.glob(f"**/*.{extension}"))

            for corpus_file in files:
                # TODO Check whether file already uploaded
                # TODO Check sha1_hash on uploaded file
                self.logger.info(f"Uploading [{corpus_file}]")
                self.client.indexer_service.upload(self.corpus_id, corpus_file)

        else:
            raise Exception("Neither corpus_id or corpus_path have been set.")

    def _init_client(self):
        self.logger.info("Initializing Vectara client")
        self.client = Factory().build()

    def _build_custom_prompt(self):
        """
        Build a custom prompt based on the sp parameters.
        """


        if self.example_text:
            # Sanitize input for prompt.
            example_speech = self.example_text.replace("\n", "\\n ")
            speech_for_doc = self.example_text.replace("\n", "\n\n")
        elif self.example_path:
            with open(self.example_path, 'r') as f:
                example_speech = f.read().replace("\n", "\\n ")
                speech_for_doc = f.read().replace("\n", "\n\n")
        else:
            raise Exception("You must specify either [example_text] or [example_path]")

        # TODO Add language to prompt.
        system_prompt = (f"""You are a sp writer who needs to write a sp for a {self.type_of_speech}. Use only the information below to create a sp of the requested length in english. Respond in the language denoted by ISO 639 code \\"$vectaraLangCode\\".""")

        system_prompt += f"\\nWrite the sp in the following style:\\n{example_speech}"

        user_prompt = (f"Create a sp on topic [{self.topic}] that is {self.length} words long, including a reference to an initiative"
                       f"listed in our prior responses. References should be identified as '[n]' where n is the number of the result")

        prompt_factory = StandardPromptFactory(system_prompt, user_prompt)
        prompt = prompt_factory.build()

        return prompt, speech_for_doc


    def build_speech(self):


        """
        Builds a sp on the topic configured for this helper.

        Methodology:

        1. Validate
        2. Initialize Client
        3. Build Corpus (if required)
        4. Build Custom Prompt
        5. Run Query+Summarizer
        6. Render Speech output

        :return:
        """
        self._validate()
        self._init_client()
        self._build_corpus()
        prompt, example_speech = self._build_custom_prompt()

        qs = self.client.query_service
        result = qs.query(self.topic,
                          self.corpus_id, promptText=prompt, re_rank=True,
                          response_lang=self.language,
                          summarizer="vectara-summary-ext-v1.3.0")

        cover_template = Path("resources/templates/basic_cover.mdt")

        values = {
            'topic': self.topic,
            'author': 'Unknown',
            'speech': result.summary[0].text,
            'example_text': example_speech,
            'date_generated': datetime.today().strftime('%d/%m/%Y')
        }

        renderer = WordRenderer(cover_template, f"{self.topic}.docx")
        renderer.render(values)

        #self.logger.info(result.summary[0].text)
        return result
