# News Information Retriveal System

## To start the project, please install following pacakge

1. python version 3.9, recommand to install virtual env tools such as anaconda pyenv 
[anaconda installation](https://docs.anaconda.com/anaconda/install/index.html)

After installation of python, create a virtual env and install the following package
```
pip install -r requirments.txt
```

2. install nodejs and npm for frontend
[npm nodejs installation](https://nodejs.org/en/download/)

3. install the elasticsearch, version 7.x.x above
[elastic search installation](https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html)

4. read django doc
[django doc](https://docs.djangoproject.com/en/4.0/)
[django elasticsearch ](https://django-elasticsearch-dsl.readthedocs.io/en/latest/)

5. to begin with frontend, refer to the readme in fronend subdirectory

## To indexing the data, please run

```./manage.py test```

## To run this project, please run the following command

1. Start the server ```./manage.py runserver```
2. Start the frontend ```cd frontend && npm run dev```
3. Open the browser ```http://127.0.0.1:8000/``` 

## To run the classfication

1. run ```git-lfs fetch``` and ```git-lfs checkout``` to download the ml model from repo
2. run ```git submodule init``` and ```git submodule update```
3. Follow the step on the jupyter notebook to run the ml model
