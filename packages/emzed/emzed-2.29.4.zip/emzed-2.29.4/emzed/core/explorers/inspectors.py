import os

from ..data_types import PeakMap, Table
from ..data_types.col_types import Blob
from ..data_types.hdf5_table_proxy import Hdf5TableProxy


def has_inspector(clz):
    return clz in (PeakMap, Table, Blob, Hdf5TableProxy)


def try_to_load(path):
    ext = os.path.splitext(path)[1]
    if ext.upper() in (".MZXML", ".MZML", ".MZDATA"):
        import emzed
        return emzed.io.loadPeakMap(path)
    elif ext == ".table":
        import emzed
        return emzed.io.loadTable(path)
    elif ext == ".hdf5":
        return Hdf5TableProxy(path)
    else:
        raise ValueError("I can not handle %s files" % ext)


def inspector(obj, *a, **kw):
    if isinstance(obj, basestring):
        obj = try_to_load(obj)
    if isinstance(obj, PeakMap):
        from peakmap_explorer import inspectPeakMap
        return lambda: inspectPeakMap(obj, *a, **kw)
    elif isinstance(obj, (Table, Hdf5TableProxy)):
        from table_explorer import inspect
        return lambda: inspect(obj, *a, **kw)
    elif isinstance(obj, (list, tuple)) and all(isinstance(t, Table) for t in obj):
        from table_explorer import inspect
        return lambda: inspect(obj, *a, **kw)
    elif isinstance(obj, Blob):
        from image_dialog import ImageDialog

        modal = kw.get("modal", True)

        if modal:
            def show():
                dlg = ImageDialog(obj.data)
                dlg.raise_()
                dlg.exec_()
        else:
            def show():
                dlg = ImageDialog(obj.data, parent=kw.get("parent"))
                dlg.show()
        return show

    return None


def inspect(obj, *a, **kw):
    insp = inspector(obj, *a, **kw)
    if insp is not None:
        return insp()
    else:
        raise Exception("no inspector for %r" % obj)
