# Neighbor hood
A web application where users create profile linked to a community through which they can make posts, and interact with other Users and their businesses within a community.

## by mwaiyusuf

## User Requirements

1. Create profile and modify and access profile.
2. Signup to a Community.
3. View community posts on home page.
4. Create Business posts and View social services.
5. Search for business and their details.
6. Create new Neighbor hoods and be the Administrator.



## Models
### Post
* Properties: Title, Description, Hood  , Poster .

### Profile
* Properties: dp, Bio, location, Django User Relationship, Contact

### Hood
* Properties: Name, Bio

### Business
* Properties: Name, Owner  , Description, Number. Locale  


## Admin Dashboard
Use django admin to post photos to the database and manage the photos

## Setup

### Requirements
This project was created on a debian linux platform but should work on other unix based[not limited to] sytems.
* Tested on Debian Linux
* Python3

### Cloning the repository
```bash
git clone  https://github.com/mwaiyusuf/Neighbor-hood.git && cd Neighborhoods
```

### Creating a virtual environment

```bash
* pip3 install virtualenv
* virtualenv virtual
* . virtual/bin/activate
```
### Installing dependencies
```bash
pip install -r requirements.txt
```

### Prepare environmet variables
Create a .env file and add the following configurations to it
```python
SECRET_KEY= #secret key will be added by default
DEBUG= #set to false in production
DB_NAME=#database name
DB_USER= #database user
DB_PASSWORD=#database password
DB_HOST="127.0.0.1"
MODE= # dev or prod , set to prod during production
ALLOWED_HOSTS='.localhost', '.herokuapp.com', '.127.0.0.1'
```

### Database migrations

```bash
python manage.py migrate
```

### Running Tests
```bash
python manage.py test
```

### Running the server
```bash
* chmod a+x start.sh
* ./start.sh

```
## Contributing

- Git clone [https://github.com/mwaiyusuf/Neighbor-hood.git] 
- Make the changes.
- Write your tests.
- If everything is OK. push your changes and make a pull request.



## Technology used

* [Python3.6](https://www.python.org/)
* [Django 1.11](https://docs.djangoproject.com/en/1.11/)
* [Heroku](https://heroku.com)


## License
MIT License

Copyright(c) 2018
