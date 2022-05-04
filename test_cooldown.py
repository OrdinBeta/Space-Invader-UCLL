from cooldown import Cooldown


def test_cooldown1():
    c = Cooldown(0.5)
    assert not c.ready
    c.update(0.1)
    assert not c.ready
    c.update(0.2)
    assert not c.ready
    c.update(0.21)
    assert c.ready
    c.reset()
    assert not c.ready

def test_cooldown2():
    c = Cooldown(1)
    assert not c.ready
    c.update(1.1)
    assert c.ready
    c.reset()
    assert not c.ready
    c.update(1.1)
    assert c.ready