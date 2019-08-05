# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

def get_seaborn_path():
    import seaborn
    seaborn_path = seaborn.__path__[0]
    return seaborn_path
def get_pandas_path():
    import pandas
    pandas_path = pandas.__path__[0]
    return pandas_path


a = Analysis(['U:\\MaxFung\\Source_Code\\REX_Dev\\rex.py'],
             pathex=['C:\\engapps\\Anaconda\\Scripts'],
             binaries=[],
             datas=[],
             hiddenimports=['scipy._lib.messagestream',     'pandas._libs.tslibs.timedeltas '],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

dict_tree = Tree(get_seaborn_path(), prefix='seaborn', excludes=["*.pyc"])
dict_tree2 = Tree(get_pandas_path(), prefix='pandas', excludes=["*.pyc"])
a.datas += dict_tree
a.datas += dict_tree2
a.binaries = filter(lambda x: 'seaborn' not in x[0], a.binaries)
a.binaries += filter(lambda x: 'pandas' not in x[0], a.binaries)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='rex',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False, icon='U:\\MaxFung\\Source_Code\\REX_Dev\\icon.ico' )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='rex')
