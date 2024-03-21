class Tests():
    def ___init__(self):
        pass

class Frontend(Tests):
    
    def test_index():
        pass

    def test_temp():
        pass

    def test_home():
        pass

    def test_about():
        pass

    def test_login():
        pass

    def test_register():
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