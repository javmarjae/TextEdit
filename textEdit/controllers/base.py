class Controller:
    """
    Base controller class.
    """

    def __init__(self, app):
        """
        Constructor

        :param app: Reference to app instance.
        """
        self.app = app