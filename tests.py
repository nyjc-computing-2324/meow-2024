class Tests():
    def ___init__(self):
        pass

class Frontend(Tests):
    
    def test_index(self):
        pass

    def test_temp(self):
        pass

    def test_home(self):
        pass

    def test_about(self):
        pass

    def test_login(self):
        pass

    def test_register(self):
        pass

class Backend(Tests):
    def __init__(self):
        raise NotImplementedError

    def test_insert(self):
        raise NotImplementedError

    def test_update(self):
        raise NotImplementedError

    def test_retrieve(self):
        raise NotImplementedError

    def test_delete(self):
        raise NotImplementedError