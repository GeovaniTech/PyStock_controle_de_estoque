import cx_Freeze

executables = [cx_Freeze.Executable('PyStock - App.py', icon='View/Imagens/Logo Ico.ico')]

cx_Freeze.setup(
    name="PyStock",
    options={'build_exe': {'packages': ['PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets', 'mysql.connector', 'os', 'sys'],
                           'include_files': ['View/']}},
    executables=executables
)