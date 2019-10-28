# Install
`$ pip install "git+https://github.com/hacchuu0119/pip_packages.git#egg=pydb&subdirectory=pydb"`

# Use

## oracle

```python
from pydb import oracle
oracle_conn = oracle(user='oracle', password='oracle', host='xx.xx.xx.xx', port='5432', sid='oracle', encoding='utf-8')
```

## mysql
```python
from pydb import mysql
mysql_conn = mysql(user='mysql', password='mysql', host='xx.xx.xx.xx', port='3306', database='mysql')
```

# How
## execute
```python
mysql_conn.execute("sql")
```

# Requirements
See `install_requires` in [setup.py](./setup.py) 
