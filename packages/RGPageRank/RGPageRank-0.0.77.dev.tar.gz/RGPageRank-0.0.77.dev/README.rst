PageRank
========

Google page rank

Installation
------------

    pip install RGPageRank


Usage
-----

    from RGPageRank import PageRank

`You may pass either directory name or dictionary with data as a first (data) parameter to the new object:`


    dir_pg = PageRank('directory_name', recursive=True, truncate_extension=True)


Where:

1. directory_name - can be either absolute path to a directory or relative path, in the second case the script will use path of the script where the script file contains
2. recursive - read nested directories or not
3. truncate_extension - truncate extensions of the files

`Each file name inside the directory is a node name and content are the corresponding data:`

dir:

1. test.txt
2. test1.txt
3. nested_dir:

    1. test2.txt
    2. test.txt

`So it will be: {'test': 'test data', 'test1': 'test1 data', 'test2': 'test2 data'}`

`If there are files with the same name the content of the files will be merged, so the dict above will contain
data from 'dir/test.txt' and 'dir/nested_dir/test.txt' for the 'test' key`

    dict_pg = PageRank({'Jimmy': 'Hello John and Carl, Carl', 'Carl': 'Hi John', 'John': 'Sup Jimmy and Carl'})

`To get page rank for the data use either 'page_rank()' or 'sorted_page_rank()'`

    print(dict_pg.page_rank())

    print(dict_pg.sorted_page_rank(reverse=True))

`There are also two helper classes: DictTransformer and DirectoryTransformer which is actually transform a given data
to a directed graph you may use it to get the graph and do something with it or draw the graph`

    from RGPageRank import DictTransformer

    from RGPageRank import DirectoryTransformer

    #dir_transformer = DirectoryTransformer('directory_name', recursive=True, truncate_extension=True)

    dict_transformer = DirectoryTransformer({'Jimmy': 'Hello John and Carl, Carl', 'Carl': 'Hi John', 'John': 'Sup Jimmy and Carl'})

    #print(dir_transformer.make_graph())

    #dir_transformer.draw_graph()

    print(dict_transformer.make_graph())

    dict_transformer.draw_graph()
