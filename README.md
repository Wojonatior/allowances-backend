### Secret key

To generate a secret key, run the following in Python:

```python
import os
os.urandom(24)
```

The output is a suitable secret key, per the [Flask documentation](http://flask.pocoo.org/docs/quickstart/)


When first installing the app run the following command to install dependencies
`pipenv install`

From then on, use the following command to setup the environment for development
`pipenv shell`

You can leave this special enviroment with the `exit` command
