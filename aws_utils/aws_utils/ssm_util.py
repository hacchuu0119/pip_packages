

def get_parameters_by_path(boto3_client, param_store_path, decryption=True):
    params = {}
    return_params = boto3_client.get_parameters_by_path(Path=param_store_path, WithDecryption=decryption)
    for pram_dic in return_params['Parameters']:
        params[pram_dic['Name'].split('/')[-1]] = pram_dic['Value']
    return params


# future
#
# def param_check(check_def):
#     print(check_def.__code__.co_varnames[:check_def.__code__.co_argcount])


