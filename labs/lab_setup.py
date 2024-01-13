from vectara_client.core import Factory
from vectara_client.util import render_markdown
from IPython.display import display, Markdown

import logging
import os

logging.basicConfig(format='%(asctime)s %(name)-20s %(levelname)s:%(message)s', level=logging.INFO, datefmt='%H:%M:%S %z')

logging.getLogger('OAuthUtil').setLevel(logging.WARNING)


logger = logging.getLogger(__name__)

def create_lab_corpus(lab_name:str, username_prefix=True, quiet=False) -> int:

    if not lab_name:
        raise TypeError("You must supply a lab name")
    elif len(lab_name) < 10:
        raise TypeError("Please use a descriptive name of at least 10 characters")

    if quiet:
        logging.getLogger('HomeConfigLoader').setLevel(logging.WARNING)
        logging.getLogger('RequestUtil').setLevel(logging.WARNING)

    username = os.getlogin()
    # Use maximum 10 characters from username
    user_part = username.split("@")[0][:10]
    logger.info(f"User prefix for lab: {user_part}")

    full_lab_name = f"{user_part}-{lab_name}"
    logger.info(f"Setting up lab corpus with name [{full_lab_name}]")
    

    client = Factory().build()
    admin_service = client.admin_service

    corpora = admin_service.list_corpora(full_lab_name)
    
    if len(corpora) >= 1:
        for corpus in corpora:
            admin_service.delete_corpus(corpus.id)
    else:
        logging.info(f"No existing corpus with the name {full_lab_name}")

    create_corpus_result = admin_service.create_corpus(full_lab_name, description="Example Corpus for use from Jupyter")
    logging.info(f"New corpus created {create_corpus_result}")
    corpus_id = create_corpus_result.corpusId

    logger.info(f"New lab created with id [{corpus_id}]")
    return corpus_id

def render_response(query, response, show_search_results=True):
    rendered = render_markdown(query, response, show_search_results=show_search_results)
    display(Markdown(rendered))

def render_chat(query, response, show_search_results=False):
    rendered = render_markdown(query, response, show_search_results=show_search_results, heading_level=3)
    display(Markdown(rendered))
    