class Tests():
    def ___init__(self):
        pass

class Frontend(Tests):
    
    def test_index(self):
        raise NotImplementedError

    def test_temp(self):
        raise NotImplementedError

    def test_home(self):
        raise NotImplementedError

    def test_about(self):
        raise NotImplementedError

    def test_login(self):
        raise NotImplementedError

    def test_register(self):
        raise NotImplementedError

class Backend(Tests):
    def __init__(self):
        #test_table = Account()
        pass
    def test_insert(self):
        raise NotImplementedError

    def test_update(self):
        raise NotImplementedError

    def test_retrieve(self):
        raise NotImplementedError

    def test_delete(self):
        raise NotImplementedError