def get_jupyter_url(user_id, kubernetes_master, repo_provider,
                    username, repo_name, branch, lab_id):
    import json
    import os
    import requests

    binderhub_base_url = json.loads(
        os.environ['BINDERHUB_URL_DICT'])[kubernetes_master]

    spec = '{username}/{repo_name}/{branch}'.format(
        username=username, repo_name=repo_name, branch=branch)

    url = '{binderhub_base_url}/build/{provider_prefix}/{spec}'.format(
        binderhub_base_url=binderhub_base_url, provider_prefix=repo_provider,
        spec=spec)

    with requests.get(url, stream=True) as response:
        content = response.content

        for ei in content.split('\n\n'):
            if 'data: ' in ei:
                import json
                d = json.loads(ei.replace('data: ', ''))
                if d['phase'] == 'ready':
                    print(d)

    return {
        'jupyter_url': jupyter_url,
        'hostname': hostname
    }
