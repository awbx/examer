# Examer
- script to register in the exam event for 42 exams!

## Installation
run the following command to setup env and install dependencies.
```bash
python3 -m pip install virtualenv
python3 -m venv env

source env/bin/activate

pip install -r requirements.txt
```

## Running

first, off you should create a file called `.env` with the following content.

```
INTRA_USER=YOUR 42 INTRA USERNAME
INTRA_PASS=YOUR 42 INTRA PASSWORD
```
then run the following command

```bash
python3 main.py
```

## License
[MIT License](./LICENSE)