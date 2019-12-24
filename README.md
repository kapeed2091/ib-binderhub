# BinderHub


# Set Environment Variables

* S3_AWS_BUCKET_NAME
* S3_AWS_REGION
* S3_AWS_ACCESS_KEY_ID
* S3_AWS_SECRET_ACCESS_KEY
* BINDERHUB_URL_DICT


# Usage


## Get Jupyter URL
```bash
get_jupyter_url
    request
        user_id <str>: User requesting for Jupyter URL
        kubernetes_master_type <str>: The master instance in which we deploy the jupyter pod
        repo_provider <str>:
            - GitHub: gh
            - GitLab: gl
        username <str>: owner of the repo provider which has access
        repo_name <str>: 
        branch <str>: repo branch through which content has to be pulled
        lab_id <str>:
    
    response
        metadata related to pod
```


## Quit/Shutdown Jupyter
```
python /home/jovyan/shutdown_jupyter.py
``` 
or 
```
>> ipython
>> import ib_binderhub
>> ib_binderhub.shutdown_jupyter
```

# Other Components of Repo

## PostStart
Pulls user related changes from S3 as patch file and apply

## PreStop
Pushes user related changes to S3 as git-patch file


