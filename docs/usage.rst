===
Uso
===

Ejecutar el *scraper* para jalar los registros de la institución Estatal
------------------------------------------------------------------------
"Manolo" tiene un *scraper* que se encarga de jalar las visitas registradas en
la web de la institución estatal. Para esto es necesario utilizar la línea
de comandos de un terminal y además se necesita especificar la dirección URL
del registro de visitas en línea.

Ejemplo para *scrappear* el registro de visitas de la OSCE::

    python manage.py scraper --url http://visitas.osce.gob.pe/controlVisitas/index.php?r=consultas/visitaConsulta/index

Puedes hacer que este script funcione una vez al día, todos los días si usas
un `cronjob <https://help.ubuntu.com/community/CronHowto>`_ django-manolo

Luego de realizar la descarga de información (demorará un buen rato)
encontrarás el motor de búsqueda de Manolo en la siguiente dirección::

    http://TU-DOMINIO.com/manolo
