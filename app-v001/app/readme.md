a blog site built with flask
===

# python 

> python >= 3.7

# install libraries

```
pip install -r requirements.txt
```

# run web

```
python manage.py runserver
```

切换运行环境修改 manage.py
```
app = create_app(env_name='development')
app = create_app(env_name='production')

```

# test

```
pytest --setup-show tests/unit/
```