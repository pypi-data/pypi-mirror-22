===========
Instalación
===========


Se basa y se implementa en Python. 3. Antes de la instalación completa de
Pytuñol, es necesario instalar antes algunas bibliotecas adicionales de Python.
Las instrucciones de instalación difieren ligeramente en cada plataforma.


-----
Linux
-----

Necesita Python3 y PyQt5. Hay una posibilidad razonable de que ambos estén
instalados. Si su distribución se basa en Debian / Ubuntu, el comando siguiente
garantiza que todas las bibliotecas necesarias se instalarán

::

    $ sudo apt-get install python3-all python3-pyqt5 python3-pyqt5.qsci
      python3-pyqt5.qtsvg python3-pyqt5.qtwebkit python3-pip
        
Si sólo desea realizar la instalación local, el comando queda:

    $ pip3 install pytunol --user

(Ignore la opción --user, si desea instalar para todos los usuarios, en cuyo
caso es necesario ejecutar el comando como * sudo *.). Una vez instalado,
puede actualizar la versión de Pytuñol ejecutando:
    
    $ pip3 install pytunol -U --user

La secuencia de comandos de instalación guarda los archivos ejecutables en la
carpeta `` ~ / .local / bin.`` y en la carpeta `` / bin / `` si existe la misma.


-------
Windows
-------

Hay dos opciones de instalación en Windows. La primera funciona sólo para
Windows 64bits y consiste en descargar el archivo auto-ejecutable del pytunol.
Descargue este archivo en cualquier lugar de su ordenador y ejecútelo con un
doble clic.

.. __: http://tinyurl.com/pytg-exe

La segunda opción consiste en descargar los paquetes de Python 3.4 y PyQt5
manualmente y realizar la instalación vía pip. Para ello, elija los instaladores
correspondientes a su versión de Windows.

32 bits
- -------

* `Python 3.4`__
* `PyQt5`__

.. __: https://www.python.org/ftp/python/3.4.4/python-3.4.4.msi
.. __: https://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.5.1/PyQt5-5.5.1-gpl-Py3.4-Qt5.5.1-x32.exe


64 bits
- -------

* `Python 3.4`__
* `PyQt5`__

.. __: https://www.python.org/ftp/python/3.4.4/python-3.4.4.amd64.msi
.. __: https://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.5.1/PyQt5-5.5.1-gpl-Py3.4-Qt5.5.1-x64.exe

Es importante marcar la opción "Agregar python.exe a su ruta" durante la 
instalación. Esto facilitará la ejecución del Pytgués posteriormente. Una vez 
finalizada la instalación, abra el terminal de Windows (Win + R y escriba "cmd") 
y ejecute los comandos:

    python -m pip install pytunol -U

Si el código anterior no funciona, probablemente significa que Python no está 
en la ruta predeterminada de búsqueda de Windows. Si este es el caso, es 
necesario cambiar al directorio donde está instalado Python. Escriba:

    cd c:\Python34\
    
Ahora repita los comandos anteriores. Si ha decidido instalar Python en otra 
ruta, modifique el comando anterior para indicar la ruta correcta.

Para ejecutar en modo gráfico, presione Win + R y escriba "pytunol" en el 
indicador. Si esto no funciona (especialmente en las versiones más recientes 
de Windows), busque el ejecutable de tugalitas en la carpeta 
``c:\Python34\Scripts\`` o ejecute el comando ``python -m pytunol`` del terminal.