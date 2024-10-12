class DummyLogger:
    """
    Creates A DummyLogger object which is just an object that does nothing
    """

    def __getattr__(self, name):
        """
        when any attribute on DummyLogger is accessed the dummy() function is called which does nothing

        :param name: The name of the attribute being accessed
        :return: dummy function
        """

        def dummy(*args, **kwargs):
            pass

        return dummy
