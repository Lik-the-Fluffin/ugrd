from zenlib.util import contains

@contains('validate', "validate is not enabled, skipping cmdline validation.")
def _validate_cmdline(self) -> None:
    f = open("/proc/cmdline", 'r').read()
    if not ('quiet' in f and 'splash' in f):
        self.logger.warning('current cmdline is missing "splash quiet" parameters, they are important for plymouth to work')

    
def prepare_files(self):
    from os.path import join
    from os import walk
    for line in open("/etc/plymouth/plymouthd.conf", 'r').readlines():
        if line.find('Theme') != -1:
            theme = "/usr/share/plymouth/themes/" + line.removeprefix('Theme=').strip('\n')
    dir_list = [theme, '/usr/lib64/plymouth/', '/etc/plymouth/plymouthd.conf', '/usr/share/plymouth/themes/text/text.plymouth', '/usr/share/plymouth/themes/details/details.plymouth']
    for dir_path in dir_list:
        self['dependencies'] = self['dependencies'] + [join(dirpath,f) for (dirpath, dirnames, filenames) in walk(dir_path) for f in filenames]


def start_plymouth(self):
    """
    Runs plymouthd
    """
    return ['mkdir -m755 -p /dev/pts',
            'mount -t devpts devpts /dev/pts -o nosuid,noexec,gid=5,mode=620',
            'plymouthd --mode=boot --pid-file=/run/plymouth/pid --attach-to-session',
            'plymouth show-splash']