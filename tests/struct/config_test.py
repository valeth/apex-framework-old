from apex.struct.config import Config

def test_creation():
    conf = Config({"one": 1, "two": 2})
    assert conf.one == 1
    assert conf.two == 2

def test_nesting():
    conf = Config({
        "one": 1,
        "dic": {"two": 2, "three": 3}
    })
    assert conf.one == 1
    assert isinstance(conf.dic, Config)
    assert conf.dic.two == 2
    assert conf.dic.three == 3

def test_array():
    conf = Config({
        "one": 1,
        "ary": [1, 2, 3],
        "ary2": [
            {"ichi": "one", "ni": "two"},
            {"first": True, "last": False}
        ]
    })
    assert conf.one == 1
    assert conf.ary == [1, 2, 3]
    assert isinstance(conf.ary2, list)
    assert len(conf.ary2) == 2
    assert isinstance(conf.ary2[0], Config)
    assert isinstance(conf.ary2[1], Config)
