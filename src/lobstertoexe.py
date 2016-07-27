#-------------------------------------------------------------------------------
# Name:        guifpy2exe.py
# Purpose:     This is a config file used to build GUIF.exe.
# Author:      Anirudh Sureka
# Created:     11/09/2011
# Copyright:   (c) LeCroy Corp. 2011
# Licence:     all rights reserved.
#-------------------------------------------------------------------------------


# ...
# ModuleFinder can't handle runtime changes to __path__, but win32com uses them
try:
    # py2exe 0.6.4 introduced a replacement modulefinder.
    # This means we have to add package paths there, not to the built-in
    # one.  If this new modulefinder gets integrated into Python, then
    # we might be able to revert this some day.
    # if this doesn't work, try import modulefinder
    try:
        import py2exe.mf as modulefinder
    except ImportError:
        import modulefinder
    import win32com, sys
    for p in win32com.__path__[1:]:
        modulefinder.AddPackagePath("win32com", p)
    for extra in ["win32com.shell"]: #,"win32com.mapi"
        __import__(extra)
        m = sys.modules[extra]
        for p in m.__path__[1:]:
            modulefinder.AddPackagePath(extra, p)
except ImportError:
    # no build path setup, no worries.
    pass


from distutils.core import setup
import py2exe
import glob, matplotlib
import LecroyUtil_portable # We need to import the glob module to search for all files.

# Remove the build folder, a bit slower but ensures that build contains the latest
import shutil
shutil.rmtree("build", ignore_errors=True)

# We need to exclude matplotlib backends not being used by this executable.  You may find
# that you need different excludes to create a working executable with your chosen backend.
# We also need to include include various numerix libraries that the other functions call.
# NOTE: added scipy.sparse.csgraph because files were missing in library.zip after creating GUIF.exe
package_includes = ["numpy.core.umath","scipy.integrate._quadpack","scipy.sparse.linalg.isolve._iterative",
                   "scipy.linalg._flinalg","scipy.io","wx","wx.lib","wx.html","subprocess","scipy.sparse.csgraph"];
opts = {
        'py2exe': {
                   'optimize': 2, # 0 (None), 1 (-O), 2 (-OO)
                   'packages': package_includes,
                   'xref': False,
                   'includes' : ["sip", "matplotlib.backends",
                                   "matplotlib.figure","pylab", "numpy",
                                   "matplotlib.backends.backend_tkagg","matplotlib.backends.backend_wxagg",
								   "matplotlib.backends.backend_qt4agg",
				                   "scipy.io.matlab.streams","email.mime.multipart","email.mime.text"
                                   ],
                   'excludes':  ['_gtkagg', '_tkagg', '_agg2', '_cairo', '_cocoaagg',
                                 '_fltkagg', '_gtk', '_gtkcairo'],
                   'dll_excludes': ['libgdk-win32-2.0-0.dll',
                                     'libgobject-2.0-0.dll',
                                     'w9xpopen.exe'],
                   'bundle_files': 3
                  }
       }

#win32Files = LecroyUtil_portable.FindAllFilesInDirTree(rootPath=r'C:\Python26\Lib\site-packages\win32')
#win32comFiles = LecroyUtil_portable.FindAllFilesInDirTree(rootPath=r'C:\Python26\Lib\site-packages\win32com')

# Save matplotlib-data to mpl-data ( It is located in the matplotlib\mpl-data
# folder and the compiled programs will look for it in \mpl-data
# note: using matplotlib.get_mpldata_info
data_files = [
                    # Because matplotlibrc does not have an extension, glob does not find it (at least I think that's why)
                    # So add it manually here:
                  (r'', glob.glob(r'C:\Python27\Lib\site-packages\Pythonwin\mfc90.dll')),
                  (r'', glob.glob(r'C:\work\webzinc\mauisoft\main\Applications\Utilities\GUIF\msvcp90.dll')),
                  (r'', glob.glob(r'C:\Python27\Lib\site-packages\wx-2.8-msw-unicode\wx\gdiplus.dll')),
#                  (r'win32', win32Files),
#                  (r'win32com', win32comFiles),
                  (r'', glob.glob(r'C:\Python27\Lib\site-packages\Pythonwin\mfc90.dll')),
                  (r'', glob.glob(r'C:\Python27\lib\site-packages\numpy\core\umath.pyd')),
                  (r'', glob.glob(r'C:\Python27\lib\site-packages\scipy\integrate\_quadpack.pyd')),
                  (r'', glob.glob(r'C:\Python27\lib\site-packages\scipy\sparse\linalg\isolve\_iterative.pyd')),
                  (r'', glob.glob(r'C:\Python27\lib\site-packages\wx-2.8-msw-unicode\wx\gdiplus.dll')),
                  (r'', glob.glob(r'C:\Python27\lib\site-packages\scipy\linalg\_flinalg.pyd'))]
data_files += matplotlib.get_py2exe_datafiles()

# for console program use 'console = [{"script" : "scriptname.py"}]
setup(windows=[{"script" : "lobsterapp.py"}], options=opts,   data_files=data_files)
#setup(console = ["GUIF.py"], options=opts,   data_files=data_files)