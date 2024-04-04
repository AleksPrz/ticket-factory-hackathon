<B>Aplicación - Ticket Factory</B>

A continuación se describen los módulos de nuestra aplicación, así como los métodos más importantes de cada uno de ellos.

<B>Módulo: Wallet</B>

Crear clase: Dados el ID de emisor y el sufijo de clase, se crea una clase 'Pass' y se retorna la ID única de la clase,
la cual está conformada por los primeros dos atributos mencionados.

Parchear clase: Este método modifica sólo los atributos que le sean especificados.

Crear objeto: Dados el ID de emisor, el sufijo de clase, el sufijo de objeto y un diccionario que contenga los datos a
formatear en el pase, se crea un objeto del mismo, el cual es una instancia de la clase pase.

Parchear objeto: Modifica sólo ciertos campos de una instancia de una clase 'Pass'

Añadir mensaje al boleto: Dada una instancia de una clase 'Pass', se le puede enviar un mensaje pasando como argumento una
lista que contenga los datos del mensaje a enviar.

<B>Módulo: Ticket Factory</B>

Crear boleto: Genera una URL para añadir el boleto a Wallet, se registra el viaje en la base de datos, se envía por correo
el boleto y, finalmente, retorna la URL de la página del boleto web.

<B>Módulo: Ticket Web Page</B>

Ver ticket: Recibe como argumento un ID de boleto; busca en la base de datos el boleto de ese ID y rellena la plantilla 
HTML con el diseño y datos de dicho boleto.

<B>Módulo: Database</B>

Modelos: Cada uno de los modelos definen la una relación o tabla de nuestra base de datos con sus respectivos campos, mien-
tras que el conjunto de modelos definen la estructura general de la base de datos.

Archivo get.py: Mediante endpoints y métodos GET, este archivo define métodos para obtener un boleto, un viaje, una suscrip-
ción web o un código QR usando la ID del elemento deseado.

Añadir boleto a la base de datos: Mediante un endpoint y una solicitud POST, se recibe información sobre los atributos que
se desea añadir al nuevo boleto y, posteriormente, se añade a la base de datos.
