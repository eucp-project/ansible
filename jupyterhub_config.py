# Use this bind_url when using Nginx as reverse proxy
c.JupyterHub.bind_url = 'http://127.0.0.1:8000'
c.Spawner.default_url = '/lab'

# Bunch of alternative spawners
#c.JupyterHub.spawner_class='sudospawner.SudoSpawner'
#c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
#c.JupyterHub.spawner_class = 'dockerspawner.SystemUserSpawner'
c.JupyterHub.spawner_class = 'systemgroupspawner.SystemGroupSpawner'
# Note: SystemGroupSpawner inherits from SystemUserSpawner, which in its turn
# inherits from DockerSpawner
c.SystemUserSpawner.environment = {'JUPYTER_ENABLE_LAB': '1', 'GRANT_SUDO': '1', 'NB_UMASK': '0027',
                                   'CDAT_ANONYMOUS_LOG': 'no'}
c.SystemUserSpawner.host_homedir_format_string = '/mnt/users/{username}'
c.DockerSpawner.volumes = {'/mnt/users': {'bind': '/home/{username}/_users', 'mode': 'ro'},
                           #'/mnt/data/data1/thredds': {'bind': '/home/{username}/_data', 'mode': 'ro'},
                           '/mnt/data/data2/cordex-fpsc': {'bind': '/home/{username}/_cordex-fpsc', 'mode': 'ro'},
                           '/mnt/data/data3/additional_data': {'bind': '/home/{username}/_additional_data', 'mode': 'rw'},
                           '/mnt/data/data1/cp-rcm': {'bind': '/home/{username}/_cp-rcm'},
                           '/mnt/data/data2/hclim-knmi': {'bind': '/home/{username}/_hclim_knmi'},
                           '/mnt/data/data3/ALP-3/HCLIMcom': {'bind': '/home/{username}/_HCLIMcom'},
}
c.DockerSpawner.image = '{{ docker_image }}'


# Turn off; minimize non-essential warnings & errors in the logs
c.PAMAuthenticator.open_sessions = False

# https://github.com/jupyterhub/dockerspawner/issues/198#issuecomment-404412344
from jupyter_client.localinterfaces import public_ips
c.JupyterHub.hub_ip = public_ips()[0]

# The following three settings are used when running JupyterHub by itself, without a proxy
#c.JupyterHub.bind_url = 'http://server.eucp-nlesc.surf-hosted.nl:8088'
#c.JupyterHub.ssl_key = '/etc/letsencrypt/live/server.eucp-nlesc.surf-hosted.nl-0001/privkey.pem'
#c.JupyterHub.ssl_cert = '/etc/letsencrypt/live/server.eucp-nlesc.surf-hosted.nl-0001/fullchain.pem'

# Uncomment the following three debug settings when debugging
#c.Application.log_level = 'DEBUG'
#c.Spawner.debug = True
#c.SystemGroupSpawner.debug = True

# Set the following to True when debugging and testing new images
#c.DockerSpawner.remove = True

c.Spawner.http_timeout = 120
c.Spawner.start_timeout = 120

## Paths to search for jinja templates, before using the default templates.
c.JupyterHub.template_paths = ['/etc/jupyterhub/templates']
c.JupyterHub.template_vars = {'logo_url': '/hub/static/images/logo-eucp.png',
                              'eucp_url': 'https://www.eucp-project.eu' }

#c.Authenticator.delete_invalid_users = True
