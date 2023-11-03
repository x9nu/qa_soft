之前打包一直不对劲，最后用多文件打包成exe：

pyinstaller [主文件] -p [副文件] -p[其他副文件]

-F 只生成一个exe

-w 打开程序不显示黑色控制台

-i 指定图标

用以上方法可以打包成一个完整的exe，但是运行时，弹出一个窗口，有如下报错：

```shell
Traceback (most recent call last):
  File "main.py", line 2, in <module>
  File "PyInstaller\loader\pyimod02_importers.py", line 391, in exec_module
  File "gui.py", line 6, in <module>
  File "PyInstaller\loader\pyimod02_importers.py", line 391, in exec_module
  File "excel_processor.py", line 1, in <module>
  File "PyInstaller\loader\pyimod02_importers.py", line 391, in exec_module
  File "openpyxl\__init__.py", line 6, in <module>
  File "PyInstaller\loader\pyimod02_importers.py", line 391, in exec_module
  File "openpyxl\workbook\__init__.py", line 4, in <module>
  File "PyInstaller\loader\pyimod02_importers.py", line 391, in exec_module
  File "openpyxl\workbook\workbook.py", line 9, in <module>
  File "PyInstaller\loader\pyimod02_importers.py", line 391, in exec_module
  File "openpyxl\worksheet\_write_only.py", line 13, in <module>
  File "openpyxl\worksheet\_writer.py", line 23, in init openpyxl.worksheet._writer
ModuleNotFoundError: No module named 'openpyxl.cell._writer'
```



然后我加上了--hidden-import=openpyxl.cell._writer

最终用下面命令成功了！！！

```shell
pyinstaller main.py -p gui.py -p record.py -p excel_processor.py -F -w -i f.ico --hidden-import=openpyxl.cell._writer
```



