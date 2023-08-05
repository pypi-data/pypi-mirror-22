from __future__ import absolute_import
from __future__ import print_function

import functools

from veriloggen.dataflow import *
from veriloggen.seq.seq import make_condition
from veriloggen.fsm.fsm import FSM
from veriloggen.seq.seq import Seq
import veriloggen.dataflow.dtypes as dtypes

from . import compiler


class Stream(vtypes.VeriloggenNode):
    __intrinsics__ = ('run', 'join', 'done')

    def __init__(self, m, name, clk, rst, func):
        self.m = m
        self.name = name
        self.clk = clk
        self.rst = rst
        self.func = func

        self.df = DataflowManager(self.m, self.clk, self.rst)
        self.seq = Seq(self.m, 'name', self.clk, self.rst)
        self.start_cond = None
        self.done_flags = []

    def run(self, fsm, *args, **kwargs):
        self.start_cond = fsm.state == fsm.current
        self.func(self, *args)

        fsm.goto_next()

        return 0

    def join(self, fsm):
        done = None

        for flag in self.done_flags:
            done = make_condition(done, flag)

        fsm.If(done).goto_next()
        return 0

    def done(self, fsm):
        done = None

        for flag in self.done_flags:
            done = make_condition(done, flag)

        return done

    def read_sequential(self, obj, start_addr, size, point=0, signed=False,
                        port=0, with_last=False):
        flag = self.m.Reg(compiler._tmp_name('_'.join(['', self.name, 'flag'])),
                          initval=0)
        self.done_flags.append(flag)

        fsm = FSM(self.m, compiler._tmp_name('_'.join(['', self.name, 'fsm'])),
                  self.clk, self.rst)
        fsm.If(self.start_cond)(
            flag(0)
        )
        fsm.If(self.start_cond).goto_next()

        rdata, rlast, done = obj.read_dataflow(
            port, start_addr, size, cond=fsm, point=point, signed=signed)
        fsm.goto_next()

        fsm.If(done)(
            flag(1)
        )

        fsm.If(done).goto_init()

        if with_last:
            return rdata, rlast

        return rdata

    def write_sequential(self, obj, start_addr, size, value, when=None, port=0):
        flag = self.m.Reg(compiler._tmp_name('_'.join(['', self.name, 'flag'])),
                          initval=0)
        self.done_flags.append(flag)

        fsm = FSM(self.m, compiler._tmp_name('_'.join(['', self.name, 'fsm'])),
                  self.clk, self.rst)
        fsm.If(self.start_cond)(
            flag(0)
        )
        fsm.If(self.start_cond).goto_next()

        done = obj.write_dataflow(
            port, start_addr, value, size, cond=fsm, when=when)
        fsm.goto_next()

        fsm.If(done)(
            flag(1)
        )

        fsm.If(done).goto_init()

        return 0

    def __getattr__(self, attr):
        try:
            return object.__getattr__(self, attr)

        except AttributeError as e:
            if attr.startswith('__') or attr not in dir(dtypes):
                raise e

            func = getattr(dtypes, attr)

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                v = func(*args, **kwargs)
                if isinstance(v, (tuple, list)):
                    for item in v:
                        self._set_info(item)
                else:
                    self._set_info(v)
                return v

            return wrapper

    def _set_info(self, v):
        if isinstance(v, dtypes._Numeric):
            v._set_module(self.m)
            v._set_df(self.df)
            v._set_seq(self.seq)
