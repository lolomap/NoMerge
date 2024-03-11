from cx_Freeze import setup, Executable

setup(
	name='NoMerge',
	version='0.1',
	description='Service for tracking simultaneous editing to prevent merge problems with binary files',
	executables=[Executable('client.pyw', base='Win32GUI')]
)
