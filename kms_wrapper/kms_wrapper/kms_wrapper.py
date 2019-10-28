import boto3
import Cryptodome.Cipher.AES as AES
from Cryptodome import Random


def __create_aes(key, iv, aes_mode):
    return AES.new(key=key, mode=aes_mode, iv=iv)


def encrypt(kms_client, kms_key_id, plain_data, aes_mode=AES.MODE_CBC):
    """
    :param kms_client: boto3_kms_client
    :param kms_key_id: aws_kms_key_id, ARMでもok
    :param plain_data: 暗号化するデータ
    :param aes_mode: Cryptodome.Cipher.AES.AES_mode(int)
    :return: iv + 暗号化文字列, data_keyを暗号化したもの
    """
    secret = kms_client.generate_data_key(KeyId=kms_key_id, KeySpec='AES_256')

    data_key = secret['Plaintext']

    #  padding
    bs = AES.block_size
    padding_data = plain_data.encode('utf-8')
    padding_length = (bs - len(padding_data) % bs) or bs
    padding_data += "".rjust(padding_length, "\x00").encode("utf-8")

    #  make iv
    iv = Random.new().read(AES.block_size)

    return iv + __create_aes(data_key, iv, aes_mode).encrypt(padding_data), secret['CiphertextBlob']


def decrypt(kms_client, iv_cipher, encrypt_data_key, aes_mode=AES.MODE_CBC):
    """
    :param kms_client: boto3_kms_client
    :param iv_cipher: iv + 暗号化文字列
    :param encrypt_data_key: data_keyの暗号化
    :param aes_mode: Cryptodome.Cipher.AES.AES_mode(int)
    :return: decrypt_data
    """
    secrets = kms_client.decrypt(CiphertextBlob=encrypt_data_key)
    data_key = secrets['Plaintext']

    #  pick iv
    iv, cipher = iv_cipher[:AES.block_size], iv_cipher[AES.block_size:]

    return __create_aes(data_key, iv, aes_mode).decrypt(cipher).decode('utf-8').rstrip('\x00')


if __name__ == '__main__':
    aws_kms_client = boto3.client('kms', region_name='',
                                  aws_access_key_id='',
                                  aws_secret_access_key='')

    from kms_wrapper.kms_wrapper import encrypt, decrypt

    enc_data, enc_data_key = encrypt(aws_kms_client, '', 'password')

    print(f'enc_data: {enc_data}, enc_data_key: {enc_data_key}')

    decrypt_data = decrypt(aws_kms_client, enc_data, enc_data_key)

    print(f'decrypt_data: {decrypt_data}')


