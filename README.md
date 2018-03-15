### Secret key

To generate a secret key, run the following in Python:

```python
import os
os.urandom(24)
```

The output is a suitable secret key, per the [Flask documentation](http://flask.pocoo.org/docs/quickstart/)

You can add the heroku apps to your git using

`git remote add dev git@heroku.com:YOUR_APP_NAME.git`

`git remote add stage git@heroku.com:YOUR_APP_NAME.git`

`git remote add pro git@heroku.com:YOUR_APP_NAME.git`

Follow for the local settings, this will be to set up your .env file
https://realpython.com/blog/python/flask-by-example-part-1-project-setup/
It should look similar to the example.config file

Though this is only needed if you want auto env, otherwise leave out the exports and just assign
the variables as normal, no source.

The PLAID keys and id in the example are the plaid sandbox versions.


### Running locally

While in your virtual env, use `gunicorn -b localhost:5000 allowances.api:app`
