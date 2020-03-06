from cx_Freeze import setup, Executable

base = "Win32GUI"

executables = [Executable( "PTax.py", base=base, icon="favicon.ico" )]
excludes = []  # 'asyncio',"tkinter",'test','xml', 'xmlrpc', 'sqlite3'
include_files = ['mainwindow.ui','license','Splash.png']
packages = ["idna", "PySide2",
            "taxjar", "uszipcode", "sys","time","pyautogui","pickle"]
shortcut_table = [
    ("DesktopShortcut",         # Shortcut
     "DesktopFolder",           # Directory_
     "PTax_shortcut",                 # Name
     "TARGETDIR",               # Component_
     "[TARGETDIR]PTax.exe",  # Target
     None,                      # Arguments
     None,                      # Description
     None,                      # Hotkey
     None,                      # Icon
     None,                      # IconIndex
     None,                      # ShowCmd
     'TARGETDIR'                # WkDir
     )
    ]

options = {
    'bdist_msi': {
        'install_icon':"favicon.ico",
        'upgrade_code':'987654-123-56789-1',
        'data': {"Shortcut": shortcut_table}},
    'build_exe': {
        'packages': packages, 'excludes': excludes, 'include_files': include_files,'include_msvcr': True,
    },

}

setup(
    name="PTax",
    options=options,
    version="1.1.0",
    description='',
    executables=executables
)
#python setup.py bdist_msi
#python setup.py build