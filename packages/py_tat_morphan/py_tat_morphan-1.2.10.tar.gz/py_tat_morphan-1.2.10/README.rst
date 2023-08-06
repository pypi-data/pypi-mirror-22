Morphological Analyser of Tatar language
========================================

Morphological Parser of Tatar language. Uses HFST-tool.
Web form which uses this tool: http://tatmorphan.pythonanywhere.com/


To install:
-----------

$ pip install py_tat_morphan

or

$ git clone https://yaugear@bitbucket.org/yaugear/py_tat_morphan.git

$ cd py_tat_morphan

$ python setup.pu install


To use lookup:
--------------

$ tat_morphan_lookup


To process text:
----------------

$ tat_morphan_process_text <filename>


To process whole folder:
------------------------

$ tat_morphan_process_folder <path_from>

or

$ tat_morphan_process_folder <path_from> <path_to>

Note: if you do not provide <path_to>, programm puts analyzed texts into folder near initial with '_analyzed' postfix. Eg, if <path_from>='/home/ramil/mytexts/', then <path_to>='/home/ramil/mytexts_analyzed/'.


To use as python module:
------------------------

>>> from py_tat_morphan.morphan import Morphan
>>> morphan = Morphan()
>>> print(morphan.analyse('урманнарга'))
урман+N+PL(ЛАр)+DIR(ГА);
>>> print(morphan.lemma('урманнарга'))
[u'\u0443\u0440\u043c\u0430\u043d']
>>> print(morphan.pos('урманнарга'))
[u'N']
>>> print(morphan.process_text('Без урманга барабыз.'))
Без
без+N+Sg+Nom;без+PN;
урманга
урман+N+Sg+DIR(ГА);
барабыз
бар+V+PRES(Й)+1PL(бЫз);
.
Type1

>>> print(morphan.analyse_text('Без урманга барабыз.'))
[[(u'\u0411\u0435\u0437', u'\u0431\u0435\u0437+N+Sg+Nom;\u0431\u0435\u0437+PN;'), (u'\u0443\u0440\u043c\u0430\u043d\u0433\u0430', u'\u0443\u0440\u043c\u0430\u043d+N+Sg+DIR(\u0413\u0410);'), (u'\u0431\u0430\u0440\u0430\u0431\u044b\u0437', u'\u0431\u0430\u0440+V+PRES(\u0419)+1PL(\u0431\u042b\u0437);'), (u'.', 'Type1')]]
>>> print(morphan.disambiguate_text('Язгы ташуларда көймә йөздерәбез.'))
[[(u'\u042f\u0437\u0433\u044b', u'\u044f\u0437\u0433\u044b+Adj;'), (u'\u0442\u0430\u0448\u0443\u043b\u0430\u0440\u0434\u0430', u'\u0442\u0430\u0448\u0443+N+PL(\u041b\u0410\u0440)+LOC(\u0414\u0410);\u0442\u0430\u0448\u044b+V+VN_1(\u0443/\u04af/\u0432)+PL(\u041b\u0410\u0440)+LOC(\u0414\u0410);'), (u'\u043a\u04e9\u0439\u043c\u04d9', u'\u043a\u04e9\u0439\u043c\u04d9+N+Sg+Nom'), (u'\u0439\u04e9\u0437\u0434\u0435\u0440\u04d9\u0431\u0435\u0437', u'\u0439\u04e9\u0437+V+CAUS(\u0414\u042b\u0440)+PRES(\u0419)+1PL(\u0431\u042b\u0437);\u0439\u04e9\u0437\u0434\u0435\u0440+V+PRES(\u0419)+1PL(\u0431\u042b\u0437);'), (u'.', 'Type1')]]

To test:
--------

$ python setup.py test


For feedback:
-------------

ramil.gata@gmail.com


Versions:
---------

1.2.1 
|    Uses HFST python package

1.2.2 
|    Add tat_morphan_lookup and tat_morphan_process_text scripts to bin/

1.2.3 
|    Fixed exception dictionary

1.2.4 
|    Fixed to use C HFST package 

|    Added tat_morphan_process_folder script to bin/

|    Added Russain Morphological Analyser (pymorphy2 package) to detect russian words in text

1.2.5
|   Fixed morphophonetic and morphotacktic rules

|   Added tat_morphan_stats_of_folder script to bin/

1.2.6
|   Fixed dictionary collection

1.2.7
|   Added morphological disambiguation stage using contextual rules methods

|   Fixed Russian word detection

|   Fixed tat_morphan_stats_of_folder script

1.2.8
|   Fixed bug with '-'

|   Added fifth type for contextual rules. Now you can check if word starts with capital letter

|   Added is_amtype_pattern method to check if amtype is formed properly

1.2.9
|   Fixed exception dictionary

|   Fixed dictionary collection. Added Russian towns names

|   Fixed some errors with loanwords

1.2.10
|   Fixed bug with disambiguation

|   Fixed exception dictionary