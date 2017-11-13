FROM jupyter/scipy-notebook
USER root
RUN conda install --yes --name root spacy pymongo tweepy
RUN ["bash", "-c", "source activate root"]
RUN python -m spacy download en
USER jovyan
