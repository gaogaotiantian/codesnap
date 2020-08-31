VizTracer
=========

.. py:class:: VizTracer(self,\
                 tracer_entries=5000000,
                 verbose=1,\
                 max_stack_depth=-1,\
                 include_files=None,\
                 exclude_files=None,\
                 ignore_c_function=False,\
                 log_print=False,\
                 pid_suffix=False,\
                 output_file="result.html")

    .. py:attribute:: tracer_entries
        :type: integer
        :value: 5000000

        Size of circular buffer. The user can only specify this value when instantiate ``VizTracer`` object. 

        ``tracer_entries`` means how many entries ``VizTracer`` can store. It's not a byte number.

    .. py:attribute:: verbose
        :type: integer
        :value: 1

        Verbose level of VizTracer. Can be set to ``0`` so it won't print anything while tracing 

        Setting it to ``0`` is equivalent to 

        .. code-block::

            python -m viztracer --quiet

    .. py:attribute:: max_stack_depth
        :type: integer
        :value: -1

        Specify the maximum stack depth VizTracer will trace. ``-1`` means infinite.

        Equivalent to 

        .. code-block::

            python -m viztracer --max_stack_depth <val>
    
    .. py:attribute:: include_files
        :type: list of string or None
        :value: None

        Specify the files or folders that VizTracer will trace. If it's not empty, VizTracer will function in whitelist mode, any files/folders not included will be ignored.
        
        Because converting code filename in tracer is too expensive, we will only compare the input and its absolute path against code filename, which could be a relative path. That means, if you run your program using relative path, but gives the ``include_files`` an absolute path, it will not be able to detect.

        Can't be set with ``exclude_files``

        Equivalent to 

        .. code-block::

            python -m viztracer --include_files file1[ file2 [file3 ...]]

        **NOTICE**

        In command line, ``--include_files`` takes multiple arguments, which will be ambiguous about the command that actually needs to run, so you need to explicitly specify comand using ``--run``

        .. code-block::

            python -m viztracer --include_files file1 file2 --run my_scrpit.py

    .. py:attribute:: exclude_files
        :type: list of string or None
        :value: None

        Specify the files or folders that VizTracer will not trace. If it's not empty, VizTracer will function in blacklist mode, any files/folders not included will be ignored.

        Because converting code filename in tracer is too expensive, we will only compare the input and its absolute path against code filename, which could be a relative path. That means, if you run your program using relative path, but gives the ``exclude_files`` an absolute path, it will not be able to detect.

        Can't be set with ``include_files``

        Equivalent to 

        .. code-block::

            python -m viztracer --exclude_files file1[ file2 [file3 ...]]
        
        **NOTICE**

        In command line, ``--exclude_files`` takes multiple arguments, which will be ambiguous about the command that actually needs to run, so you need to explicitly specify comand using ``--run``

        .. code-block::

            python -m viztracer --exclude_files file1 file2 --run my_scrpit.py

    .. py:attribute:: ignore_c_function
        :type: boolean
        :value: False

        Whether trace c function

        Setting it to ``True`` is equivalent to 

        .. code-block::

            python -m viztracer --ignore_c_function

    .. py:attribute:: log_print 
        :type: boolean
        :value: False

        Whether replace the ``print`` function to log in VizTracer report

        Setting it to ``True`` is equivalent to 

        .. code-block::

            python -m viztracer --log_print
    
    .. py:attribute:: output_file
        :type: string
        :value: "result.html"

        Default file path to write report

        Equivalent to 

        .. code-block::

            python -m viztracer -o <filepath>
    
    .. py:method:: run(command, output_file=None)

        run ``command`` and save report to ``output_file``
    
    .. py:method:: save(output_file=None, save_flamegraph=False)

        parse data and save report to ``output_file``. If ``output_file`` is ``None``, save to default path. If ``save_flamegraph`` is ``True``, save the flamegraph report as well
    
    .. py:method:: start()

        start tracing 

    .. py:method:: stop()

        start tracing 

    .. py:method:: clear()

        clear all the data

    .. py:method:: cleanup()

        clear all the data and free the memory allocated

    .. py:method:: parse()

        parse the data collected, return number of total entries

    .. py:method:: add_instant(name, args, scope="g")
        
        :param str name: name of this instant event
        :param object args: a jsonifiable object to log with the event
        :param str scope: one of ``g``, ``p`` or ``t`` for global, process or thread level event

        Add instant event to the report. 



