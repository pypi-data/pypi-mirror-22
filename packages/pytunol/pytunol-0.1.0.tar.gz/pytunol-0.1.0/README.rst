========
Pytuñol
========

Pytuñol es una versión del lenguaje de programación Python que intenta acercarse 
al máximo posible de un * pseudo-código* en español. La motivación principal 
en aprender Pytuñol es evitar las barreras con la lengua inglesa cuando 
empezamos a aprender programación. Una ventaja de Pytuñol con respecto a otras 
soluciones similares es que la transición a un lenguaje de programación de uso 
común es bastante suave, ya que es posible mezclar código Python y Pytuñol en 
el mismo programa.

La sintaxis del lenguaje de programación Python a menudo se compara con un 
*pseudo-código* o un algoritmo ejecutable. A pesar de que existen algunos 
recursos sintácticos avanzados que ciertamente violan esta simplicidad, Python 
probablemente es uno de los lenguajes de programación de uso general con la
sintaxis más cercana al lenguaje natural. Los programas en Python a menudo se 
asemejan mucho a una descripción (en inglés) del algoritmo que implementa. Con 
el Pytuñol, esta facilidad también se aplica a los hablantes de el idioma de
Cervantes.

Al igual que Python, el Pytuñol es un lenguaje dinámico que no necesita ser 
compilado. El código se ejecuta directamente por el intérprete o se puede crear 
en modo interactivo en el estilo REPL (read / eval / print / loop, del inglés
bucle de lectura, evaluación e impresión). En este modo, el intérprete ejecuta 
inmediatamente los comandos introducidos por el usuario y ya muestra el 
resultado en la pantalla.

Este paquete instala el "pytunol", que consiste en un ambiente de programación 
visual, en el estilo del lenguaje LOGO. Para comenzar su interacción con 
Pytuñol, ejecute en el indicador ``$ pytunol``. Una vez abierta la ventana del 
terminal de Pytuñol, escriba el comando:

   >>> imprimir("Hola, mundo!")

¡Buena programación!


Observación
===========

Pytuñol no es un lenguaje serio. La mayoría de las traducciones se hicieron
usando google translate y mantener intencionalmente algunos errores divertidos
(pero equivocados) ::

Pecado pecado
Bronceado
* Abs -> abdominales

+muchos errores más pequeños. Incluso este mensaje fue creado con google
traductor. Así que no confíes ni siquiera en el descargo de responsabilidad
diciendo que las traducciones son malas! Nuestro objetivo es provocar a alguien
que inicie una traducción legítima al español.


Quieres probar?
===============

Pytuñol se puede instalar a través de pip (python3)::

    $ pip install pytunol[gui]