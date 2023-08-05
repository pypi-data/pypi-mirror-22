log-Init
========

1. install
----------

.. code-block:: sh

        pip install --user loginit==<version>

2. upgrade
----------

.. code-block:: sh

        pip install --user -U loginit==<version>   # upgrade

3. uninstall
------------

.. code-block:: sh

        pip uninstall --user loginit

4. How to use
---------------


.. code-block:: python

        #!/usr/bin/env python

        from loginit import init_logger
        import  logging

        if __name__ == "__main__":
            import platform
            if platform.system() == "Windows":
                init_logger("C:\\Users\\JXM\Desktop\\test.log")
            elif platform.system() == "Linux":
                init_logger("/tmp/test.log")
            else: 
                init_logger()

            logging.info("this is info test !!!")
            logging.debug("this is debug test !!!")
            logging.warning("this is warning test !!!")
            logging.error("this is error test !!!")
            logging.critical("this is critical test !!!")
            try:
                raise Exception("this exception test !!!")
            except Exception as e:
                logging.exception(e)


