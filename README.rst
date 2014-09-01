mjango-manolo
=============

|Pypi index| |Build Status| |Cover alls|

Manolo, buscador de lobistas
============================

Presento un buscador de personas que ingresan las oficinas del
**Organismo Supervisor de las Contrataciones del Estado**.
http://aniversarioperu.me/manolo/

Motivación
==========

Todo aquel que visita el Organismo de Contrataciones debe registrarse
dejando su **nombre, documento de indentidad, motivo de visita, empleado
público que lo recibe, hora de ingreso, salida y fecha**. Toda esta
información está disponible en la Internet en esta dirección:
http://visitas.osce.gob.pe/controlVisitas/index.php?r=consultas/visitaConsulta/index

El problema es que la interfaz no es muy amigable y sólo se pueden
buscar visitantes a la institución por día. Seleccionas cualquier día
del menú y veras todos los visitantes que de esa fecha. Si quieres saber
cuántas veces ha visitado el lugar una determinada persona, debes buscar
día por día, página por página, revisar línea por línea en búsqueda de
la persona de interés.

Obviamente este tipo de búsqueda es muy tedioso, aburrido, inexacto (se
presta a errores de conteo) además que toma demasiado tiempo hacer una
simple búsqueda.

Por eso decidí construir un simple buscador de personas que visitan
dicha institución estatal. La función de este buscador simple: **Tipeas
un nombre y aparecerán en pantalla todas las veces que la persona tenga
ingresos registrados al Organismo de Contrataciones.**

Más información en un post en el blog Útero de Marita:

http://aniversarioperu.utero.pe/2014/03/08/manolo-buscador-de-lobistas/

Esta es la dirección web de **Manolo, buscador de personas**:
http://aniversarioperu.me/manolo/

Documentación
=============

"Manolo" es un paquete o *app* para Django y puede ser agregado
fácilmente a algún projecto de Django a manera de plugin.

La documentación completa está en este enlace:
https://django-manolo.readthedocs.org.

.. |Pypi index| image:: https://badge.fury.io/py/django-manolo.png
   :target: https://badge.fury.io/py/django-manolo
.. |Build Status| image:: https://travis-ci.org/aniversarioperu/django-manolo.png?branch=master
   :target: https://travis-ci.org/aniversarioperu/django-manolo
.. |Cover alls| image:: https://coveralls.io/repos/aniversarioperu/django-manolo/badge.png?branch=master
   :target: https://coveralls.io/r/aniversarioperu/django-manolo?branch=master
