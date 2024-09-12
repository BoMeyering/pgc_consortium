# PGC Consortium
Django app for perennial groundcover related standard operating procedures and data.

## Current Progress
* Main applications are instantiated each with their own models and admin pages
  * `data_storage`: Contains the main types of data storage for the project including trials, plots, and observations.
  * `resources`: Contains metadata storage that doesn't directly affect the observational/trial level data.
  * `ontology`: This app contains the models and view pertaining to variables, and controlled vocabulary terms
  * `imaging`: This app contains a few models related to image storage locally as well as the deep learning models hosted in AWS used to process those images
  * `api`: This is a DRF app that contains the routes and views for various api calls
* A few different API calls on some of the simpler tables have been written and are implemented.
* Database design is at a good stage and can handle most of the business needs.
* UI and navbar is workable.
* Some trial and plot geometry is worked out in geojson format.
## To Do
There are many outstanding tasks that need to be completed
- [ ] Go over the database schema with stakeholders and think through any edge cases
- [ ] Finish migrating any models and views to their respective apps
- [ ] Get the trial information uploader working
- [ ] Implement mapping functionality with leaflet
- [ ] Finish building out the API and the Swaggerhub API page
- [ ] Ontology browser?
- [ ] Migrate email server from Google to Sendmail
- [ ] Other things?

## Starting the Application
The docker compose yaml file currently has no volumes attached so no data is persisted if the database is spun down.
If there are any migrations that you need to get rid of, run
```
$ find . -path '*/migrations/*.py' ! -name '__init__.py' | xargs rm
```
First, spin up the docker containers for the database and the adminer page
```
$ docker compose up -d
```
Then run the development server
```
$ python manage.py runserver
```
Pull open a new terminal and run migrations
```
$ python manage.py makemigrations
$ python manage.py migrate
```
Open the app at `localhost:8000/`
