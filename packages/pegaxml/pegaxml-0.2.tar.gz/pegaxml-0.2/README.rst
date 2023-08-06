Exercícios Pypratico
--------------------

.. image:: https://travis-ci.org/mulhergorila/pypraticopegaxml.svg?branch=master
    :target: https://travis-ci.org/mulhergorila/pypraticopegaxml

.. image:: https://pyup.io/repos/github/mulhergorila/pypraticopegaxml/shield.svg
     :target: https://pyup.io/repos/github/mulhergorila/pypraticopegaxml/
     :alt: Updates

.. image:: https://pyup.io/repos/github/mulhergorila/pypraticopegaxml/python-3-shield.svg
     :target: https://pyup.io/repos/github/mulhergorila/pypraticopegaxml/
     :alt: Python 3

Exemplos de uso
---------------
Instalando o pacote via pip install

``$ pip install pegaxml``


==========
Exemplo 1:
==========

.. code-block:: python

   >>> from pegaxml.pegadados import lista_titulos
   >>> print(lista_titulos())
   ['Empire Burlesque', 'Hide your heart', 'Greatest Hits', 'Still got the blues', 'Eros', 'One night only', 'Sylvias Mother', 'Maggie May', 'Romanza', 'When a man loves a woman', 'Black angel', '1999 Grammy Nominees', 'For the good times', 'Big Willie style', 'Tupelo Honey', 'Soulsville', 'The very best of', 'Stop', 'Bridge of Spies', 'Private Dancer', 'Midt om natten', 'Pavarotti Gala Concert', 'The dock of the bay', 'Picture book', 'Red', 'Unchain my heart']


==========
Exemplo 2:
==========

.. code-block:: python

   >>> from pegaxml.pegadados import lista_titulos
   >>> titulos = lista_titulos()
   >>> for titulo in titulos:
   ...     print(titulo)

   Empire Burlesque
   Hide your heart
   Greatest Hits
   Still got the blues
   Eros
   One night only
   Sylvias Mother
   Maggie May
   Romanza
   When a man loves a woman
   Black angel
   1999 Grammy Nominees
   For the good times
   Big Willie style
   Tupelo Honey
   Soulsville
   The very best of
   Stop
   Bridge of Spies
   Private Dancer
   Midt om natten
   Pavarotti Gala Concert
   The dock of the bay
   Picture book
   Red
   Unchain my heart
