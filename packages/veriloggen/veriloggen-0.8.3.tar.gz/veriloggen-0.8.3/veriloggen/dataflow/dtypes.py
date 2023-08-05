from __future__ import absolute_import
from __future__ import print_function

from functools import partial
from collections import OrderedDict
from math import log
import veriloggen.core.vtypes as vtypes
import veriloggen.types.fixed as fx
import veriloggen.types.rom as rom
from veriloggen.seq.seq import make_condition as _make_condition
from . import mul
from . import div


# Object ID counter for object sorting key
_object_counter = 0


#-------------------------------------------------------------------------
def Constant(value, fixed=True, point=0):
    if isinstance(value, int):
        return Int(value)

    if isinstance(value, bool):
        v = 1 if value else 0
        return Int(v)

    if isinstance(value, float):
        if fixed:
            value = fx.to_fixed(value, point)
            return FixedPoint(value, point)
        return Float(value)

    if isinstance(value, str):
        return Str(value)

    raise TypeError("Unsupported type for Constant '%s'" % str(type(value)))


#-------------------------------------------------------------------------
def Variable(data=None, valid=None, ready=None, width=32, point=0, signed=False):
    return _Variable(data, valid, ready, width, point, signed)


#-------------------------------------------------------------------------
def Parameter(name, value, width=32, point=0, signed=False):
    """ parameter with an immediate value """
    if not isinstance(name, str):
        raise TypeError("'name' must be str, not '%s'" % str(tyep(name)))
    return _ParameterVariable(name, width, point, signed, value=value)


def ParameterVariable(data, width=32, point=0, signed=False):
    """ parameter with an existing object """
    if isinstance(data, float):
        return Constant(data, point=point)
    if isinstance(data, (int, bool)):
        data = vtypes.Int(data, width=width)
    return _ParameterVariable(data, width, point, signed)


#-------------------------------------------------------------------------
class _Node(object):

    def __init__(self):
        global _object_counter
        self.object_id = _object_counter
        _object_counter += 1

    def __hash__(self):
        object_id = self.object_id if hasattr(self, 'object_id') else None
        return hash((id(self), object_id))

    def __eq__(self, other):
        return (id(self), self.object_id) == (id(other), other.object_id)


#-------------------------------------------------------------------------
class _Numeric(_Node):
    latency = 0

    def __hash__(self):
        object_id = self.object_id if hasattr(self, 'object_id') else None
        return hash((id(self), object_id))

    def __init__(self):
        _Node.__init__(self)

        # set up by _set_managers()
        self.m = None
        self.df = None
        self.seq = None

        self.output_data = None
        self.output_valid = None
        self.output_ready = None

        self.output_sig_data = None
        self.output_sig_valid = None
        self.output_sig_ready = None

        self.output_node = None

        self.sig_data = None
        self.sig_valid = None
        self.sig_ready = None

        self.start_stage = None
        self.end_stage = None
        self.sink = []

        # set up by _set_attributes()
        self.width = None
        self.point = None
        self.signed = False

        # stage numbers incremented
        self.delayed_value = OrderedDict()

        # stage numbers NOT incremented
        self.previous_value = OrderedDict()

    def output(self, data, valid=None, ready=None):
        if self.output_data is not None:
            raise ValueError('output_data is already assigned.')
        self.output_data = data
        self.output_valid = valid
        self.output_ready = ready

        if self.df is not None:
            self.df.add(self)

    def output_tmp(self):
        if self.m is None:
            raise ValueError("Module information is not set.")

        tmp = self.m.get_tmp()
        self.output(_tmp_data(tmp), _tmp_valid(tmp), _tmp_ready(tmp))

    def prev(self, index):
        if index < 0:
            raise ValueError("index must be greater than 0")

        prev = self
        for i in range(index):
            r = self._get_previous_value(i + 1)
            if r is not None:
                prev = r
                continue
            r = _Prev(prev)
            r._set_parent_value(self)
            self._add_previous_value(i + 1, r)
            prev = r

        return prev

    #-------------------------------------------------------------------------
    def write(self, wdata, cond=None):
        raise TypeError("Unsupported method.")

    def read(self, cond=None):
        if self.output_node is not None and id(self) != id(self.output_node):
            return self.output_node.read(cond)

        if self.output_sig_data is None:

            # set default name
            if self.output_data is None:
                self.output_tmp()

            self._implement_output_sig(self.m, self.seq, aswire=True)

        data = self.output_sig_data
        valid = self.output_sig_valid

        if valid is None:
            valid = 1

        ready = make_condition(cond)
        val = 1 if ready is None else ready

        if ready is not None and self.output_sig_ready is None:
            raise ValueError("Dataflow ready port is required for throttling.")

        if self.output_sig_ready is not None:
            prev_assign = self.output_sig_ready._get_assign()
            if not prev_assign:
                self.output_sig_ready.assign(val)
            else:
                prev_assign.overwrite_right(
                    vtypes.OrList(prev_assign.statement.right, val))
                m = self.output_sig_ready._get_module()
                m.remove(prev_assign)
                m.append(prev_assign)

        if ready is not None:
            ack = vtypes.AndList(valid, ready)
        else:
            ack = valid

        rdata = data
        rvalid = ack

        return rdata, rvalid

    #--------------------------------------------------------------------------
    def get_signed(self):
        return self.signed

    def get_point(self):
        return self.point

    def bit_length(self):
        return self.width

    def eval(self):
        raise NotImplementedError('eval() is not implemented')

    #--------------------------------------------------------------------------
    def _set_attributes(self):
        raise NotImplementedError('_set_attributes() is not implemented')

    def _set_managers(self):
        raise NotImplementedError('_set_managers() is not implemented')

    def _set_module(self, m):
        self.m = m

    def _set_df(self, df):
        self.df = df

    def _set_seq(self, seq):
        self.seq = seq

    #--------------------------------------------------------------------------
    def _implement(self, m, seq):
        raise NotImplementedError('_implement() is not implemented.')

    def _implement_input(self, m, seq, aswire=False):
        raise NotImplementedError('_implement_input() is not implemented.')

    def _implement_output(self, m, seq, aswire=False):
        if self.end_stage is None:
            self.end_stage = 0

        self._implement_output_sig(m, seq, aswire)
        data = self.output_sig_data
        valid = self.output_sig_valid
        ready = self.output_sig_ready

        m.Assign(data(self.sig_data))

        if self.output_valid is not None:
            m.Assign(valid(self.sig_valid))

        if self.output_ready is not None:
            _connect_ready(m, self.sig_ready, ready)
        elif self.sig_ready is not None:
            _connect_ready(m, self.sig_ready, 1)

    def _implement_output_sig(self, m, seq, aswire=False):
        if self.output_sig_data is not None:
            return

        if self.m is None:
            raise ValueError("Module information is not set.")

        width = self.bit_length()
        signed = self.get_signed()

        type_i = m.Wire if aswire else m.Input
        type_o = m.Wire if aswire else m.Output

        if isinstance(self.output_data, (vtypes.Wire, vtypes.Output)):
            data = self.output_data
            self.output_sig_data = data
        else:
            data = type_o(self.output_data, width=width, signed=signed)
            self.output_sig_data = data

        if isinstance(self.output_valid, (vtypes.Wire, vtypes.Output)):
            valid = self.output_valid
            self.output_sig_valid = valid
        elif self.output_valid is not None:
            valid = type_o(self.output_valid)
            self.output_sig_valid = valid

        if isinstance(self.output_ready, (vtypes._Numeric, int, bool)):
            ready = self.output_ready
            self.output_sig_ready = ready
        elif self.output_ready is not None:
            ready = type_i(self.output_ready)
            self.output_sig_ready = ready

    #--------------------------------------------------------------------------
    def _has_output(self):
        if self.output_data is not None:
            return True
        return False

    def _disable_output(self):
        self.output_data = None
        self.output_valid = None
        self.output_ready = None

    def _disable_output_sig(self):
        self.output_sig_data = None
        self.output_sig_valid = None
        self.output_sig_ready = None

    def _set_output_node(self, node):
        self.output_node = node

    def _set_start_stage(self, stage):
        self.start_stage = stage

    def _get_start_stage(self):
        return self.start_stage

    def _has_start_stage(self):
        if self.start_stage is None:
            return False
        return True

    def _set_end_stage(self, stage):
        self.end_stage = stage

    def _get_end_stage(self):
        return self.end_stage

    def _has_end_stage(self):
        if self.end_stage is None:
            return False
        return True

    def _add_sink(self, value):
        self.sink.append(value)

    def _add_delayed_value(self, delay, value):
        if delay in self.delayed_value:
            raise ValueError('%d-delayed value is already allocated.' % delay)
        self.delayed_value[delay] = value

    def _get_delayed_value(self, delay):
        if delay not in self.delayed_value:
            return None
        return self.delayed_value[delay]

    def _add_previous_value(self, delay, value):
        if delay in self.delayed_value:
            raise ValueError('%d-delayed value is already allocated.' % delay)
        self.previous_value[delay] = value

    def _get_previous_value(self, delay):
        if delay not in self.previous_value:
            return None
        return self.previous_value[delay]

    #--------------------------------------------------------------------------
    def __lt__(self, r):
        return LessThan(self, r)

    def __le__(self, r):
        return LessEq(self, r)

    def __eq__(self, r):
        return Eq(self, r)

    def __ne__(self, r):
        return NotEq(self, r)

    def __ge__(self, r):
        return GreaterEq(self, r)

    def __gt__(self, r):
        return GreaterThan(self, r)

    def __add__(self, r):
        return Plus(self, r)

    def __sub__(self, r):
        return Minus(self, r)

    def __pow__(self, r):
        return Power(self, r)

    def __mul__(self, r):
        return Times(self, r)

    def __div__(self, r):
        return Divide(self, r)

    def __truediv__(self, r):
        return Divide(self, r)

    def __mod__(self, r):
        return Mod(self, r)

    def __and__(self, r):
        return And(self, r)

    def __or__(self, r):
        return Or(self, r)

    def __xor__(self, r):
        return Xor(self, r)

    def __lshift__(self, r):
        return Sll(self, r)

    def __rshift__(self, r):
        return Srl(self, r)

    def __neg__(self):
        return Uminus(self)

    def __pos__(self):
        return Uplus(self)

    def __getitem__(self, r):
        if isinstance(r, slice):
            size = self.bit_length()

            right = r.start
            if right is None:
                right = 0
            elif isinstance(right, int) and right < 0:
                right = size - abs(right)

            left = r.stop
            if left is None:
                left = size
            elif isinstance(left, int) and left < 0:
                left = size - abs(left)
            left -= 1

            if isinstance(left, int) and left < 0:
                raise ValueError("Illegal slice index: left = %d" % left)

            step = r.step
            if step is None:
                return Slice(self, left, right)
            else:
                if not (isinstance(left, int) and
                        isinstance(right, int) and
                        isinstance(step, int)):
                    raise ValueError(
                        "Slice with step is not supported in Verilog Slice.")

                if step == 0:
                    raise ValueError("Illegal slice step: step = %d" % step)

                values = [Pointer(self, i)
                          for i in range(right, left + 1, step)]
                values.reverse()
                return Cat(*values)

        if isinstance(r, int) and r < 0:
            r = self.bit_length() - abs(r)

        return Pointer(self, r)

    def sra(self, r):  # shift right arithmetically
        return Sra(self, r)

    def repeat(self, times):
        return Repeat(self, times)

    def slice(self, msb, lsb):
        return Slice(self, msb, lsb)

    def __iter__(self):
        self.iter_size = len(self)
        self.iter_count = 0
        return self

    def __next__(self):
        if self.iter_count >= self.iter_size:
            raise StopIteration()

        ret = Pointer(self, self.iter_count)
        self.iter_count += 1
        return ret

    # for Python2
    def next(self):
        return self.__next__()

    def __len__(self):
        ret = self.bit_length()
        if not isinstance(ret, int):
            raise ValueError("Non int length.")
        return ret

    @property
    def raw_data(self):
        if self.sig_data is None:
            raise ValueError(
                "Dataflow is not synthesized yet. Run Dataflow.implement().")
        return self.sig_data

    @property
    def raw_valid(self):
        if self.sig_data is None:
            raise ValueError(
                "Dataflow is not synthesized yet. Run Dataflow.implement().")
        if self.sig_valid is None:
            return 1
        return self.sig_valid

    @property
    def raw_ready(self):
        if self.sig_data is None:
            raise ValueError(
                "Dataflow is not synthesized yet. Run Dataflow.implement().")
        return self.sig_ready

    @property
    def data(self):
        if self.output_node is not None:
            return self.output_node.output_sig_data
        return self.raw_data

    @property
    def valid(self):
        if self.output_node is not None:
            return self.output_node.output_sig_valid
        return self.raw_valid

    @property
    def ready(self):
        if self.output_node is not None:
            return self.output_node.output_sig_ready
        return self.raw_ready


#-------------------------------------------------------------------------
class _Operator(_Numeric):
    latency = 1

    def _implement(self, m, seq):
        raise NotImplementedError('_implement() is not implemented.')


class _BinaryOperator(_Operator):

    def __init__(self, left, right):
        _Operator.__init__(self)
        self.left = _to_constant(left)
        self.right = _to_constant(right)
        self.left._add_sink(self)
        self.right._add_sink(self)
        self.op = getattr(vtypes, self.__class__.__name__, None)
        self._set_attributes()
        self._set_managers()

    def _set_attributes(self):
        left_fp = self.left.get_point()
        right_fp = self.right.get_point()
        left = self.left.bit_length() - left_fp
        right = self.right.bit_length() - right_fp
        self.width = max(left, right) + max(left_fp, right_fp)
        self.point = max(left_fp, right_fp)
        self.signed = self.left.get_signed() and self.right.get_signed()

    def _set_managers(self):
        self._set_df(_get_df(self.left, self.right))
        self._set_module(getattr(self.df, 'module', None))
        self._set_seq(getattr(self.df, 'seq', None))

    def _implement(self, m, seq):
        if self.latency != 1:
            raise ValueError("Latency mismatch '%d' vs '%s'" %
                             (self.latency, 1))

        width = self.bit_length()
        signed = self.get_signed()

        tmp = m.get_tmp()
        data = m.Reg(_tmp_data(tmp), width, initval=0, signed=signed)
        valid = m.Reg(_tmp_valid(tmp), initval=0)
        ready = m.Wire(_tmp_ready(tmp))
        self.sig_data = data
        self.sig_valid = valid
        self.sig_ready = ready

        lpoint = self.left.get_point()
        rpoint = self.right.get_point()

        ldata, rdata = fx.adjust(
            self.left.sig_data, self.right.sig_data, lpoint, rpoint, signed)

        lvalid = self.left.sig_valid
        rvalid = self.right.sig_valid

        lready = self.left.sig_ready
        rready = self.right.sig_ready

        all_valid = _and_vars(lvalid, rvalid)
        all_ready = _and_vars(lready, rready)

        accept = vtypes.OrList(ready, vtypes.Not(valid))

        valid_cond = _and_vars(accept, all_ready)
        valid_reset_cond = _and_vars(valid, ready)
        data_cond = _and_vars(valid_cond, all_valid)
        ready_cond = _and_vars(accept, all_valid)

        seq(data(self.op(ldata, rdata)), cond=data_cond)
        seq(valid(0), cond=valid_reset_cond)
        seq(valid(all_valid), cond=valid_cond)
        _connect_ready(m, lready, ready_cond)
        _connect_ready(m, rready, ready_cond)

        if not self._has_output():
            _connect_ready(m, ready, vtypes.Int(1))


class _UnaryOperator(_Operator):

    def __init__(self, right):
        _Operator.__init__(self)
        self.right = _to_constant(right)
        self.right._add_sink(self)
        self.op = getattr(vtypes, self.__class__.__name__, None)
        self._set_attributes()
        self._set_managers()

    def _set_attributes(self):
        right = self.right.bit_length()
        right_fp = self.right.get_point()
        self.width = right
        self.point = right_fp
        self.signed = self.right.get_signed()

    def _set_managers(self):
        self._set_df(_get_df(self.right))
        self._set_module(getattr(self.df, 'module', None))
        self._set_seq(getattr(self.df, 'seq', None))

    def _implement(self, m, seq):
        if self.latency != 1:
            raise ValueError("Latency mismatch '%d' vs '%s'" %
                             (self.latency, 1))

        width = self.bit_length()
        signed = self.get_signed()

        tmp = m.get_tmp()
        data = m.Reg(_tmp_data(tmp), width, initval=0, signed=signed)
        valid = m.Reg(_tmp_valid(tmp), initval=0)
        ready = m.Wire(_tmp_ready(tmp))
        self.sig_data = data
        self.sig_valid = valid
        self.sig_ready = ready

        rdata = self.right.sig_data

        rvalid = self.right.sig_valid

        rready = self.right.sig_ready

        all_valid = _and_vars(rvalid)
        all_ready = _and_vars(rready)

        accept = vtypes.OrList(ready, vtypes.Not(valid))

        valid_cond = _and_vars(accept, all_ready)
        valid_reset_cond = _and_vars(valid, ready)
        data_cond = _and_vars(valid_cond, all_valid)
        ready_cond = _and_vars(accept, all_valid)

        seq(data(self.op(rdata)), cond=data_cond)
        seq(valid(0), cond=valid_reset_cond)
        seq(valid(all_valid), cond=valid_cond)
        _connect_ready(m, rready, ready_cond)

        if not self._has_output():
            _connect_ready(m, ready, vtypes.Int(1))


class Power(_BinaryOperator):
    latency = 0

    def eval(self):
        return self.left.eval() ** self.right.eval()

    def _implement(self, m, seq):
        raise NotImplementedError('_implement() is not implemented.')


class Times(_BinaryOperator):
    latency = 6 + 1

    def eval(self):
        return self.left.eval() * self.right.eval()

    def _set_attributes(self):
        left_fp = self.left.get_point()
        right_fp = self.right.get_point()
        left = self.left.bit_length()
        right = self.right.bit_length()
        self.width = max(left, right)
        self.point = max(left_fp, right_fp)
        self.signed = self.left.get_signed() and self.right.get_signed()

    def _implement(self, m, seq):
        if self.latency <= 3:
            raise ValueError("Latency of '*' operator must be greater than 3")

        width = self.bit_length()
        signed = self.get_signed()

        tmp = m.get_tmp()
        data = m.Wire(_tmp_data(tmp), width, signed=signed)
        valid = m.Wire(_tmp_valid(tmp))
        ready = m.Wire(_tmp_ready(tmp))
        self.sig_data = data
        self.sig_valid = valid
        self.sig_ready = ready

        lwidth = self.left.bit_length()
        rwidth = self.right.bit_length()

        lpoint = self.left.get_point()
        rpoint = self.right.get_point()

        lsigned = self.left.get_signed()
        rsigned = self.right.get_signed()

        ldata = self.left.sig_data
        rdata = self.right.sig_data

        accept = vtypes.OrList(ready, vtypes.Not(valid))

        odata = m.Wire(_tmp_data(tmp, prefix='_tmp_odata_'),
                       lwidth + rwidth, signed=signed)
        data_reg = m.Reg(_tmp_data(tmp, prefix='_tmp_data_reg_'), lwidth + rwidth,
                         signed=signed, initval=0)

        shift_size = min(lpoint, rpoint)
        if shift_size > 0:
            seq(data_reg(fx.shift_right(odata, shift_size, signed=signed)), cond=accept)
        else:
            seq(data_reg(odata), cond=accept)

        m.Assign(data(data_reg))

        ovalid = m.Wire(_tmp_valid(tmp, prefix='_tmp_ovalid_'))
        valid_reg = m.Reg(_tmp_valid(tmp, prefix='_tmp_valid_reg_'), initval=0)

        seq(valid_reg(ovalid), cond=accept)
        m.Assign(valid(valid_reg))

        lvalid = self.left.sig_valid
        rvalid = self.right.sig_valid

        lready = self.left.sig_ready
        rready = self.right.sig_ready

        all_valid = _and_vars(lvalid, rvalid)
        all_ready = _and_vars(lready, rready)

        valid_cond = _and_vars(accept, all_ready)
        valid_reset_cond = _and_vars(valid, ready)
        data_cond = _and_vars(valid_cond, all_valid)
        ready_cond = _and_vars(accept, all_valid)

        depth = self.latency - 1

        inst = mul.get_mul(lwidth, rwidth, lsigned, rsigned, depth)
        clk = m._clock
        rst = m._reset

        enable = m.Wire(_tmp_data(tmp, prefix='_tmp_enable_'))
        update = m.Wire(_tmp_data(tmp, prefix='_tmp_update_'))

        m.Assign(enable(data_cond))
        m.Assign(update(accept))  # NOT valid_cond

        ports = [('CLK', clk), ('RST', rst),
                 ('update', update), ('enable', enable), ('valid', ovalid),
                 ('a', ldata), ('b', rdata), ('c', odata)]

        m.Instance(inst, ''.join(['mul', str(tmp)]), ports=ports)

        _connect_ready(m, lready, ready_cond)
        _connect_ready(m, rready, ready_cond)

        if not self._has_output():
            _connect_ready(m, ready, vtypes.Int(1))


class Divide(_BinaryOperator):
    latency = 32 + 3
    variable_latency = 'bit_length'

    def eval(self):
        left = self.left.eval()
        right = self.right.eval()
        if isinstance(left, int) and isinstance(right, int):
            return int(left / right)
        return Divide(left, right)

    def _implement(self, m, seq):
        if self.latency <= 3:
            raise ValueError("Latency of '*' operator must be greater than 3")

        width = self.bit_length()
        signed = self.get_signed()

        tmp = m.get_tmp()
        data = m.Wire(_tmp_data(tmp), width, signed=signed)
        valid = m.Wire(_tmp_valid(tmp))
        ready = m.Wire(_tmp_ready(tmp))
        self.sig_data = data
        self.sig_valid = valid
        self.sig_ready = ready

        lpoint = self.left.get_point()
        rpoint = self.right.get_point()

        lsigned = self.left.get_signed()
        rsigned = self.right.get_signed()

        ldata = m.Reg(_tmp_data(tmp, prefix='_tmp_ldata_'),
                      width, signed=lsigned, initval=0)
        rdata = m.Reg(_tmp_data(tmp, prefix='_tmp_rdata_'),
                      width, signed=rsigned, initval=0)

        point = max(lpoint, rpoint)

        if lpoint <= rpoint:
            lval, rval = fx.adjust(
                self.left.sig_data, self.right.sig_data, lpoint, rpoint, signed)
            shift_size = point
        else:
            lval = self.left.sig_data
            rval = self.right.sig_data
            shift_size = point - (lpoint - rpoint)

        accept = vtypes.OrList(ready, vtypes.Not(valid))

        seq(ldata(lval), cond=accept)
        seq(rdata(rval), cond=accept)

        sign = vtypes.Not(vtypes.OrList(vtypes.AndList(ldata[width - 1] == 0, rdata[width - 1] == 0),  # + , +
                                        vtypes.AndList(ldata[width - 1] == 1, rdata[width - 1] == 1)))  # - , -

        abs_ldata = m.Reg(
            _tmp_data(tmp, prefix='_tmp_abs_ldata_'), width, initval=0)
        abs_rdata = m.Reg(
            _tmp_data(tmp, prefix='_tmp_abs_rdata_'), width, initval=0)

        if not lsigned:
            seq(abs_ldata(ldata), cond=accept)
        else:
            seq(abs_ldata(vtypes.Mux(ldata[width - 1] == 0, ldata, vtypes.Unot(ldata) + 1)),
                cond=accept)

        if not rsigned:
            seq(abs_rdata(rdata), cond=accept)
        else:
            seq(abs_rdata(vtypes.Mux(rdata[width - 1] == 0, rdata, vtypes.Unot(rdata) + 1)),
                cond=accept)

        osign = m.Wire(_tmp_data(tmp, prefix='_tmp_osign_'))
        abs_odata = m.Wire(
            _tmp_data(tmp, prefix='_tmp_abs_odata_'), width, signed=signed)

        if shift_size > 0:
            shifted_abs_odata = vtypes.Sll(abs_odata, shift_size)
        else:
            shifted_abs_odata = abs_odata

        odata = m.Reg(_tmp_data(tmp, prefix='_tmp_odata_'),
                      width, signed=signed, initval=0)

        if not signed:
            seq(odata(shifted_abs_odata), cond=accept)
        else:
            seq(odata(vtypes.Mux(osign == 0, shifted_abs_odata, vtypes.Unot(shifted_abs_odata) + 1)),
                cond=accept)

        m.Assign(data(odata))

        ovalid = m.Wire(_tmp_valid(tmp, prefix='_tmp_ovalid_'))

        v = ovalid
        for i in range(3):
            nv = m.Reg(_tmp_valid(
                tmp, prefix='_tmp_valid_reg' + str(i) + '_'), initval=0)
            seq(nv(v), cond=accept)
            v = nv
        m.Assign(valid(v))

        s = sign
        for i in range(self.latency):
            ns = m.Reg(_tmp_data(tmp, prefix='_tmp_sign' +
                                 str(i) + '_'), initval=0)
            seq(ns(s), cond=accept)
            s = ns
        m.Assign(osign(s))

        lvalid = self.left.sig_valid
        rvalid = self.right.sig_valid

        lready = self.left.sig_ready
        rready = self.right.sig_ready

        all_valid = _and_vars(lvalid, rvalid)
        all_ready = _and_vars(lready, rready)

        valid_cond = _and_vars(accept, all_ready)
        valid_reset_cond = _and_vars(valid, ready)
        data_cond = _and_vars(valid_cond, all_valid)
        ready_cond = _and_vars(accept, all_valid)

        inst = div.get_div()
        clk = m._clock
        rst = m._reset

        enable = m.Wire(_tmp_data(tmp, prefix='_tmp_enable_'))
        update = m.Wire(_tmp_data(tmp, prefix='_tmp_update_'))
        m.Assign(enable(data_cond))
        m.Assign(update(accept))  # NOT valid_cond

        params = [('W_D', width)]
        ports = [('CLK', clk), ('RST', rst),
                 ('update', update), ('enable', enable), ('valid', ovalid),
                 ('in_a', abs_ldata), ('in_b', abs_rdata), ('rslt', abs_odata)]

        m.Instance(inst, ''.join(['div', str(tmp)]), params, ports)

        _connect_ready(m, lready, ready_cond)
        _connect_ready(m, rready, ready_cond)

        if not self._has_output():
            _connect_ready(m, ready, vtypes.Int(1))


class Mod(_BinaryOperator):
    latency = 32 + 3
    variable_latency = 'bit_length'

    def eval(self):
        return self.left.eval() % self.right.eval()

    def _implement(self, m, seq):
        if self.latency <= 3:
            raise ValueError("Latency of '*' operator must be greater than 3")

        width = self.bit_length()
        signed = self.get_signed()

        tmp = m.get_tmp()
        data = m.Wire(_tmp_data(tmp), width, signed=signed)
        valid = m.Wire(_tmp_valid(tmp))
        ready = m.Wire(_tmp_ready(tmp))
        self.sig_data = data
        self.sig_valid = valid
        self.sig_ready = ready

        lpoint = self.left.get_point()
        rpoint = self.right.get_point()

        lsigned = self.left.get_signed()
        rsigned = self.right.get_signed()

        ldata = m.Reg(_tmp_data(tmp, prefix='_tmp_ldata_'),
                      width, signed=lsigned, initval=0)
        rdata = m.Reg(_tmp_data(tmp, prefix='_tmp_rdata_'),
                      width, signed=rsigned, initval=0)

        point = max(lpoint, rpoint)

        if lpoint <= rpoint:
            lval, rval = fx.adjust(
                self.left.sig_data, self.right.sig_data, lpoint, rpoint, signed)
            shift_size = point
        else:
            lval = self.left.sig_data
            rval = self.right.sig_data
            shift_size = point - (lpoint - rpoint)

        accept = vtypes.OrList(ready, vtypes.Not(valid))

        seq(ldata(lval), cond=accept)
        seq(rdata(rval), cond=accept)

        sign = vtypes.Not(vtypes.OrList(vtypes.AndList(ldata[width - 1] == 0, rdata[width - 1] == 0),  # + , +
                                        vtypes.AndList(ldata[width - 1] == 1, rdata[width - 1] == 1)))  # - , -

        abs_ldata = m.Reg(
            _tmp_data(tmp, prefix='_tmp_abs_ldata_'), width, initval=0)
        abs_rdata = m.Reg(
            _tmp_data(tmp, prefix='_tmp_abs_rdata_'), width, initval=0)

        if not lsigned:
            seq(abs_ldata(ldata), cond=accept)
        else:
            seq(abs_ldata(vtypes.Mux(ldata[width - 1] == 0, ldata, vtypes.Unot(ldata) + 1)),
                cond=accept)

        if not rsigned:
            seq(abs_rdata(rdata), cond=accept)
        else:
            seq(abs_rdata(vtypes.Mux(rdata[width - 1] == 0, rdata, vtypes.Unot(rdata) + 1)),
                cond=accept)

        osign = m.Wire(_tmp_data(tmp, prefix='_tmp_osign_'))
        abs_odata = m.Wire(
            _tmp_data(tmp, prefix='_tmp_abs_odata_'), width, signed=signed)

        if shift_size > 0:
            shifted_abs_odata = vtypes.Sll(abs_odata, shift_size)
        else:
            shifted_abs_odata = abs_odata

        odata = m.Reg(_tmp_data(tmp, prefix='_tmp_odata_'),
                      width, signed=signed, initval=0)

        if not signed:
            seq(odata(shifted_abs_odata), cond=accept)
        else:
            seq(odata(vtypes.Mux(osign == 0, shifted_abs_odata, vtypes.Unot(shifted_abs_odata) + 1)),
                cond=accept)

        m.Assign(data(odata))

        ovalid = m.Wire(_tmp_valid(tmp, prefix='_tmp_ovalid_'))

        v = ovalid
        for i in range(3):
            nv = m.Reg(_tmp_valid(
                tmp, prefix='_tmp_valid_reg' + str(i) + '_'), initval=0)
            seq(nv(v), cond=accept)
            v = nv
        m.Assign(valid(v))

        s = sign
        for i in range(self.latency):
            ns = m.Reg(_tmp_data(tmp, prefix='_tmp_sign' +
                                 str(i) + '_'), initval=0)
            seq(ns(s), cond=accept)
            s = ns
        m.Assign(osign(s))

        lvalid = self.left.sig_valid
        rvalid = self.right.sig_valid

        lready = self.left.sig_ready
        rready = self.right.sig_ready

        all_valid = _and_vars(lvalid, rvalid)
        all_ready = _and_vars(lready, rready)

        valid_cond = _and_vars(accept, all_ready)
        valid_reset_cond = _and_vars(valid, ready)
        data_cond = _and_vars(valid_cond, all_valid)
        ready_cond = _and_vars(accept, all_valid)

        inst = div.get_div()
        clk = m._clock
        rst = m._reset

        enable = m.Wire(_tmp_data(tmp, prefix='_tmp_enable_'))
        update = m.Wire(_tmp_data(tmp, prefix='_tmp_update_'))
        m.Assign(enable(data_cond))
        m.Assign(update(accept))  # NOT valid_cond

        params = [('W_D', width)]
        ports = [('CLK', clk), ('RST', rst),
                 ('update', update), ('enable', enable), ('valid', ovalid),
                 ('in_a', abs_ldata), ('in_b', abs_rdata), ('mod', abs_odata)]

        m.Instance(inst, ''.join(['div', str(tmp)]), params, ports)

        _connect_ready(m, lready, ready_cond)
        _connect_ready(m, rready, ready_cond)

        if not self._has_output():
            _connect_ready(m, ready, vtypes.Int(1))


class Plus(_BinaryOperator):

    def eval(self):
        return self.left.eval() + self.right.eval()


class Minus(_BinaryOperator):

    def eval(self):
        return self.left.eval() - self.right.eval()


class Sll(_BinaryOperator):
    max_width = 1024

    def _set_attributes(self):
        v = self.right.eval()
        if isinstance(v, int):
            return self.left.bit_length() + v
        v = 2 ** self.right.bit_length()
        ret = self.left.bit_length() + v
        if ret > self.max_width:
            raise ValueError("bit_length is too large '%d'" % ret)
        self.width = ret
        left_fp = self.left.get_point()
        self.point = left_fp
        self.signed = False

    def _implement(self, m, seq):
        if self.right.get_point() != 0:
            raise TypeError("shift amount must be int")
        _BinaryOperator._implement(self, m, seq)

    def eval(self):
        return self.left.eval() << self.right.eval()


class Srl(_BinaryOperator):

    def _set_attributes(self):
        self.width = self.left.bit_length()
        self.point = self.left.get_point()
        self.signed = False

    def _implement(self, m, seq):
        if self.right.get_point() != 0:
            raise TypeError("shift amount must be int")
        _BinaryOperator._implement(self, m, seq)

    def eval(self):
        return self.left.eval() >> self.right.eval()


class Sra(_BinaryOperator):

    def _set_attributes(self):
        self.width = self.left.bit_length()
        self.point = self.left.get_point()
        self.signed = self.left.get_signed()

    def _implement(self, m, seq):
        if self.right.get_point() != 0:
            raise TypeError("shift amount must be int")
        _BinaryOperator._implement(self, m, seq)

    def eval(self):
        left = self.left.eval()
        right = self.right.eval()
        if isinstance(left, int) and isinstance(right, int):
            sign = left >= 0
            left = abs(left)
            ret = left >> right
            if not sign:
                return -1 * ret
            return ret
        return Sra(left, right)


class LessThan(_BinaryOperator):

    def _set_attributes(self):
        self.width = 1
        self.point = 0
        self.signed = False

    def eval(self):
        return self.left.eval() < self.right.eval()


class GreaterThan(_BinaryOperator):

    def _set_attributes(self):
        self.width = 1
        self.point = 0
        self.signed = False

    def eval(self):
        return self.left.eval() > self.right.eval()


class LessEq(_BinaryOperator):

    def _set_attributes(self):
        self.width = 1
        self.point = 0
        self.signed = False

    def eval(self):
        return self.left.eval() <= self.right.eval()


class GreaterEq(_BinaryOperator):

    def _set_attributes(self):
        self.width = 1
        self.point = 0
        self.signed = False

    def eval(self):
        return self.left.eval() >= self.right.eval()


class Eq(_BinaryOperator):

    def _set_attributes(self):
        self.width = 1
        self.point = 0
        self.signed = False

    def eval(self):
        return self.left.eval() == self.right.eval()


class NotEq(_BinaryOperator):

    def _set_attributes(self):
        self.width = 1
        self.point = 0
        self.signed = False

    def eval(self):
        return self.left.eval() != self.right.eval()


class _BinaryLogicalOperator(_BinaryOperator):

    def _set_attributes(self):
        left = self.left.bit_length()
        right = self.right.bit_length()
        self.width = max(left, right)
        self.point = 0
        self.signed = False

    def _implement(self, m, seq):
        if self.latency != 1:
            raise ValueError("Latency mismatch '%d' vs '%s'" %
                             (self.latency, 1))

        width = self.bit_length()
        signed = False

        tmp = m.get_tmp()
        data = m.Reg(_tmp_data(tmp), width, initval=0, signed=signed)
        valid = m.Reg(_tmp_valid(tmp), initval=0)
        ready = m.Wire(_tmp_ready(tmp))
        self.sig_data = data
        self.sig_valid = valid
        self.sig_ready = ready

        ldata = self.left.sig_data
        rdata = self.right.sig_data

        lvalid = self.left.sig_valid
        rvalid = self.right.sig_valid

        lready = self.left.sig_ready
        rready = self.right.sig_ready

        all_valid = _and_vars(lvalid, rvalid)
        all_ready = _and_vars(lready, rready)

        accept = vtypes.OrList(ready, vtypes.Not(valid))

        valid_cond = _and_vars(accept, all_ready)
        valid_reset_cond = _and_vars(valid, ready)
        data_cond = _and_vars(valid_cond, all_valid)
        ready_cond = _and_vars(accept, all_valid)

        seq(data(self.op(ldata, rdata)), cond=data_cond)
        seq(valid(0), cond=valid_reset_cond)
        seq(valid(all_valid), cond=valid_cond)
        _connect_ready(m, lready, ready_cond)
        _connect_ready(m, rready, ready_cond)

        if not self._has_output():
            _connect_ready(m, ready, vtypes.Int(1))


class And(_BinaryLogicalOperator):

    def eval(self):
        return self.left.eval() & self.right.eval()


class Xor(_BinaryLogicalOperator):

    def eval(self):
        return self.left.eval() ^ self.right.eval()


class Xnor(_BinaryLogicalOperator):

    def eval(self):
        left = self.left.eval()
        right = self.right.eval()
        ret = left ^ right
        if isinstance(ret, int):
            return ret == 0
        return Xnor(left, right)


class Or(_BinaryLogicalOperator):

    def eval(self):
        return self.left.eval() | self.right.eval()


class Land(_BinaryLogicalOperator):

    def eval(self):
        left = self.left.eval()
        right = self.right.eval()
        if isinstance(left, (int, bool)) and isinstance(right, (int, bool)):
            return left and right
        return Land(left, right)


class Lor(_BinaryLogicalOperator):

    def eval(self):
        left = self.left.eval()
        right = self.right.eval()
        if isinstance(left, (int, bool)) and isinstance(right, (int, bool)):
            return left or right
        return Land(left, right)


class Uplus(_UnaryOperator):

    def eval(self):
        return self.right.eval()


class Uminus(_UnaryOperator):

    def eval(self):
        return - self.right.eval()


class _UnaryLogicalOperator(_UnaryOperator):

    def _set_attributes(self):
        right = self.right.bit_length()
        self.width = right
        self.point = 0
        self.signed = False


class Ulnot(_UnaryLogicalOperator):

    def _set_attributes(self):
        self.width = 1
        self.point = 0

    def eval(self):
        right = self.right.eval()
        if isinstance(right, (int, bool)):
            return not right
        return Ulnot(right)


class Unot(_UnaryLogicalOperator):

    def eval(self):
        return ~ self.right.eval()


class Uand(_UnaryLogicalOperator):

    def _set_attributes(self):
        self.width = 1
        self.point = 0

    def eval(self):
        right = self.right.eval()
        if isinstance(right, bool):
            return right
        if isinstance(right, int):
            width = self.right.bit_length()
            for i in range(width):
                if right & 0x1 == 0:
                    return False
                right = right >> 1
            return True
        return Uand(right)


class Unand(_UnaryLogicalOperator):

    def _set_attributes(self):
        self.width = 1
        self.point = 0

    def eval(self):
        right = self.right.eval()
        if isinstance(right, bool):
            return not right
        if isinstance(right, int):
            width = self.right.bit_length()
            for i in range(width):
                if right & 0x1 == 0:
                    return True
                right = right >> 1
            return False
        return Unand(right)


class Uor(_UnaryLogicalOperator):

    def _set_attributes(self):
        self.width = 1
        self.point = 0

    def eval(self):
        right = self.right.eval()
        if isinstance(right, bool):
            return right
        if isinstance(right, int):
            width = self.right.bit_length()
            for i in range(width):
                if right & 0x1 == 1:
                    return True
                right = right >> 1
            return False
        return Uor(right)


class Unor(_UnaryLogicalOperator):

    def _set_attributes(self):
        self.width = 1
        self.point = 0

    def eval(self):
        right = self.right.eval()
        if isinstance(right, bool):
            return not right
        if isinstance(right, int):
            width = self.right.bit_length()
            for i in range(width):
                if right & 0x1 == 1:
                    return False
                right = right >> 1
            return True
        return Unor(right)


class Uxor(_UnaryLogicalOperator):

    def _set_attributes(self):
        self.width = 1
        self.point = 0

    def eval(self):
        right = self.right.eval()
        if isinstance(right, bool):
            return right
        if isinstance(right, int):
            width = self.right.bit_length()
            ret = 1
            for i in range(width):
                ret = ret ^ (right & 0x1)
                right = right >> 1
            return ret == 1
        return Uxor(right)


class Uxnor(_UnaryLogicalOperator):

    def _set_attributes(self):
        self.width = 1
        self.point = 0

    def eval(self):
        right = self.right.eval()
        if isinstance(right, bool):
            return not right
        if isinstance(right, int):
            width = self.right.bit_length()
            ret = 1
            for i in range(width):
                ret = ret ^ (right & 0x1)
                right = right >> 1
            return ret == 0
        return Uxnor(right)


#-------------------------------------------------------------------------
# alias
def Not(*args):
    return Ulnot(*args)


def AndList(*args):
    if len(args) == 0:
        raise ValueError("LandList requires at least one argument.")
    if len(args) == 1:
        return args[0]
    left = args[0]
    for right in args[1:]:
        left = Land(left, right)
    return left


def OrList(*args):
    if len(args) == 0:
        raise ValueError("LorList requires at least one argument.")
    if len(args) == 1:
        return args[0]
    left = args[0]
    for right in args[1:]:
        left = Lor(left, right)
    return left

Ands = AndList
Ors = OrList


#-------------------------------------------------------------------------
class _SpecialOperator(_Operator):
    latency = 1

    def __init__(self, *args):
        _Operator.__init__(self)
        self.args = [_to_constant(arg) for arg in args]
        for var in self.args:
            var._add_sink(self)
        self.op = None
        self._set_attributes()
        self._set_managers()

    def _set_attributes(self):
        wargs = [arg.bit_length() for arg in self.args]
        self.width = max(*wargs)
        pargs = [arg.get_point() for arg in self.args]
        self.point = max(*pargs)
        self.signed = False
        for arg in self.args:
            if arg.get_signed():
                self.signed = True
                break

    def _set_managers(self):
        self._set_df(_get_df(*self.args))
        self._set_module(getattr(self.df, 'module', None))
        self._set_seq(getattr(self.df, 'seq', None))

    def _implement(self, m, seq):
        if self.latency != 1:
            raise ValueError("Latency mismatch '%d' vs '%s'" %
                             (self.latency, 1))

        width = self.bit_length()
        signed = self.get_signed()

        tmp = m.get_tmp()
        data = m.Reg(_tmp_data(tmp), width, initval=0, signed=signed)
        valid = m.Reg(_tmp_valid(tmp), initval=0)
        ready = m.Wire(_tmp_ready(tmp))
        self.sig_data = data
        self.sig_valid = valid
        self.sig_ready = ready

        arg_data = [arg.sig_data for arg in self.args]
        arg_valid = [arg.sig_valid for arg in self.args]
        arg_ready = [arg.sig_ready for arg in self.args]

        all_valid = _and_vars(*arg_valid)
        all_ready = _and_vars(*arg_ready)

        accept = vtypes.OrList(ready, vtypes.Not(valid))

        valid_cond = _and_vars(accept, all_ready)
        valid_reset_cond = _and_vars(valid, ready)
        data_cond = _and_vars(valid_cond, all_valid)
        ready_cond = _and_vars(accept, all_valid)

        seq(data(self.op(*arg_data)), cond=data_cond)
        seq(valid(0), cond=valid_reset_cond)
        seq(valid(all_valid), cond=valid_cond)

        for r in arg_ready:
            _connect_ready(m, r, ready_cond)

        if not self._has_output():
            _connect_ready(m, ready, vtypes.Int(1))


#-------------------------------------------------------------------------
class Pointer(_SpecialOperator):

    def __init__(self, var, pos):
        _SpecialOperator.__init__(self, var, pos)
        self.op = vtypes.Pointer

    def _set_attributes(self):
        self.width = 1
        self.point = 0
        self.signed = False

    @property
    def var(self):
        return self.args[0]

    @var.setter
    def var(self, var):
        self.args[0] = var

    @property
    def pos(self):
        return self.args[1]

    @pos.setter
    def pos(self, pos):
        self.args[1] = pos

    def eval(self):
        var = self.var.eval()
        pos = self.pos.eval()
        if isinstance(var, int) and isinstance(pos, int):
            return (var >> pos) & 0x1
        return Pointer(var, pos)


class Slice(_SpecialOperator):

    def __init__(self, var, msb, lsb):
        msb = msb.eval() if isinstance(msb, _Constant) else msb
        lsb = lsb.eval() if isinstance(lsb, _Constant) else lsb
        if not isinstance(msb, int) or not isinstance(lsb, int):
            raise TypeError('msb and lsb must be int')
        _SpecialOperator.__init__(self, var, msb, lsb)
        self.op = vtypes.Slice

    def _set_attributes(self):
        self.width = self.msb - self.lsb + 1
        self.point = 0
        self.signed = False

    @property
    def var(self):
        return self.args[0]

    @var.setter
    def var(self, var):
        self.args[0] = var

    @property
    def msb(self):
        return self.args[1]

    @msb.setter
    def msb(self, msb):
        self.args[1] = msb

    @property
    def lsb(self):
        return self.args[2]

    @lsb.setter
    def lsb(self, lsb):
        self.args[2] = lsb

    def eval(self):
        var = self.var.eval()
        msb = self.msb.eval()
        lsb = self.lsb.eval()
        if isinstance(var, int) and isinstance(msb, int) and isinstance(lsb, int):
            mask = 0
            for i in range(msb - lsb + 1):
                mask = (mask << 1) | 0x1
            return (var >> lsb) & mask
        return Slice(var, msb, lsb)


class Cat(_SpecialOperator):

    def __init__(self, *vars):
        _SpecialOperator.__init__(self, *vars)
        self.op = vtypes.Cat

    def _set_attributes(self):
        ret = 0
        for v in self.vars:
            ret += v.bit_length()
        self.width = ret
        self.point = 0
        self.signed = False

    @property
    def vars(self):
        return self.args

    @vars.setter
    def vars(self, vars):
        self.args = list(vars)

    def eval(self):
        vars = [var.eval() for var in self.vars]
        for var in vars:
            if not isinstance(var, int):
                return Cat(*vars)
        ret = 0
        for var in vars:
            ret = (ret << var.bit_length()) | var
        return ret


class Repeat(_SpecialOperator):

    def __init__(self, var, times):
        times = times.eval() if isinstance(times, _Constant) else times
        if not isinstance(times, int):
            raise TypeError('times must be int')
        _SpecialOperator.__init__(self, var, times)
        self.op = vtypes.Repeat

    def _set_attributes(self):
        self.width = self.var.bit_length() * self.times.eval()
        self.point = 0
        self.signed = False

    @property
    def var(self):
        return self.args[0]

    @var.setter
    def var(self, var):
        self.args[0] = var

    @property
    def times(self):
        return self.args[1]

    @times.setter
    def times(self, times):
        self.args[1] = times

    def eval(self):
        var = self.var.eval()
        times = self.times.eval()
        ret = 0
        for i in times:
            ret = (ret << var.bit_length()) | var
        return ret


class Cond(_SpecialOperator):

    def __init__(self, condition, true_value, false_value):
        _SpecialOperator.__init__(self, condition, true_value, false_value)
        self.op = vtypes.Cond

    def _set_attributes(self):
        true_value_fp = self.true_value.get_point()
        false_value_fp = self.false_value.get_point()
        true_value = self.true_value.bit_length() - true_value_fp
        false_value = self.false_value.bit_length() - false_value_fp
        self.width = max(true_value, false_value) + \
            max(true_value_fp, false_value_fp)
        self.point = max(true_value_fp, false_value_fp)
        self.signed = self.true_value.get_signed() or self.false_value.get_signed()

    @property
    def condition(self):
        return self.args[0]

    @condition.setter
    def condition(self, condition):
        self.args[0] = condition

    @property
    def true_value(self):
        return self.args[1]

    @true_value.setter
    def true_value(self, true_value):
        self.args[1] = true_value

    @property
    def false_value(self):
        return self.args[2]

    @false_value.setter
    def false_value(self, false_value):
        self.args[2] = false_value

    def eval(self):
        condition = self.condition.eval()
        true_value = self.true_value.eval()
        false_value = self.false_value.eval()
        if isinstance(condition, (int, bool)):
            if condition:
                return true_value
            else:
                return false_value
        return Cond(condition, true_value, false_value)


def Mux(condition, true_value, false_value):
    # return the result immediately if the condition can be resolved now
    if isinstance(condition, (bool, int, float, str, list, tuple)):
        return true_value if condition else false_value
    return Cond(condition, true_value, false_value)


#-------------------------------------------------------------------------
class CustomOp(_SpecialOperator):

    def __init__(self, op, *vars):
        _SpecialOperator.__init__(self, *vars)
        self.op = op

    def eval(self):
        return self


#-------------------------------------------------------------------------
class LUT(_SpecialOperator):
    latency = 1

    def __init__(self, address, patterns, width=32, point=0, signed=False):
        _SpecialOperator.__init__(self, address)
        self.op = None
        self.width = width
        self.point = point
        self.signed = signed
        self.patterns = patterns

    def _set_attributes(self):
        pass

    @property
    def address(self):
        return self.args[0]

    @address.setter
    def address(self, address):
        self.args[0] = address

    def _implement(self, m, seq):
        if self.latency != 1:
            raise ValueError("Latency mismatch '%d' vs '%s'" %
                             (self.latency, 1))

        width = self.bit_length()
        signed = self.get_signed()

        tmp = m.get_tmp()
        data = m.Wire(_tmp_data(tmp), width, signed=signed)
        valid = m.Reg(_tmp_valid(tmp), initval=0)
        ready = m.Wire(_tmp_ready(tmp))
        self.sig_data = data
        self.sig_valid = valid
        self.sig_ready = ready

        arg_data = self.address.sig_data

        arg_valid = self.address.sig_valid

        arg_ready = self.address.sig_ready

        all_valid = _and_vars(arg_valid)
        all_ready = _and_vars(arg_ready)

        accept = vtypes.OrList(ready, vtypes.Not(valid))

        valid_cond = _and_vars(accept, all_ready)
        valid_reset_cond = _and_vars(valid, ready)
        data_cond = _and_vars(valid_cond, all_valid)
        ready_cond = _and_vars(accept, all_valid)

        size = int(log(len(self.patterns), 2))

        inst = rom.mkROMDefinition('_'.join(['', 'LUT', str(tmp)]), self.patterns,
                                   size, width, sync=True, with_enable=True)

        address = m.Wire(_tmp_data(tmp, prefix='_tmp_address_'), width=size)
        address.assign(arg_data)

        clk = m._clock

        ports = [('CLK', clk), ('addr', address),
                 ('enable', data_cond), ('val', data)]

        m.Instance(inst, '_'.join(['LUT', str(tmp)]), ports=ports)

        seq(valid(0), cond=valid_reset_cond)
        seq(valid(all_valid), cond=valid_cond)

        _connect_ready(m, arg_ready, ready_cond)

        if not self._has_output():
            _connect_ready(m, ready, vtypes.Int(1))


#-------------------------------------------------------------------------
class _Delay(_UnaryOperator):

    def __init__(self, right):
        _UnaryOperator.__init__(self, right)
        # parent value for delayed_value and previous_value
        self.parent_value = None

    def _set_parent_value(self, value):
        self.parent_value = value

    def _get_parent_value(self):
        return self.parent_value

    def eval(self):
        return self

    def _implement(self, m, seq):
        if self.latency != 1:
            raise ValueError("Latency mismatch '%d' vs '%s'" %
                             (self.latency, 1))

        width = self.bit_length()
        signed = self.get_signed()

        tmp = m.get_tmp()
        data = m.Reg(_tmp_data(tmp), width, initval=0, signed=signed)
        valid = m.Reg(_tmp_valid(tmp), initval=0)
        ready = m.Wire(_tmp_ready(tmp))
        self.sig_data = data
        self.sig_valid = valid
        self.sig_ready = ready

        rdata = self.right.sig_data

        rvalid = self.right.sig_valid

        rready = self.right.sig_ready

        all_valid = _and_vars(rvalid)
        all_ready = _and_vars(rready)

        accept = vtypes.OrList(ready, vtypes.Not(valid))

        valid_cond = _and_vars(accept, all_ready)
        valid_reset_cond = _and_vars(valid, ready)
        data_cond = _and_vars(valid_cond, all_valid)
        ready_cond = _and_vars(accept, all_valid)

        seq(data(rdata), cond=data_cond)
        seq(valid(0), cond=valid_reset_cond)
        seq(valid(all_valid), cond=valid_cond)
        _connect_ready(m, rready, ready_cond)

        if not self._has_output():
            _connect_ready(m, ready, vtypes.Int(1))


#-------------------------------------------------------------------------
class _Prev(_UnaryOperator):
    latency = 0

    def __init__(self, right):
        _UnaryOperator.__init__(self, right)
        # parent value for delayed_value and previous_value
        self.parent_value = None

    def _set_parent_value(self, value):
        self.parent_value = value

    def _get_parent_value(self):
        return self.parent_value

    def eval(self):
        return self

    def _implement(self, m, seq):
        if self.latency != 0:
            raise ValueError("Latency mismatch '%d' vs '%s'" %
                             (self.latency, 0))

        width = self.bit_length()
        signed = self.get_signed()

        tmp = m.get_tmp()
        data = m.Reg(_tmp_data(tmp), width, initval=0, signed=signed)
        valid = self.parent_value.sig_valid
        ready = self.parent_value.sig_ready
        self.sig_data = data
        self.sig_valid = valid
        self.sig_ready = ready

        rdata = self.right.sig_data

        data_cond = _and_vars(valid, ready)

        seq(data(rdata), cond=data_cond)


#-------------------------------------------------------------------------
class _Constant(_Numeric):

    def __init__(self, value):
        _Numeric.__init__(self)
        self.value = value
        self.signed = False
        self._set_attributes()
        self._set_managers()
        self.sig_data = self.value

    def _set_attributes(self):
        self.width = self.value.bit_length() + 1
        self.point = 0
        self.signed = False

    def _set_managers(self):
        self._set_df(_get_df(self.value))
        self._set_module(getattr(self.df, 'module', None))
        self._set_seq(getattr(self.df, 'seq', None))

    def eval(self):
        return self.value

    def _implement(self, m, seq):
        data = self.value
        valid = None
        ready = None
        self.sig_data = data
        self.sig_valid = valid
        self.sig_ready = ready


#-------------------------------------------------------------------------
class _Variable(_Numeric):

    def __init__(self, data=None, valid=None, ready=None, width=32, point=0, signed=False):
        _Numeric.__init__(self)
        self.input_data = data
        self.input_valid = valid
        self.input_ready = ready
        if isinstance(self.input_data, _Numeric):
            self.input_data._add_sink(self)
        self.width = width
        self.point = point
        self.signed = signed

    def eval(self):
        return self

    def output(self, data, valid=None, ready=None):
        if isinstance(self.input_data, _Numeric):
            self.input_data.output(data, valid, ready)
            return
        _Numeric.output(self, data, valid, ready)

    def connect(self, data, valid=None, ready=None):
        if self.sig_data is not None:
            raise ValueError("Input signals are already synthesized.")

        if not isinstance(data, (_Numeric, vtypes._Numeric, int, bool)):
            raise TypeError(
                "'data' must be dtypes._Numeric or vtypes._Numeric.")
        if valid is not None and not isinstance(valid, (vtypes._Numeric, int, bool)):
            raise TypeError(
                "'valid' must be None, vtypes._Numeric, int, or bool.")
        if ready is not None and not isinstance(ready, vtypes._Numeric):
            raise TypeError("'ready' must be None or vtypes._Numeric.")

        self.input_data = data
        self.input_valid = valid
        self.input_ready = ready
        if isinstance(self.input_data, _Numeric):
            self.input_data._add_sink(self)

    #-------------------------------------------------------------------------
    def write(self, wdata, cond=None):
        if self.sig_data is None:
            if self.m is None:
                raise ValueError("Module information is not set.")
            self._implement_input(self.m, self.seq, aswire=True)

        if isinstance(self.sig_data, vtypes.Input):
            raise TypeError("Variable with Input type is not supported.")

        if isinstance(self.sig_data, vtypes.Wire):
            if hasattr(self, 'sig_data_write'):
                data = self.sig_data_write
            else:
                data = self.m.TmpReg(self.bit_length(), initval=0)
                self.sig_data_write = data
                self.sig_data.assign(data)
        else:
            data = self.sig_data

        if self.sig_valid is None:
            valid = 1
        elif isinstance(self.sig_valid, vtypes.Wire):
            if hasattr(self, 'sig_valid_write'):
                valid = self.sig_valid_write
            else:
                valid = self.m.TmpReg(initval=0)
                self.sig_valid_write = valid
                self.sig_valid.assign(valid)
        else:
            valid = self.sig_valid

        if self.sig_ready is None:
            ready = 1
        else:
            ready = self.sig_ready

        if cond is not None:
            self.seq.If(cond)

        if self.sig_ready is None:
            ack = None
        else:
            ack = vtypes.OrList(ready, vtypes.Not(valid))

        self.seq.If(ack)(
            data(wdata)
        )

        if self.sig_valid is not None:
            self.seq.Then()(
                valid(1),
            )
            self.seq.Delay(1)(
                valid(0)
            )
            if self.sig_ready is not None:
                self.seq.If(vtypes.AndList(valid, vtypes.Not(ready)))(
                    valid(valid)  # overwrite previous de-assertion
                )

        return ack

    #--------------------------------------------------------------------------
    def _implement(self, m, seq):
        if self.input_data is None:
            raise TypeError("'input_data' must not be None.")

        # if input_data is a standard signal, skip
        if not isinstance(self.input_data, _Numeric):
            return

        if self.input_data.sig_data is None:
            self.input_data._implement(m, seq)

        self.sig_data = self.input_data.sig_data
        self.sig_valid = self.input_data.sig_valid
        self.sig_ready = self.input_data.sig_ready

    def _implement_input(self, m, seq, aswire=False):
        if self.input_data is None:
            raise TypeError("'input_data' must not be None")

        # if input_data is an other variable, skip
        if isinstance(self.input_data, _Numeric):
            return

        # if already synthesized
        if self.sig_data is not None:
            return

        type_i = m.Wire if aswire else m.Input
        type_o = m.Wire if aswire else m.Output

        width = self.bit_length()
        signed = self.get_signed()

        if isinstance(self.input_data, (vtypes._Numeric, int, bool)):
            self.sig_data = self.input_data
        else:
            self.sig_data = type_i(self.input_data, width, signed=signed)

        if isinstance(self.input_valid, (vtypes._Numeric, int, bool)):
            self.sig_valid = self.input_valid
        elif self.input_valid is not None:
            self.sig_valid = type_i(self.input_valid)
        else:
            self.sig_valid = None

        if isinstance(self.input_ready, (vtypes.Wire, vtypes.Output)):
            self.sig_ready = self.input_ready
        elif self.input_ready is not None:
            self.sig_ready = type_o(self.input_ready)
        else:
            self.sig_ready = None

    def _implement_output(self, m, seq, aswire=False):
        if isinstance(self.input_data, _Numeric):
            if self.input_data.output_sig_data is None:
                self.input_data._implement_output(m, seq, aswire)
            self.output_sig_data = self.input_data.output_sig_data
            self.output_sig_valid = self.input_data.output_sig_valid
            self.output_sig_ready = self.input_data.output_sig_ready
            return
        _Numeric._implement_output(self, m, seq, aswire)

    #-------------------------------------------------------------------------
    # __getattribute__() method is always called,
    # whenever fields of the node is accessed.
    def __getattribute__(self, attr):
        # for isinstance method
        if attr == '__class__':
            return _Numeric.__getattribute__(self, '__class__')

        try:
            input_data = _Numeric.__getattribute__(self, 'input_data')
        except AttributeError:
            return _Numeric.__getattribute__(self, attr)

        # always returns input_data for 'input_data' attribute
        if attr == 'input_data':
            return input_data

        # if it has a variable alias, redirect to it
        if isinstance(input_data, _Numeric):
            return getattr(input_data, attr)

        # nornal access
        return _Numeric.__getattribute__(self, attr)


#-------------------------------------------------------------------------
class _ParameterVariable(_Variable):

    def __init__(self, data, width=32, point=0, signed=False, value=None):
        if isinstance(data, _Numeric):
            raise TypeError(
                "_ParameterVariable cannot receive type '%s'" % str(type(data)))

        if value is not None and not isinstance(data, str):
            raise TypeError(
                "Required str for 'data', when 'value' is assigned")

        _Variable.__init__(self, data=data, width=width,
                           point=point, signed=signed)
        self.value = value

    def _implement(self, m, seq):
        pass

    def _implement_input(self, m, seq, aswire=False):
        type_i = m.Wire if aswire else m.Input

        width = self.bit_length()
        signed = self.get_signed()

        if isinstance(self.input_data, (vtypes._Numeric, int, bool)):
            self.sig_data = self.input_data
        elif self.value is not None:
            self.sig_data = m.Parameter(self.input_data, self.value,
                                        width=self.width, signed=self.signed)
        else:
            self.sig_data = type_i(
                self.input_data, self.width, signed=self.signed)

        self.sig_valid = None
        self.sig_ready = None

    def __getattribute__(self, attr):
        # normal access
        return _Numeric.__getattribute__(self, attr)


#-------------------------------------------------------------------------
class _Accumulator(_UnaryOperator):
    latency = 1
    ops = (vtypes.Plus, )

    def __init__(self, right, initval=None, enable=None, reset=None, width=32, signed=False):
        self.initval = _to_constant(
            initval) if initval is not None else _to_constant(0)
        self.enable = _to_constant(enable)
        if self.enable is not None:
            self.enable._add_sink(self)
        self.reset = _to_constant(reset)
        if self.reset is not None:
            self.reset._add_sink(self)
        if not isinstance(self.initval, _Constant):
            raise TypeError("initval must be Constant, not '%s'" %
                            str(type(self.initval)))
        _UnaryOperator.__init__(self, right)
        self.width = width
        self.signed = signed
        self.label = None

    def _set_attributes(self):
        self.point = self.right.get_point()

    def _set_managers(self):
        self._set_df(_get_df(self.right, self.initval,
                             self.enable, self.reset))
        self._set_module(getattr(self.df, 'module', None))
        self._set_seq(getattr(self.df, 'seq', None))

    def eval(self):
        return self

    def _implement(self, m, seq):
        if self.latency != 1:
            raise ValueError("Latency mismatch '%d' vs '%s'" %
                             (self.latency, 1))

        initval_data = self.initval.sig_data
        #initval_valid = self.initval.sig_valid
        #initval_ready = self.initval.sig_ready

        width = self.bit_length()
        signed = self.get_signed()

        tmp = m.get_tmp()
        data = m.Reg(_tmp_data(tmp), width,
                     initval=initval_data, signed=signed)
        valid = m.Reg(_tmp_valid(tmp), initval=0)
        ready = m.Wire(_tmp_ready(tmp))
        self.sig_data = data
        self.sig_valid = valid
        self.sig_ready = ready

        rdata = self.right.sig_data
        enabledata = self.enable.sig_data if self.enable is not None else None
        resetdata = self.reset.sig_data if self.reset is not None else None

        rvalid = self.right.sig_valid
        enablevalid = self.enable.sig_valid if self.enable is not None else None
        resetvalid = self.reset.sig_valid if self.reset is not None else None

        rready = self.right.sig_ready
        enableready = self.enable.sig_ready if self.enable is not None else None
        resetready = self.reset.sig_ready if self.reset is not None else None

        all_valid = _and_vars(rvalid, enablevalid, resetvalid)
        all_ready = _and_vars(rready, enableready, resetready)

        accept = vtypes.OrList(ready, vtypes.Not(valid))

        valid_cond = _and_vars(accept, all_ready)
        valid_reset_cond = _and_vars(valid, ready)
        data_cond = _and_vars(valid_cond, all_valid)
        ready_cond = _and_vars(accept, all_valid)

        value = data
        for op in self.ops:
            if not isinstance(op, type):
                value = op(value, rdata)
            elif issubclass(op, vtypes._BinaryOperator):
                value = op(value, rdata)
            elif issubclass(op, vtypes._UnaryOperator):
                value = op(value)

            if not isinstance(value, vtypes._Numeric):
                raise TypeError("Operator '%s' returns unsupported object type '%s'."
                                % (str(op), str(type(value))))

        # for Ireg
        if not self.ops:
            value = rdata

        if self.reset is not None:
            reset_value = initval_data
            for op in self.ops:
                if not isinstance(op, type):
                    reset_value = op(reset_value, rdata)
                elif issubclass(op, vtypes._BinaryOperator):
                    reset_value = op(reset_value, rdata)
                elif issubclass(op, vtypes._UnaryOperator):
                    reset_value = op(reset_value)

                if not isinstance(reset_value, vtypes._Numeric):
                    raise TypeError("Operator '%s' returns unsupported object type '%s'."
                                    % (str(op), str(type(reset_value))))

        if self.enable is not None:
            enable_data_cond = _and_vars(data_cond, enabledata)
            seq(data(value), cond=enable_data_cond)
            _connect_ready(m, enableready, ready_cond)
        else:
            seq(data(value), cond=data_cond)

        seq(valid(0), cond=valid_reset_cond)
        seq(valid(all_valid), cond=valid_cond)
        _connect_ready(m, rready, ready_cond)

        if self.reset is not None:
            if self.enable is None:
                reset_data_cond = _and_vars(data_cond, resetdata)
                seq(data(reset_value), cond=reset_data_cond)
            else:
                reset_data_cond = _and_vars(data_cond, resetdata)
                seq(data(initval_data), cond=reset_data_cond)
                reset_enable_data_cond = _and_vars(
                    data_cond, enabledata, resetdata)
                seq(data(reset_value), cond=reset_enable_data_cond)
            _connect_ready(m, resetready, ready_cond)

        if not self._has_output():
            _connect_ready(m, ready, vtypes.Int(1))


class Ireg(_Accumulator):
    ops = ()

    def __init__(self, right, initval=0, enable=None, reset=None, width=32, signed=False):
        _Accumulator.__init__(self, right, initval,
                              enable, reset, width, signed)
        self.label = 'reg'


class Iadd(_Accumulator):
    ops = (vtypes.Plus, )

    def __init__(self, right, initval=0, enable=None, reset=None, width=32, signed=False):
        _Accumulator.__init__(self, right, initval,
                              enable, reset, width, signed)


class Isub(_Accumulator):
    ops = (vtypes.Minus, )

    def __init__(self, right, initval=0, enable=None, reset=None, width=32, signed=False):
        _Accumulator.__init__(self, right, initval,
                              enable, reset, width, signed)


class Imul(_Accumulator):
    #latency = 6
    latency = 1
    ops = (vtypes.Times, )

    def __init__(self, right, initval=1, enable=None, reset=None, width=32, signed=False):
        _Accumulator.__init__(self, right, initval,
                              enable, reset, width, signed)


class Idiv(_Accumulator):
    latency = 32
    op = ()

    def __init__(self, right, initval=1, enable=None, reset=None, width=32, signed=False):
        raise NotImplementedError()
        _Accumulator.__init__(self, right, initval,
                              enable, reset, width, signed)


class Icustom(_Accumulator):

    def __init__(self, ops, right, initval=0, enable=None, reset=None,
                 width=32, signed=False, label=None):
        _Accumulator.__init__(self, right, initval,
                              enable, reset, width, signed)
        if not isinstance(ops, (tuple, list)):
            ops = tuple([ops])
        self.ops = ops
        self.label = label


#-------------------------------------------------------------------------
class Int(_Constant):

    def __init__(self, value, signed=True):
        _Constant.__init__(self, value)
        self.signed = signed

    def _set_attributes(self):
        self.width = self.value.bit_length() + 1
        self.point = 0

    def _implement(self, m, seq):
        data = vtypes.Int(self.value, width=self.width)
        valid = None
        ready = None
        self.sig_data = data
        self.sig_valid = valid
        self.sig_ready = ready


class Float(_Constant):

    def _set_attributes(self):
        self.width = 32
        self.point = 0
        self.signed = True


class FixedPoint(_Constant):

    def __init__(self, value, point=0, signed=True):
        _Constant.__init__(self, value)
        self.point = point
        self.signed = signed

    def _set_attributes(self):
        self.width = self.value.bit_length() + 1
        self.point = 0

    def _implement(self, m, seq):
        data = vtypes.Int(self.value, width=self.width)
        valid = None
        ready = None
        self.sig_data = data
        self.sig_valid = valid
        self.sig_ready = ready


class Str(_Constant):

    def _set_attributes(self):
        self.width = 0
        self.point = 0
        self.signed = False


#-------------------------------------------------------------------------
def _RegionAcc(op, right, size, initval=0, enable=None, reset=None,
               width=32, signed=False, filter=False, filter_value=0):

    counter = Counter(1, maxval=size, initval=0, enable=enable, reset=reset)

    valid = (counter == size - 1).prev(1)

    if enable is not None:
        valid = Land(valid, enable)

    if reset is None:
        reset = valid.prev(1)
    else:
        reset = Lor(reset, valid.prev(1))

    comp = op(right, initval=initval, enable=enable,
              reset=reset, width=width, signed=signed)
    if filter:
        comp = Mux(valid, comp, filter_value)

    return comp, valid


def RegionReg(right, size, initval=0, enable=None, reset=None,
              width=32, signed=False, filter=False, filter_value=0):
    return _RegionAcc(Ireg, right, size, initval, enable, reset,
                      width, signed, filter, filter_value)


def RegionAdd(right, size, initval=0, enable=None, reset=None,
              width=32, signed=False, filter=False, filter_value=0):
    return _RegionAcc(Iadd, right, size, initval, enable, reset,
                      width, signed, filter, filter_value)


def RegionSub(right, size, initval=0, enable=None, reset=None,
              width=32, signed=False, filter=False, filter_value=0):
    return _RegionAcc(Isub, right, size, initval, enable, reset,
                      width, signed, filter, filter_value)


def RegionMul(right, size, initval=0, enable=None, reset=None,
              width=32, signed=False, filter=False, filter_value=0):
    return _RegionAcc(Imul, right, size, initval, enable, reset,
                      width, signed, filter, filter_value)


def RegionDiv(right, size, initval=0, enable=None, reset=None,
              width=32, signed=False, filter=False, filter_value=0):
    return _RegionAcc(Idiv, right, size, initval, enable, reset,
                      width, signed, filter, filter_value)


def RegionCustom(ops, right, size, initval=0, enable=None, reset=None,
                 width=32, signed=False, filter=False, filter_value=0):
    op = partial(Icustom, ops)
    return _RegionAcc(op, right, size, initval, enable, reset,
                      width, signed, filter, filter_value)


#-------------------------------------------------------------------------
def Counter(step=None, maxval=None, initval=0, enable=None, reset=None, width=32, signed=False):
    if step is None:
        step = 1

    step = _to_constant(step)
    if not isinstance(step, _Constant):
        raise TypeError("'step' must be constant")
    raw_step = step.value

    initval = _to_constant(initval)
    if not isinstance(initval, _Constant):
        raise TypeError("'initval' must be constant")
    raw_initval = initval.value

    if maxval is None:
        return Icustom(lambda a, b: a + b,
                       step, initval=initval, enable=enable, reset=reset,
                       width=width, signed=signed,
                       label='Counter')

    #maxval = _to_constant(maxval)
    # if not isinstance(maxval, _Constant):
    #    raise TypeError("'maxval' must be constant")
    #raw_maxval = maxval.value

    # return Icustom(lambda a, b: vtypes.Mux(a >= raw_maxval - raw_step, raw_initval, a + b),
    #               step, initval=initval, enable=enable, reset=reset,
    #               width=width, signed=signed,
    #               label='Counter')
    return Icustom(lambda a, b: vtypes.Mux(a >= maxval - raw_step, raw_initval, a + b),
                   step, initval=initval, enable=enable, reset=reset,
                   width=width, signed=signed,
                   label='Counter')


#-------------------------------------------------------------------------
def make_condition(*cond, **kwargs):
    ready = kwargs['ready'] if 'ready' in kwargs else None

    _cond = []
    for c in cond:
        if isinstance(c, (tuple, list)):
            _cond.extend(c)
        else:
            _cond.append(c)

    cond = _cond

    new_cond = []
    for c in cond:
        if c is None:
            continue
        if isinstance(c, _Numeric):
            d, v = c.read(cond=ready)
            new_cond.append(d)
            new_cond.append(v)
        else:
            new_cond.append(c)

    return _make_condition(*new_cond)


#-------------------------------------------------------------------------
def is_dataflow_object(*objs):
    for obj in objs:
        if isinstance(obj, _Node):
            return True
    return False


#-------------------------------------------------------------------------
def _to_constant(obj):
    if isinstance(obj, (int, float, bool, str)):
        return Constant(obj)
    if isinstance(obj, vtypes._Numeric):
        return _from_vtypes_value(obj)
    return obj


def _tmp_data(val, prefix='_tmp_data_'):
    return ''.join([prefix, str(val)])


def _tmp_valid(val, prefix='_tmp_valid_'):
    return ''.join([prefix, str(val)])


def _tmp_ready(val, prefix='_tmp_ready_'):
    return ''.join([prefix, str(val)])


def _get_df(*vars):
    ret = None
    for var in vars:
        v = getattr(var, 'df', None)
        if v is None:
            continue
        if ret is None:
            ret = v
            continue
        if v.object_id < ret.object_id:
            if v.module != ret.module:
                raise ValueError("Different modules")
            if id(v.clock) != id(ret.clock):
                raise ValueError("Different clock domains: '%s' and '%s'" %
                                 (str(v.clock), str(ret.clock)))
            if id(v.reset) != id(ret.reset):
                raise ValueError("Different reset domains: '%s' and '%s'" %
                                 (str(v.reset), str(ret.reset)))
            ret = v
    return ret


def _max(*vars):
    m = None
    for v in vars:
        if v is None:
            continue
        if m is None:
            m = v
            continue
        if m < v:
            m = v
    return m


def _and_vars(*vars):
    if not vars:
        return vtypes.Int(1)
    ret = None
    for var in vars:
        if var is None:
            continue
        if ret is None:
            ret = var
        else:
            ret = vtypes.AndList(ret, var)
    if ret is None:
        return vtypes.Int(1)
    return ret


def _connect_ready(m, var, ready):
    if var is None:
        return

    prev_assign = var._get_assign()
    if not prev_assign:
        m.Assign(var(ready))
    elif (isinstance(prev_assign.statement.right, vtypes.Int) and
          prev_assign.statement.right.value == 1):
        prev_assign.overwrite_right(ready)
        m.remove(prev_assign)
        m.append(prev_assign)
    else:
        prev_assign.overwrite_right(
            _and_vars(prev_assign.statement.right, ready))
        m.remove(prev_assign)
        m.append(prev_assign)


def _from_vtypes_value(value):
    if isinstance(value, vtypes.Int):
        if not isinstance(value.value, int):
            raise TypeError("Unsupported type for Constant '%s'" %
                            str(type(value)))
        return Int(value.value)

    if isinstance(value, vtypes.Float):
        return Float(value.value)

    if isinstance(value, vtypes.Str):
        return Str(value.value)

    if isinstance(value, vtypes._Numeric):
        return Variable(value)

    raise TypeError("Unsupported type '%s'" % str(type(value)))
