# Install
`$ pip install "git+https://github.com/hacchuu0119/pip_packages.git#egg=ssm_util&subdirectory=ssm_util"`

# Use

## get_parameters_by_path
wrapper for boto3.get_parameters_by_path



If the parameter store has a hierarchical structure,
 the key and value can be acquired in a dictionary by specifying the absolute path above the hierarchy with the parameter key you want to acquire.

```python
from ssm_util import get_parameters_by_path

param_store_path = '/param/store/path/'

response_dict = get_parameters_by_path(ssm_client, param_store_path)
```


# Argument
## ssm_client
`ssm_client` is bot3 ssm client.
```python
import boto3

aws_ssm_client = boto3.client('ssm', region_name='your_region',
                              aws_access_key_id='your_access_key_id',
                              aws_secret_access_key='your_secret_access_key')
``` 




# Requirements
See `install_requires` in [setup.py](./setup.py) 
