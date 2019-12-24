def lambda_handler(event, context):
    if event['function_type'] == 'GET':
        from s3_utility import S3Utility
        s3 = S3Utility()
        lab_id = event['lab_id']
        user_id = event['user_id']
        object_name = event['object_name']
        key_name = '{lab_id}/{user_id}/{object_name}'.format(
            lab_id=lab_id, user_id=user_id, object_name=object_name)
        expires_in_seconds = event.get('expires_in_seconds', 3600)
        presigned_url = s3.get_presigned_url(
            key_name, expires_in_seconds=expires_in_seconds)
        return {'url': presigned_url}

    elif event['function_type'] == 'POST':
        from s3_utility import S3Utility
        s3 = S3Utility()
        lab_id = event['lab_id']
        user_id = event['user_id']
        file_to_write = event['file_to_write']
        object_name = event['object_name']
        key_name = '{lab_id}/{user_id}/{object_name}'.format(
            lab_id=lab_id, user_id=user_id, object_name=object_name)
        expires_in_seconds = event.get('expires_in_seconds', 3600)
        s3.post_with_presigned_url(file_to_write, key_name, expires_in_seconds)
        return

    elif event['function_type'] == 'CREATE':
        from s3_utility import S3Utility
        s3 = S3Utility()
        lab_id = event['lab_id']
        user_id = event['user_id']
        object_name = event['object_name']
        key_name = '{lab_id}/{user_id}/{object_name}'.format(
            lab_id=lab_id, user_id=user_id, object_name=object_name)
        expires_in_seconds = event.get('expires_in_seconds', 3600)
        return s3.create_presigned_post(key_name,
                                        expires_in_seconds=expires_in_seconds)
