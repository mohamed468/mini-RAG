# mini-RAG

This is a minimal implemention of the RAG model for question answering.

## Requirements

- python 3.8 or later

#### Install python using MiniConda

1) Downloda and install MiniConda from [here](https://www.anaconda.com/docs/getting-started/miniconda/main#quick-command-line-install)
2) create a new environment using the following Command:
```bash
$ conda create -n mini-rag python=3.8
```
3) Activate the environment:
```bash
$ conda activate mini-rag
```

### (Optional) Setup you command line interface for better readability
```bash
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "
```


## Installation

### Install the required packages

```bash
$ pip install -r requirements.txt
```

### setup the environment variables

```bash
$ cp .env.example .env
```

Set your environment variables in the `.env` file. Like `OPENAI_API_KEY` value.

## Run the FastAPI server

```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

## POSTMAN Collection

Download the POSTMAN collection from[/assets/mini-rag-app.postman_collection.json](/assets/mini-rag-app.postman_collection.json)
