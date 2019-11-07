def s3_put_object_with_partition(s3_resource, bucket, key_and_prefix, partition_column, file_body, key_name='object'):
    """
    :param s3_resource: boto3.resource
    :param bucket: bucket name
    :param key_and_prefix: save path
    :param partition_column: ex) register_date=yyyy-mm-dd
    :param file_body: text.object
    :param key_name: save file name
    :return:
    """

    key_and_prefix = key_and_prefix.rstrip('/').strip('/')

    path = key_and_prefix + "/" + partition_column + "/" + key_name

    s3_resource.Object(bucket, path).put(Body=str(file_body).encode('utf-8'),
                                         ContentEncoding='utf-8',
                                         ContentType='text/plane'
                                         )
