# encoding: utf-8

import sys
import multiprocessing


def integrate(ftable, integratorid="std", msLevel=None, showProgress=True, n_cpus=-1,
              min_size_for_parallel_execution=500, post_fixes=None):
    """ integrates features  in ftable.
        returns processed table. ``ftable`` is not changed inplace.

        The peak integrator corresponding to the integratorId is
        defined in ``algorithm_configs.py`` or ``local_configs.py``

        n_cpus <= 0 has special meaning:
            n_cpus = 0 means "use all cpu cores"
            n_cpus = -1 means "use all but one cpu cores", etc

    """

    needed_columns = ["mzmin", "mzmax", "rtmin", "rtmax", "peakmap"]
    if post_fixes is None:
        post_fixes = ftable.supportedPostfixes(needed_columns)
        if not post_fixes:
            raise Exception("is no feature table")
    else:
        col_names = ftable.getColNames()
        missing = []
        for post_fix in post_fixes:
            for name in needed_columns:
                if name + post_fix not in col_names:
                    missing.append(name + post_fix)
        if missing:
            raise ValueError("column name(s) %s missing" % (", ".join(missing)))

    if sys.platform == "win32":
        # if subprocesses use python.exe a console window pops up for each
        # subprocess. this is quite ugly..
        import os.path
        multiprocessing.set_executable(os.path.join(
                                       os.path.dirname(sys.executable),
                                       "pythonw.exe")
                                       )
    import time
    from ..core.data_types import Table

    started = time.time()

    messages, n_cpus = check_num_cpus(n_cpus, len(ftable), min_size_for_parallel_execution)

    if showProgress:
        print
        if messages:
            print "\n".join(messages)
        print "integrate table using", n_cpus, "processes"
        print

    if n_cpus == 1:
        __, result = _integrate((0, ftable, post_fixes, integratorid, msLevel, showProgress,))
    else:
        pool = multiprocessing.Pool(n_cpus)
        args = []
        all_pms = []
        for i in range(n_cpus):
            partial = ftable[i::n_cpus]
            show_progress = (i == 0)  # only first process prints progress status
            args.append(
                (i, partial, post_fixes, integratorid, msLevel, show_progress))
            all_pms.append(partial.peakmap.values)

        # map_async() avoids bug of map() when trying to stop jobs using ^C
        results = pool.map_async(_integrate, args).get()

        results.sort()  # sorts by first entry which is the index of the partial table
        tables = [t for (i, t) in results]

        # as peakmaps are serialized/unserialized for paralell execution, lots of duplicate
        # peakmaps come back after. we reset those columns to their state before spreading
        # them:
        for t, pms in zip(tables, all_pms):
            t.replaceColumn("peakmap", pms, type_=ftable.getColType("peakmap"),
                            format_=ftable.getColFormat("peakmap"))

        # at least needed on win, else worker processes accumulate:
        pool.close()

        tables = [t for t in tables if len(t) > 0]
        result = Table.stackTables(tables)

    if showProgress:
        needed = time.time() - started
        minutes = int(needed) / 60
        seconds = needed - minutes * 60
        print
        if minutes:
            print "needed %d minutes and %.1f seconds" % (minutes, seconds)
        else:
            print "needed %.1f seconds" % seconds
    return result


def _integrate((idx, ftable, supportedPostfixes, integratorid, msLevel, showProgress)):
    from ..algorithm_configs import peakIntegrators
    import sys

    integrator = dict(peakIntegrators).get(integratorid)
    if integrator is None:
        raise Exception("unknown integrator '%s'" % integratorid)

    resultTable = ftable.copy()

    lastcent = -1
    for postfix in supportedPostfixes:
        areas = []
        rmses = []
        peak_shape_params = []
        eics = []
        baselines = []
        for i, row in enumerate(ftable.rows):
            if showProgress:
                # integer div here !
                cent = ((i + 1) * 20) / len(ftable) / len(supportedPostfixes)
                if cent != lastcent:
                    print cent * 5,
                    try:
                        sys.stdout.flush()
                    except IOError:
                        # migh t happen on win cmd console
                        pass
                    lastcent = cent
            rtmin = ftable.getValue(row, "rtmin" + postfix)
            rtmax = ftable.getValue(row, "rtmax" + postfix)
            mzmin = ftable.getValue(row, "mzmin" + postfix)
            mzmax = ftable.getValue(row, "mzmax" + postfix)
            peakmap = ftable.getValue(row, "peakmap" + postfix)
            if rtmin is None or rtmax is None or mzmin is None or mzmax is None\
                    or peakmap is None:
                area = rmse = params = eic = baseline = None
            else:
                integrator.setPeakMap(peakmap)
                result = integrator.integrate(mzmin, mzmax, rtmin, rtmax, msLevel)
                # take existing values which are not integration realated:
                area = result["area"]
                rmse = result["rmse"]
                params = result["params"]
                eic = result["eic"]
                baseline = result["baseline"]

            areas.append(area)
            rmses.append(rmse)
            peak_shape_params.append(params)
            eics.append(eic)
            baselines.append(baseline)

        resultTable._updateColumnWithoutNameCheck("method" + postfix,
                                                  integratorid, str, "%s",
                                                  insertBefore="peakmap" + postfix)

        resultTable._updateColumnWithoutNameCheck("area" + postfix, areas, float,
                                                  "%.2e", insertBefore="peakmap" + postfix)

        resultTable._updateColumnWithoutNameCheck("baseline" + postfix, baselines, float,
                                                  "%.2e", insertBefore="peakmap" + postfix)

        resultTable._updateColumnWithoutNameCheck("rmse" + postfix, rmses, float,
                                                  "%.2e", insertBefore="peakmap" + postfix)

        resultTable._updateColumnWithoutNameCheck("params" + postfix, peak_shape_params,
                                                  object, None, insertBefore="peakmap" + postfix)

        resultTable._updateColumnWithoutNameCheck("eic" + postfix, eics,
                                                  object, None, insertBefore="peakmap" + postfix)

    resultTable.meta["integrated"] = True, "\n"
    resultTable.title = "integrated: " + (resultTable.title or "")
    resultTable.resetInternals()
    return idx, resultTable


def check_num_cpus(n_cpus, table_size, min_table_size):

    messages = []
    if multiprocessing.current_process().daemon and n_cpus != 1:
        messages.append("WARNING: you choose n_cpus = %d but integrate already runs inside a "
                        "daemon process which is not allowed. therefore set n_cpus = 1" % n_cpus)
        n_cpus = 1

    if n_cpus < 0:
        n_cpus = multiprocessing.cpu_count() + n_cpus

    if n_cpus <= 0:
        messages.append("WARNING: you requested to use %d cores, "
                        "we use single core instead !" % n_cpus)
        n_cpus = 1

    if n_cpus > 1 and table_size < min_table_size:
        messages.append("INFO: as the table has les thann %d rows, we switch to one cpu mode"
                        % min_table_size)
        n_cpus = 1

    elif n_cpus > multiprocessing.cpu_count():
        messages.append("WARNING: more processes demanded than available cpu cores, this might be "
                        "inefficient")

    return messages, n_cpus
