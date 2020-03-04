from cx_Freeze import setup, Executable

base = "Win32GUI"

executables = [Executable( "PTax.py", base=base, icon="favicon.ico" )]
excludes = []  # 'asyncio',"tkinter",'test','xml', 'xmlrpc', 'sqlite3'
include_files = ['mainwindow.ui']
packages = ["idna", "PySide2",
            "taxjar", "uszipcode", "sys"]

options = {
    'build_exe': {
        'packages': packages, 'excludes': excludes, 'include_files': include_files,
    },
}

setup(
    name="PTax",
    options=options,
    version="0.7.5",
    description='Beta',
    executables=executables
)
