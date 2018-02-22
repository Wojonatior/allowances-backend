### Secret key

To generate a secret key, run the following in Python:

```python
import os
os.urandom(24)
```

The output is a suitable secret key, per the [Flask documentation](http://flask.pocoo.org/docs/quickstart/)
