def prepare_files(self):
    import os
    for line in open("/etc/plymouth/plymouthd.conf", 'r').readlines():
        if line.find('Theme') != -1:
            theme = "/usr/share/plymouth/themes/" + line.removeprefix('Theme=').strip('\n')
    self['dependencies'] = [theme, '/usr/lib64/plymouth/', '/etc/plymouth/plymouthd.conf', '/usr/share/plymouth/themes/text/text.plymouth', '/usr/share/plymouth/themes/details/details.plymouth']


def start_plymouth(self):
    """
    Runs plymouthd
    """
    return ['mkdir -m755 -p /dev/pts',
            'mount -t devpts devpts /dev/pts -o nosuid,noexec,gid=5,mode=620',
            'plymouthd --mode=boot --pid-file=/run/plymouth/pid --attach-to-session',
            'plymouth show-splash']