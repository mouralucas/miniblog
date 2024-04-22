# Miniblog

This is a prototype for a blog. 
This was a simple build just to show how it can be done.

Not all errors and exceptions were handled and the tests may not cover all cases and edge cases.


# Usage

## Docker
To run just build the docker image, and then run it:

```bash
docker build -t blog_image .
```

```bash
docker run -p 8000:8000 blog_image
```

The project will be available at:
```
localhost:8000
```

## Virtual environment
It can be built using python command line as well.

Obs: commands for Linux, it may differ for other operating systems

In project root, create a virtual environment:
```bash
python3 -m venv venv
```

Start the venv:
```bash
source venv/bin/activate
```

Install the requirements:
```bash
pip3 install -r requirements.txt
```

Run the migrations
```bash
python3 manage.py migrate
```

Finally, run the server
```bash
python3 manage.py runserver
```

This will also start the server at:
```
localhost:8000
```

With this approach, test can be run with the following command:
```bash
python3 manage.py test
```
