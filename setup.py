from cx_Freeze import setup, Executable

setup(
    name = "GLASS",
    version = "0.0.1",
    description = "Grouping Ligand Alignment Sites Selectively",
    executables = [Executable("main.py", base="Console")], # Use the name of your main python file here
)