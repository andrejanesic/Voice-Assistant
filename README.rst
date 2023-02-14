Voice Assistant
===============

Personal voice assistant developed in Python with Tensorflow/Keras. Group assignment conducted as part of the Voice Recognition (5025) and Deep Learning (8032) subjects.

Project Specs
-------------

This project involves the creation of a miniature *voice assistant* app. The system supports the following functionalities:

-  Recognizing speech in voice audio
-  Voice-2-Text (recognition of different pre-defined commands, and their parameters)
-  Processing of commands through internal components and external APIs to generate a response
-  Sentiment analysis of spoken text (if such a command is issued)
-  Text-2-Voice (responding to user's command)

The project relies on deep learning methods (transformers and NLP models) for text-to-speech, sentiment analysis, speech-to-text, etc.

Setup & Installation
--------------------

Please run `./make` (Linux) or `.\make.bat` (Windows) to set up the package. This will create a new Python `virtual environment <https://docs.python.org/3/library/venv.html>`__ and install the required dependencies; the script will also download the required NLP wav-2-vec model files.

Other available Make commands include:

- `./make models` - downloads the deep learning models
- `./make dev` - runs the script
- `./make test` - runs the test script
- `./make build` - builds the Python package

Running
-------

The script connects to external APIs to fetch data. For this to work, you'll need a free `RapidAPI account <https://rapidapi.com/hub>`__.

After creating an account, find the key of your `default application <https://rapidapi.com/developer/apps>`__. Copy the key, then run the following command::

   ./make.bat dev API_KEY       # If you're on Windows
   ./make dev APIKEY="API_KEY"  # If you're on Linux

Authors
-------

*In alphabetical order:*

| **Brcic, Luka** \[`LinkedIn <https://www.linkedin.com/in/luka-brcic-5120b8197/>`__\]
| Software Engineer @ `Seven Bridges <https://www.sevenbridges.com/>`__
| Comp Sci Undergrad @ `School of Computing, Belgrade <https://www.linkedin.com/school/racunarski-fakultet/>`__
| lbrcic4219rn@raf.rs
| 

| **Nesic, Andreja** \[`LinkedIn <https://www.linkedin.com/in/andreja-nesic/>`__\]
| Comp Sci Undergrad @ `School of Computing, Belgrade <https://www.linkedin.com/school/racunarski-fakultet/>`__
| office@andrejanesic.com
| anesic3119rn@raf.rs
| 

| **Tadic, Nikola** \[`LinkedIn <https://www.linkedin.com/in/nikola-tadi%C4%87-01112000/>`__\]
| Frontend Developer @ `Insightful <https://www.insightful.io/>`__
| Comp Sci Undergrad @ `School of Computing, Belgrade <https://www.linkedin.com/school/racunarski-fakultet/>`__
| ntadic4419rn@raf.rs
| 