# Based on https://groups.google.com/forum/#!topic/jupyter/6I9YXjrhGww
import pwd, grp
from dockerspawner import SystemUserSpawner

class SystemGroupSpawner(SystemUserSpawner):

    def get_env(self):
        """Ensure the group settings for the system user are also applied in
        the Docker container"""
        env = super().get_env()
        gid = pwd.getpwnam(self.user.name).pw_gid
        env['NB_GID'] = gid
        env['NB_GROUP'] = grp.getgrgid(gid).gr_name
        return env
