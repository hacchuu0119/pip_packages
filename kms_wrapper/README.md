# Install
`$ pip install "git+https://github.com/hacchuu0119/pip_packages.git#egg=kms_wrapper&subdirectory=kms_wrapper"`

# Use

## Encrypt

```python
from kms_wrapper import encrypt
encrypt_data, encrypt_data_key = encrypt(kms_client, kms_key_id, plain_data)
```

## Decrypt
```python
from kms_wrapper import decrypt
plain_data = decrypt(kms_client, encrypt_data, encrypt_data_key)
```

# How
## AES Mode
If you want change AES_MODE

```python
from kms_wrapper import encrypt, decrypt

encrypt(kms_client, kms_key_id, plain_data, aes_mode=AES_MODE) # Specify 'aes_mode'

decrypt(kms_client, encrypt_data, encrypt_data_key, aes_mode=AES_MODE) # Specify 'aes_mode'
```

Of course, 'encrypt' and 'decrypt' in the same encryption format.

### The type of AES mode is the following URL
https://github.com/Legrandin/pycryptodome/blob/5b4e8d882e57280d640a3f8aae3d6ad4732f5502/lib/Crypto/Cipher/AES.py#L235-L245

## Argument
`kms_client` is bot3 kms client.
```python
import boto3

aws_kms_client = boto3.client('kms', region_name='your_region',
                              aws_access_key_id='your_access_key_id',
                              aws_secret_access_key='your_secret_access_key')
``` 

# Requirements
See `install_requires` in [setup.py](./setup.py) 
