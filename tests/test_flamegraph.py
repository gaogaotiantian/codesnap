# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/viztracer/blob/master/NOTICE.txt

import json
from viztracer import FlameGraph
import os
from .base_tmpl import BaseTmpl


def depth(tree):
    if not tree.children:
        return 1
    return max([depth(n) for n in tree.children.values()]) + 1


class TestFlameGraph(BaseTmpl):
    def test_basic(self):
        with open(os.path.join(os.path.dirname(__file__), "data/multithread.json")) as f:
            sample_data = json.loads(f.read())
        fg = FlameGraph(sample_data)
        for tree in fg.trees.values():
            self.assertGreater(depth(tree.root), 1)
        ofile = "result_flamegraph.html"
        fg.save(ofile)
        self.assertTrue(os.path.exists(ofile))
        os.remove(ofile)

    def test_load(self):
        fg = FlameGraph()
        fg.load(os.path.join(os.path.dirname(__file__), "data/multithread.json"))
        for tree in fg.trees.values():
            self.assertGreater(depth(tree.root), 1)
        ofile = "result_flamegraph.html"
        fg.save(ofile)
        self.assertTrue(os.path.exists(ofile))
        os.remove(ofile)
        ofile = "result_flamegraph.html"
        fg.save(ofile)
        self.assertTrue(os.path.exists(ofile))
        os.remove(ofile)

    def test_dump_perfetto(self):
        with open(os.path.join(os.path.dirname(__file__), "data/multithread.json")) as f:
            sample_data = json.loads(f.read())
        fg = FlameGraph(sample_data)
        data = fg.dump_to_perfetto()
        self.assertEqual(len(data), 5)
        for callsite_info in data:
            self.assertIn("name", callsite_info)
            self.assertIn("flamegraph", callsite_info)
