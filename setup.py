import cx_Freeze

executables = [
    cx_Freeze.Executable("client.py"),
    cx_Freeze.Executable("server.py")
]

cx_Freeze.setup(
    name="A bit Racey",
    options={"build_exe": {"packages": ["pygame"], "include_files": [
        'assets/',
        'config.json',
        'constants.py',
        'scripts/'
    ]}},
    executables=executables
)

# python setup.py build
