[![Build Status](https://travis-ci.org/mini-kep/full-app.svg?branch=dev)](https://travis-ci.org/mini-kep/full-app)

# full-app
Keep all functionality for (parsers + db + frontend API)  inside one Django project.


Suggested components:

1. Parser yields datapoints based on call with varname and frequency.
   Can yield random values for a prototype.

2. Import broker calls parser and stores datapoints in database.

3. Database stores datapoints. For simlicity overwrite existing datapoints with newer ones.

4. End user API allows querying database to by varname/frequency

Simplifications:
- No time limits
- Same API to enduser and to parser


## Django Rest API project: mini-kep

### Install project
#### 1. Create virtual enviroment with Python 3.6 and start it:
    virtualenv -p python3.6 minikep
    source /minikep/bin/activate
#### 2. Clone proect from git and install requirements:
    git clone https://github.com/mini-kep/full-app.git full-app
    cd full-app
    pip install -r requirements.txt

### Run the project:
    python manage.py runserver
 If you are not using virtual environment with defined python version 3.6 you need to follow this command:   
    
    python3 manage.py runserver
 

#### Login:
    http://localhost:8000/auth/login/?next=/
    user: admin
    pass: asdasdasd

#### Datapoint page:
    http://localhost:8000/api/datapoints/
   
#### API page:
    http://localhost:8000/api/

#### Tests:
Run tests:
    
    python manage.py test
You can look to api/tests to check how CRUD works for Datapoint
   

#### About project:
It's a simple Django Rest Api project.

Project has one model:
    minikep.api.models.Datapoint. 

The model has appropriate serializer:
    minikep.api.serializers.DatapointSerializer 

This view takes data from the model to API for CRUD operations:  
    minikep.api.views.DatapointViewSet

Global Django settings for whole project:
      Minikep.minikep

#### Database
Now project works with sqlite, so you can easy install it locally 
and check how it works.
    
### Travis
Project work with continuous integration service. Now it works with dev branch. It run all tests before deploying changes on Git.
.travis.yml - main configuration file for Travis

### Heroku
    https://rocky-ridge-15355.herokuapp.com/api/
    user: admin
    pass: asdasdasd

