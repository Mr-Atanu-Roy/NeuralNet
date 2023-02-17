
## Features
There are mainly 3 functionalitys of this project. Their names with functionalities are given below :

### ChitChat
An AI chatbot which can answer all your queries. You can ask it anything you want. But it must be relivant. After the respose is generated, the AI will also read it for you. Voice search option is also available. You can just talk to it like you talk to other persons. After you sign up, you will be able to make customizable bots as per your requirments.There are many options like age, name, bot-type, gender which are customizable in this section.

### CodeGenie
An AI code generator, which generate codes as per your instructions and selected languages. 
Currently supported languages are - 
- Python
- Java
- JavaScript
- C 
- C++
- C#
- Ruby
- Rust
- PHP
- R Language
- HTML

### ArtiFlex
An AI that can generate images as per your given prompt. I can generate anything, even if such thing does not exists. If it does not exists then it will generate it arificially.
Currently it generated 3 images for each given prompt and each image is of size 256 x 256 pixels

Authentication system is also added, which included signin, login, logout, email verification, reset password. user can access all the products(ChitChat, Artiflex and CodeGenie) only after signing up. After you register you will be able to customize the ChitCht bot. There are many options like age, name, bot-type, gender which are customizable in this section

## Tech Stack

**Client Side:** HTML, SCSS, TailwindCSS

**Server Side:** Django, Redis, OpenAi for the AI generated contents


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`DEBUG = TRUE`

`SECRET_KEY = 'django-insecure-=)pmi!os!bpw_g_qbl*!3-!_%hn30(nm6na*vi1#&@7#^_w1ye'`

`API_KEY = Your API Key`

For the `API_KEY` go to OpenAi's webiste : https://openai.com/api/  from there signup (or login if you have account). Then generate an API key and put it in the .env file

## Installation

Create a folder and open terminal and install this project by
command 
```bash
git clone https://github.com/Mr-Atanu-Roy/NeuralNet

```
or simply download this project from https://github.com/Mr-Atanu-Roy/NeuralNet

In project directory Create a virtual environment(say env) :

```bash
  virtualenv env

```
Activate the virtual environment -

For windows :
```bash
  env\Script\activate

```
Install dependencies :
```bash
  pip install -r requirements.txt

```
To migrate the database run migrations commands(not necessary for this project) :
```bash
  py manage.py magemigrations
  py manage.py migrate

```

Create a super user(not necessary for this project) :
```bash
  py manage.py createsuperuser

```

To run the project in your localserver :
```bash
  py manage.py runserver

```
Then go to http://127.0.0.1:8000 in your browser to see the project

## Author

- [@Mr-Atanu-Roy](https://www.github.com/Mr-Atanu-Roy)

