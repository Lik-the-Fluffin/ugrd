def prepare_files(self):
    from os.path import exists
    if exists("/etc/kernel/cmdline"):
        cmdline_file="/etc/kernel/cmdline"
    elif exists("/etc/kernel/uefi-mkconfig"):
        cmdline_file="/etc/kernel/uefi-mkconfig"
    else:
        cmdline_file="/proc/cmdline"
    f = open(cmdline_file, 'r').read()
    if not ('quiet' in f and 'splash' in f):
        raise ValueError('cmdline is missing "splash quiet" parameters, they are important for plymouth')
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