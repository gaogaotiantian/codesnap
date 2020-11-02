# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/viztracer/blob/master/NOTICE.txt

import unittest
import os
import sys
import subprocess
import time
import json
import shutil
import builtins
from viztracer.tracer import _VizTracer
from viztracer import VizTracer, ignore_function, trace_and_save, get_tracer


def fib(n):
    if n == 1 or n == 0:
        return 1
    return fib(n-1) + fib(n-2)


class TestTracerBasic(unittest.TestCase):
    def test_construct(self):
        def fib(n):
            if n == 1 or n == 0:
                return 1
            return fib(n-1) + fib(n-2)
        t = _VizTracer()
        t.start()
        fib(5)
        t.stop()
        entries = t.parse()
        self.assertEqual(entries, 15)
        t.generate_report()

    def test_builtin_func(self):
        import random
        def fun(n):
            for _ in range(n):
                random.randrange(n)
        t = _VizTracer(ignore_c_function=True)
        t.start()
        fun(10)
        t.stop()
        entries = t.parse()
        self.assertEqual(entries, 21)

    def test_cleanup(self):
        def fib(n):
            if n == 1 or n == 0:
                return 1
            return fib(n-1) + fib(n-2)
        t = _VizTracer()
        t.start()
        fib(5)
        t.stop()
        t.cleanup()
        entries = t.parse()
        self.assertEqual(entries, 0)


class TestVizTracerBasic(unittest.TestCase):
    def test_run(self):
        snap = VizTracer()
        snap.run("import random; random.randrange(10)", output_file="test_run.json")
        self.assertTrue(os.path.exists("test_run.json"))
        os.remove("test_run.json")

    def test_with(self):
        with VizTracer(output_file="test_with.json") as _:
            fib(10)
        self.assertTrue(os.path.exists("test_with.json"))
        os.remove("test_with.json")

    def test_tracer_entries(self):
        tracer = VizTracer(tracer_entries=10)
        tracer.start()
        fib(10)
        tracer.stop()
        entries = tracer.parse()
        self.assertEqual(entries, 10)

    def test_save(self):
        tracer = VizTracer(tracer_entries=10)
        tracer.start()
        fib(5)
        tracer.stop()
        tracer.parse()
        tracer.save("./tmp/result.html")
        self.assertTrue(os.path.exists("./tmp/result.html"))
        tracer.start()
        fib(5)
        tracer.save("./tmp/result2.json")
        self.assertTrue(os.path.exists("./tmp/result2.json"))
        self.assertTrue(tracer.enable)

        shutil.rmtree("./tmp")

    def test_save_flamegraph(self):
        tracer = VizTracer(tracer_entries=10)
        tracer.start()
        fib(5)
        tracer.stop()
        tracer.parse()
        tracer.save_flamegraph()
        self.assertTrue(os.path.exists("result_flamegraph.html"))
        os.remove("result_flamegraph.html")


class TestVizTracerOutput(unittest.TestCase):
    def test_json(self):
        t = _VizTracer()
        t.start()
        fib(10)
        t.stop()
        t.parse()
        t.generate_json()


class TestInstant(unittest.TestCase):
    def test_addinstant(self):
        tracer = VizTracer()
        tracer.start()
        tracer.add_instant("instant", {"karma": True})
        tracer.stop()
        entries = tracer.parse()
        self.assertEqual(entries, 1)

    def test_invalid_scope(self):
        tracer = VizTracer()
        tracer.start()
        tracer.add_instant("instant", {"karma": True}, scope="invalid")
        tracer.stop()
        entries = tracer.parse()
        self.assertEqual(entries, 0)


class TestFunctionArg(unittest.TestCase):
    def test_addfunctionarg(self):
        def f(tracer):
            tracer.add_functionarg("hello", "world")
        tracer = VizTracer()
        tracer.start()
        f(tracer)
        tracer.stop()
        tracer.parse()
        self.assertTrue("args" in tracer.data["traceEvents"][0] and
                        "hello" in tracer.data["traceEvents"][0]["args"])


class TestDecorator(unittest.TestCase):
    def test_pause_resume(self):
        @ignore_function
        def ignore(n):
            if n == 0:
                return 1
            return ignore(n-1) + 1
        tracer = VizTracer()
        tracer.start()
        ignore(10)
        tracer.stop()
        entries = tracer.parse()
        self.assertEqual(entries, 0)

    def test_trace_and_save(self):
        @trace_and_save(output_dir="./tmp")
        def my_function(n):
            fib(n)
        for _ in range(5):
            my_function(10)
        time.sleep(0.5)
        counter = len(os.listdir("./tmp"))
        shutil.rmtree("./tmp")
        self.assertEqual(counter, 5)

        if sys.platform in ["linux", "linux2", "darwin"]:
            # ls does not work on windows. Don't bother fixing it because it's just coverage test
            @trace_and_save
            def my_function2(n):
                fib(n)
            my_function2(10)
            time.sleep(0.5)
            a = subprocess.run(["ls result_my_function2*.json"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.assertEqual(a.returncode, 0)
            a = subprocess.run(["rm result_my_function2*.json"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.assertEqual(a.returncode, 0)


class TestLogPrint(unittest.TestCase):
    def test_log_print(self):
        tracer = VizTracer(log_print=True)
        tracer.start()
        print("hello")
        print("hello")
        print("hello")
        print("hello")
        tracer.stop()
        entries = tracer.parse()
        self.assertEqual(entries, 4)


class TestForkSave(unittest.TestCase):
    def test_basic(self):
        def fib(n):
            if n == 1 or n == 0:
                return 1
            return fib(n-1) + fib(n-2)
        t = VizTracer(verbose=0)
        for i in range(5, 10):
            t.start()
            fib(i)
            t.stop()
            t.parse()
            t.fork_save(output_file=str(i) + ".json")
        time.sleep(0.6)

        expected = {
            5: 15,
            6: 25,
            7: 41,
            8: 67,
            9: 109
        }
        pid = None
        for i in range(5, 10):
            path = str(i) + ".json"
            self.assertTrue(os.path.exists(path))
            with open(path) as f:
                data = json.load(f)
            os.remove(path)
            self.assertEqual(len(data["traceEvents"]), expected[i])
            if pid is None:
                pid = data["traceEvents"][0]["pid"]
            else:
                self.assertEqual(data["traceEvents"][0]["pid"], pid)

class TestGlobalTracer(unittest.TestCase):
    def test_get_tracer(self):
        with self.assertRaises(NameError):
            tmp = __viz_tracer__ # noqa: F821
        self.assertIs(get_tracer(), None)
        tracer = VizTracer
        builtins.__dict__["__viz_tracer__"] = tracer
        self.assertIs(get_tracer(), tracer)
        builtins.__dict__.pop("__viz_tracer__")