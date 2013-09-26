
from cx_Freeze import setup, Executable

setup(
    name = "familysysadmin",
    version = "0.0",
    author='James Abel',
    author_email='j@abel.co',
    url='www.lat.us',
    license='LICENSE',
    description = "family system admin",
    py_modules=['*'],
    executables = [Executable("familysysadmin.py")]
)