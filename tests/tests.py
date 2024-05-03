from afb_test import AFBTestCase, configure_afb_binding_tests, run_afb_binding_tests

import libafb

bindings = {"helloworld": f"libhelloworld-binding.so"}

def setUpModule():
    configure_afb_binding_tests(bindings=bindings)

class TestHelloWorld(AFBTestCase):

    def test_hello_verb(self):
        """Test hello verb"""
        with self.assertRaises(RuntimeError):
            r = libafb.callsync(self.binder, "helloworld", "hello", None)

        r = libafb.callsync(self.binder, "helloworld", "hello")
        assert r.args == ("Hello world!",)

        r = libafb.callsync(self.binder, "helloworld", "hello", "you")
        assert r.args == ('Hello "you"!',)

        r = libafb.callsync(self.binder, "helloworld", "hello", 42)
        assert r.args == ("Hello 42!",)

        r = libafb.callsync(self.binder, "helloworld", "hello", 42, 43)
        assert r.args == ("Hello 42!",)

        r = libafb.callsync(self.binder, "helloworld", "hello", {"ok": 1})
        assert r.args == ('Hello {"ok":1}!',)

        r = libafb.callsync(self.binder, "helloworld", "hello", 3.14)
        assert r.args == ("Hello 3.1400000000000001!",)

        r = libafb.callsync(self.binder, "helloworld", "hello", [1, 2, 3])
        assert r.args == ("Hello [1,2,3]!",)


    def test_hello_evt(self):
        """Test hello event"""
        with self.assertEventEmitted("helloworld", "verb_called"):
            libafb.callsync(self.binder, "helloworld", "hello")

    def test_sum_verb(self):
        """Test sum verb"""
        for arg, expected_sum in [
            ([1, 2, 3, 4], 10),
            ([0, -10], -10),
            ([2**40], 2**40),
            ([2**63 - 1], 2**63 - 1),
            ([], 0),
        ]:
            r = libafb.callsync(self.binder, "helloworld", "sum", arg)
            assert r.args == (expected_sum,)

        # check integer limits
        with self.assertRaises(ValueError):
            libafb.callsync(self.binder, "helloworld", "sum", [2**64])

        # check no argument raises an error
        with self.assertRaises(RuntimeError):
            libafb.callsync(self.binder, "helloworld", "sum")

        # check argument of the wrong type raises
        with self.assertRaises(RuntimeError):
            libafb.callsync(self.binder, "helloworld", "sum", 42)

    def test_sum_evt(self):
        """Test sum event"""
        with self.assertEventEmitted("helloworld", "verb_called"):
            libafb.callsync(self.binder, "helloworld", "sum", [42])

if __name__ == "__main__":
    run_afb_binding_tests(bindings)
