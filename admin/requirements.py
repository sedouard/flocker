from subprocess import check_output, check_call
from tempfile import mkdtemp
from twisted.python.filepath import FilePath

from _preamble import TOPLEVEL

venv_dir = FilePath(mkdtemp())
check_call(["virtualenv", venv_dir.path])
pip = venv_dir.descendant(["bin", "pip"])
check_call([pip.path, 'install', TOPLEVEL.path])

def get_installed_packages():
    reqs = check_output([pip.path, 'freeze']).splitlines()
    return filter(lambda req: not req.startswith('Flocker=='), reqs)

requirements = get_installed_packages()

TOPLEVEL.child('requirements.txt').setContent(
    "\n".join(requirements) + "\n"
)

check_call([pip.path, 'install', "Flocker[dev,release,doc]"])

dev_requirements = [
    req for req in get_installed_packages() if req not in req requirements
]

TOPLEVEL.child('dev-requirements.txt').setContent(
    "\n".join(dev_requirements) + "\n"
)

venv_dir.remove()
