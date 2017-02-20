import os

from rsqueakvm.error import PrimitiveFailedError
from rsqueakvm.model.numeric import W_Float, W_SmallInteger
from rsqueakvm.plugins.python.model import W_PythonObject
from rsqueakvm.plugins.python.global_state import py_space
from rsqueakvm.model.variable import W_BytesObject

from pypy.interpreter.error import OperationError
from pypy.interpreter.main import compilecode, ensure__main__
from pypy.interpreter.module import Module
from pypy.interpreter.pycode import PyCode
from pypy.module.__builtin__ import compiling as py_compiling
from pypy.objspace.std.bytesobject import W_BytesObject as WP_BytesObject
from pypy.objspace.std.floatobject import W_FloatObject as WP_FloatObject
from pypy.objspace.std.intobject import W_IntObject as WP_IntObject
from pypy.objspace.std.listobject import W_ListObject as WP_ListObject
from pypy.objspace.std.tupleobject import W_TupleObject as WP_TupleObject

from rpython.rlib import objectmodel


def _run_eval_string(source, filename, cmd):
    # Adopted from PyPy's main.py
    try:
        w = py_space.wrap

        pycode = compilecode(py_space, w(source), filename or '<string>', cmd)

        mainmodule = ensure__main__(py_space)
        assert isinstance(mainmodule, Module)
        w_globals = mainmodule.w_dict

        py_space.setitem(w_globals, w('__builtins__'), py_space.builtin)
        if filename is not None:
            py_space.setitem(w_globals, w('__file__'), w(filename))

        return pycode.exec_code(py_space, w_globals, w_globals)

    except OperationError as operationerr:
        operationerr.record_interpreter_traceback()
        raise


@objectmodel.specialize.argtype(0)
def wrap(space, wp_object):
    # import pdb; pdb.set_trace()
    if isinstance(wp_object, WP_FloatObject):
        return space.wrap_float(py_space.float_w(wp_object))
    elif isinstance(wp_object, WP_BytesObject):
        return space.wrap_string(py_space.str_w(wp_object))
    elif isinstance(wp_object, WP_ListObject):
        return space.wrap_list(
            [wrap(space, item) for item in wp_object.getitems()])
    elif isinstance(wp_object, WP_TupleObject):
        return space.wrap_list(
            [wrap(space, item) for item in wp_object.tolist()])
    elif wp_object is None or wp_object is py_space.w_None:
        return space.w_nil
    elif isinstance(wp_object, WP_IntObject):
        # WP_BoolObject inherits from WP_IntObject
        if wp_object is py_space.w_False:
            return space.w_false
        elif wp_object is py_space.w_True:
            return space.w_true
        return space.wrap_int(py_space.int_w(wp_object))
    else:
        return W_PythonObject(wp_object)


@objectmodel.specialize.argtype(0)
def unwrap(space, w_object):
    if isinstance(w_object, W_PythonObject):
        return w_object.wp_object
    elif w_object is None or w_object is space.w_nil:
        return py_space.w_None
    elif w_object is space.w_true:
        return py_space.w_True
    elif w_object is space.w_false:
        return py_space.w_False
    elif isinstance(w_object, W_Float):
        return py_space.newfloat(space.unwrap_float(w_object))
    elif isinstance(w_object, W_SmallInteger):
        return py_space.newint(space.unwrap_int(w_object))
    elif isinstance(w_object, W_BytesObject):
        # if w_object.getclass(space).is_same_object(space.w_String):
        return py_space.newbytes(space.unwrap_string(w_object))
    # import pdb; pdb.set_trace()
    print 'Cannot unwrap %s' % w_object
    raise PrimitiveFailedError


def get_pycode(source, filename, cmd):
    # source = 'def __dummy__():\n%s\n' % '\n'.join(
    #     ['    %s' % line for line in source.split('\n')])
    print 'Trying to patch:\n%s' % source
    try:
        py_code = py_compiling.compile(py_space, py_space.wrap(source),
                                       filename, cmd)
        assert isinstance(py_code, PyCode)
        co_consts_w_len = len(py_code.co_consts_w)
        if co_consts_w_len >= 1:
            if co_consts_w_len > 1:
                print 'More than 1 const produced: %s' % co_consts_w_len
            first_consts_w = py_code.co_consts_w[0]
            if not isinstance(first_consts_w, PyCode):
                print 'First const is not a PyCode'
                return py_code
            return py_code.co_consts_w[0]
    except OperationError as e:
        # import pdb; pdb.set_trace()
        print 'Failed to compile new frame: %s' % e.errorstr(py_space)
    return None


def call_method(space, wp_rcvr, methodname, args_w):
    args_w_len = len(args_w)
    if args_w_len == 1:
        arg1 = unwrap(space, args_w[0])
        return wrap(space, py_space.call_method(wp_rcvr, methodname, arg1))
    elif args_w_len == 2:
        arg1 = unwrap(space, args_w[0])
        arg2 = unwrap(space, args_w[1])
        return wrap(space, py_space.call_method(wp_rcvr, methodname,
                                                arg1, arg2))
    elif args_w_len == 3:
        arg1 = unwrap(space, args_w[0])
        arg2 = unwrap(space, args_w[1])
        arg3 = unwrap(space, args_w[2])
        return wrap(space, py_space.call_method(wp_rcvr, methodname,
                                                arg1, arg2, arg3))
    elif args_w_len == 4:
        arg1 = unwrap(space, args_w[0])
        arg2 = unwrap(space, args_w[1])
        arg3 = unwrap(space, args_w[2])
        arg4 = unwrap(space, args_w[3])
        return wrap(space, py_space.call_method(wp_rcvr, methodname,
                                                arg1, arg2, arg3, arg4))
    return wrap(space, py_space.call_method(wp_rcvr, methodname))


def call_function(space, wp_func, args_w):
    args_w_len = len(args_w)
    if args_w_len == 1:
        arg1 = unwrap(space, args_w[0])
        return wrap(space, py_space.call_function(wp_func, arg1))
    elif args_w_len == 2:
        arg1 = unwrap(space, args_w[0])
        arg2 = unwrap(space, args_w[1])
        return wrap(space, py_space.call_function(wp_func, arg1, arg2))
    elif args_w_len == 3:
        arg1 = unwrap(space, args_w[0])
        arg2 = unwrap(space, args_w[1])
        arg3 = unwrap(space, args_w[2])
        return wrap(space, py_space.call_function(wp_func, arg1, arg2, arg3))
    elif args_w_len == 4:
        arg1 = unwrap(space, args_w[0])
        arg2 = unwrap(space, args_w[1])
        arg3 = unwrap(space, args_w[2])
        arg4 = unwrap(space, args_w[3])
        return wrap(space, py_space.call_function(wp_func,
                                                  arg1, arg2, arg3, arg4))
    return wrap(space, py_space.call_function(wp_func))


def entry_point(argv):
    filename = argv[-1]
    if not os.path.isfile(filename):
        print 'File "%s" does not exist.' % filename
        return 1
    with open(filename, 'r') as f:
        runstring = f.read()
        # import pdb; pdb.set_trace()
        _run_eval_string(runstring, '<string>', 'exec')
    return 0
