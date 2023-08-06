#pylint: disable=W0201,W0223,R0901,R0902,R0904
"""
Main OP2 class
ftp://161.24.15.247/Nastran2011/seminar/SEC04-DMAP_MODULES.pdf

Datablock	Type	Description
EFMFSMS	Matrix	6 x 1 Total Effective mass matrix
EFMASSS	Matrix	6 x 6 Effective mass matrix
RBMASS	Matrix	6 x 6 Rigid body mass matrix
EFMFACS	Matrix	6 X N Modal effective mass fraction matrix
MPFACS	Matrix	6 x N Modal participation factor matrix
MEFMASS	Matrix	6 x N Modal effective mass matrix
MEFWTS	Matrix	6 x N Modal effective weight matrix
RAFGEN	Matrix	N x M Generalized force matrix
RADEFMP	Matrix	N X U2 Effective inertia loads
BHH	Matrix	N x N Viscous damping matrix
K4HH	Matrix	N x N Structural damping matrix
RADAMPZ	Matrix	N x N equivalent viscous damping ratios
RADAMPG	Matrix	N X N equivalent structural damping ratio

LAMA	LAMA	Eigenvalue summary table
OGPWG	OGPWG	Mass properties output
OQMG1	OQMG	Modal MPC forces
RANCONS	ORGY1	Constraint mode element strain energy table
RANEATC	ORGY1	Attachment mode element strain energy table
RAGCONS	OGPFB	Constraint mode grid point force table
RAGEATC	OGPFB	Attachment mode grid point force table
RAPCONS	OES	Constraint mode ply stress table
RAPEATC	OES	Attachment mode ply stress table
RASCONS	OES	Constraint mode element stress table
RAECONS	OES	Constraint mode element strain table
RASEATC	OES	Attachment mode element stress table
RAEEATC	OES	Attachment mode element strain table
OES1C	OES	Modal Element Stress Table
OES1X	OES	Modal Element Stress Table
OSTR1C	OES	Modal Element Strain Table
OSTR1X	OSTR	Modal Element Strain Table
RAQCONS	OUG	Constraint mode MPC force table
RADCONS	OUG	Constraint mode displacement table
RADEFFM	OUG	Effective inertia displacement table
RAQEATC	OUG	Attachment mode  MPC force table
RADEATC	OUG	Attachment mode displacement table
OUGV1	OUG	Eigenvector Table
RAFCONS	OEF	Constraint mode element force table
RAFEATC	OEF	Attachment mode element force table
OEF1X	OEF	Modal Element Force Table
OGPFB1	OGPFB	Modal Grid Point Force Table
ONRGY1	ONRGY1	Modal Element Strain Energy Table
ONRGY2	ONRGY1

#--------------------

RADCONS - Displacement Constraint Mode
RADDATC - Displacement Distributed Attachment Mode
RADNATC - Displacement Nodal Attachment Mode
RADEATC - Displacement Equivalent Inertia Attachment Mode
RADEFFM - Displacement Effective Inertia Mode

RAECONS - Strain Constraint Mode
RAEDATC - Strain Distributed Attachment Mode
RAENATC - Strain Nodal Attachment Mode
RAEEATC - Strain Equivalent Inertia Attachment Mode

RAFCONS - Element Force Constraint Mode
RAFDATC - Element Force Distributed Attachment Mode
RAFNATC - Element Force Nodal Attachment Mode
RAFEATC - Element Force Equivalent Inertia Attachment Mode

RALDATC - Load Vector Used to Compute the Distributed Attachment M

RANCONS - Strain Energy Constraint Mode
RANDATC - Strain Energy Distributed Attachment Mode
RANNATC - Strain Energy Nodal Attachment Mode
RANEATC - Strain Energy Equivalent Inertia Attachment Mode

RAQCONS - Ply Strains Constraint Mode
RAQDATC - Ply Strains Distributed Attachment Mode
RAQNATC - Ply Strains Nodal Attachment Mode
RAQEATC - Ply Strains Equivalent Inertia Attachment Mode

RARCONS - Reaction Force Constraint Mode
RARDATC - Reaction Force Distributed Attachment Mode
RARNATC - Reaction Force Nodal Attachment Mode
RAREATC - Reaction Force Equivalent Inertia Attachment Mode

RASCONS - Stress Constraint Mode
RASDATC - Stress Distributed Attachment Mode
RASNATC - Stress Nodal Attachment Mode
RASEATC - Stress Equivalent Inertia Attachment Mode

RAPCONS - Ply Stresses Constraint Mode
RAPDATC - Ply Stresses Distributed Attachment Mode
RAPNATC - Ply Stresses Nodal Attachment Mode
RAPEATC - Ply Stresses Equivalent Inertia Attachment Mode

RAGCONS - Grid Point Forces Constraint Mode
RAGDATC - Grid Point Forces Distributed Attachment Mode
RAGNATC - Grid Point Forces Nodal Attachment Mode
RAGEATC - Grid Point Forces Equivalent Inertia Attachment Mode

RADEFMP - Displacement PHA^T * Effective Inertia Mode

RADAMPZ - Viscous Damping Ratio Matrix
RADAMPG - Structural Damping Ratio Matrix

RAFGEN  - Generalized Forces
BHH     - Modal Viscous Damping Matrix
K4HH    - Modal Structural Damping Matrix
"""
from __future__ import (nested_scopes, generators, division, absolute_import,
                        print_function, unicode_literals)
from six import iterkeys, iteritems, string_types, itervalues
import os
import sys

import numpy as np

from pyNastran.utils import (
    object_attributes, object_methods, integer_types, ipython_info)
from pyNastran.op2.tables.monpnt import MONPNT1, MONPNT3

from pyNastran.f06.errors import FatalError
from pyNastran.op2.errors import SortCodeError, DeviceCodeError, FortranMarkerError
#from pyNastran.op2.op2_interface.op2_writer import OP2Writer
from pyNastran.op2.op2_interface.op2_f06_common import Op2F06Attributes
from pyNastran.op2.op2_interface.op2_scalar import OP2_Scalar


def read_op2(op2_filename=None, combine=True, subcases=None,
             exclude_results=None, include_results=None,
             log=None, debug=True, debug_file=None, build_dataframe=None,
             skip_undefined_matrices=True, mode='msc', encoding=None):
    """
    Creates the OP2 object without calling the OP2 class.

    Parameters
    ----------
    op2_filename : str (default=None -> popup)
        the op2_filename
    combine : bool; default=True
        True : objects are isubcase based
        False : objects are (isubcase, subtitle) based;
                will be used for superelements regardless of the option
    subcases : List[int, ...] / int; default=None->all subcases
        list of [subcase1_ID,subcase2_ID]
    exclude_results / include_results : List[str] / str; default=None
        a list of result types to exclude/include
        one of these must be None
    build_dataframe : bool (default=None -> True if in iPython, False otherwise)
        builds a pandas DataFrame for op2 objects
    skip_undefined_matrices : bool; default=False
         True : prevents matrix reading crashes
    debug : bool; default=False
        enables the debug log and sets the debug in the logger
    log : Log()
        a logging object to write debug messages to
        (.. seealso:: import logging)
    mode : str; default='msc'
        the version of the Nastran you're using
        {nx, msc, optistruct}
    debug_file : str; default=None (No debug)
        sets the filename that will be written to
    encoding : str
        the unicode encoding (default=None; system default)

    Returns
    -------
    model : OP2()
        an OP2 object

    .. todo:: creates the OP2 object without all the read methods

    .. note :: this method will change in order to return an object that
               does not have so many methods
    """
    model = OP2(log=log, debug=debug, debug_file=debug_file, mode=mode)
    model.set_subcases(subcases)
    if exclude_results and include_results:
        msg = 'exclude_results or include_results must be None\n'
        msg += 'exclude_results=%r\n' % exclude_results
        msg += 'include_results=%r\n' % include_results
        raise RuntimeError(msg)
    elif exclude_results:
        model.remove_results(exclude_results)
    elif include_results:
        model.set_results(include_results)

    model.read_op2(op2_filename=op2_filename, build_dataframe=build_dataframe,
                   skip_undefined_matrices=skip_undefined_matrices, combine=combine,
                   encoding=encoding)
    ## TODO: this will go away when OP2 is refactored
    ## TODO: many methods will be missing, but it's a start...
    ## doesn't support F06 writer
    #obj = Op2F06Attributes()
    #attr_names = object_attributes(obj, mode="public", keys_to_skip=None)
    #for attr_name in attr_names:
        #attr = getattr(model, attr_name)
        #setattr(obj, attr_name, attr)
    #obj.get_op2_stats()
    return model


#class OP2(OP2_Scalar, OP2Writer):
class OP2(OP2_Scalar):

    def __init__(self,
                 debug=True, log=None,
                 debug_file=None, mode='msc'):
        """
        Initializes the OP2 object

        Parameters
        ----------
        debug : bool; default=False
            enables the debug log and sets the debug in the logger
        log : Log()
            a logging object to write debug messages to
         (.. seealso:: import logging)
        debug_file : str; default=None (No debug)
            sets the filename that will be written to
        mode : str; default='msc'
            {msc, nx}
        """
        self.encoding = None
        self.set_mode(mode)
        make_geom = False
        assert make_geom == False, make_geom
        OP2_Scalar.__init__(self, debug=debug, log=log, debug_file=debug_file)
        self.ask = False

    def object_attributes(self, mode='public', keys_to_skip=None):
        if keys_to_skip is None:
            keys_to_skip = []

        my_keys_to_skip = [
            'object_methods', 'object_attributes',
        ]
        return object_attributes(self, mode=mode, keys_to_skip=keys_to_skip+my_keys_to_skip)

    def object_methods(self, mode='public', keys_to_skip=None):
        if keys_to_skip is None:
            keys_to_skip = []
        my_keys_to_skip = []

        my_keys_to_skip = [
            'object_methods', 'object_attributes',
        ]
        return object_methods(self, mode=mode, keys_to_skip=keys_to_skip+my_keys_to_skip)

    def __eq__(self, op2_model):
        """diffs the current op2 model vs. another op2 model"""
        if not self.read_mode == op2_model.read_mode:
            print('self.read_mode=%s op2_model.read_mode=%s ... assume True' % (
                self.read_mode, op2_model.read_mode))
            return True
        table_types = self.get_table_types()
        for table_type in table_types:
            adict = getattr(self, table_type)
            bdict = getattr(op2_model, table_type)
            if len(adict) != len(bdict):
                print('len(self.%s)=%s len(op2_model.%s)=%s' % (
                    table_type, len(adict), table_type, len(bdict)))
                return False
            for key, avalue in iteritems(adict):
                bvalue = bdict[key]
                aname = avalue.__class__.__name__
                bname = bvalue.__class__.__name__
                if not aname == bname:
                    print('type(a)=%s type(b)=%s' % (aname, bname))
                    return False
                if not any(word in aname for word in ['Array', 'Eigenvalues']):
                    msg = '%s is not an Array ... assume equal' % aname
                    print(msg)
                    raise NotImplementedError('%s __eq__' % aname)
                    #continue
                if avalue != bvalue:
                    print('key=%s table_type=%r is different; class_name=%r' % (key, table_type, aname))
                    return False
        return True

    def set_mode(self, mode):
        """
        Sets the mode as 'msc' or 'nx'
        """
        if mode.lower() == 'msc':
            self.set_as_msc()
        elif mode.lower() == 'nx':
            self.set_as_nx()
        else:
            raise RuntimeError("mode=%r and must be 'msc' or 'nx'")

    def _set_ask_vectorized(self, ask=False):
        """
        Enables vectorization

        The code will degenerate to dictionary based results when
        a result does not support vectorization.

        Vectorization is always True here.

        Parameters
        ----------
        ask: bool
            Do you want to see a GUI of result types.

        +--------+---------------+---------+------------+
        | Case # | Vectorization |  Ask    | Read Modes |
        +========+===============+=========+============+
        |    1   | True          |  True   |  1, 2      |
        +--------+---------------+---------+------------+
        |    2   | True          |  False  |  1, 2      |
        +--------+---------------+---------+------------+
        |    3   | False         |  True   |  1, 2      |
        +--------+---------------+---------+------------+
        |    4   | False         |  False  |  0         |
        +--------+---------------+---------+------------+

        Definitions
        ===========
          Vectorization - A storage structure that allows for faster read/access
                          speeds and better memory usage, but comes with a more
                          difficult to use data structure.

                          It limits the node IDs to all be integers (e.g. element
                          centroid).  Composite plate elements (even for just CTRIA3s)
                          with an inconsistent number of layers will have a more
                          difficult data structure.
          Scanning   - a quick check used to figure out how many results to process
                      that takes almost no time
          Reading    - process the op2 data
          Build      - call the __init__ on a results object (e.g. RealDisplacementArray)
          Start Over - Go to the start of the op2 file
          Ask        - launch a GUI dialog to let the user click which results to load

        Read Mode Definitions
        =====================
          0.   The default OP2 dictionary based-approach with no asking GUI (removed)
          1.   The first read of a result to get the shape of the data
          2.   The second read of a result to get the results

        Cases
        ======
          1.   Scan the block to get the size, build the object (read_mode=1),
               ask the user, start over, fill the objects (read_mode=2).
               Degenerate to read_mode=0 when read_mode=2 cannot be used based
               upon the value of ask.
          2.   Same as case #1, but don't ask the user.
               Scan the block to get the size, build the object (read_mode=1),
               start over, fill the objects (read_mode=2).
          3.   Scan the block to get the object types (read_mode=1), ask the user,
               build the object & fill it (read_mode=2)
          4.   Read the block to get the size, build the object & fill it (read_mode=0; removed)
        """
        self.ask = ask

    def read_op2(self, op2_filename=None, combine=True, build_dataframe=None,
                 skip_undefined_matrices=False, encoding=None):
        """
        Starts the OP2 file reading

        Parameters
        ----------
        op2_filename : str (default=None -> popup)
            the op2_filename
        combine : bool; default=True
            True : objects are isubcase based
            False : objects are (isubcase, subtitle) based;
                    will be used for superelements regardless of the option
        build_dataframe : bool (default=None -> True if in iPython, False otherwise)
            builds a pandas DataFrame for op2 objects
        skip_undefined_matrices : bool; default=False
             True : prevents matrix reading crashes
        encoding : str
            the unicode encoding (default=None; system default)
        """
        if build_dataframe is None:
            build_dataframe = False
            if ipython_info():
                build_dataframe = True

        if encoding is None:
            encoding = sys.getdefaultencoding()
        self.encoding = encoding

        self.skip_undefined_matrices = skip_undefined_matrices
        assert self.ask in [True, False], self.ask
        self.is_vectorized = True
        self.log.debug('combine=%s' % combine)
        self.log.debug('-------- reading op2 with read_mode=1 (array sizing) --------')
        self.read_mode = 1
        self._close_op2 = False

        # get GUI object names, build objects, but don't read data
        OP2_Scalar.read_op2(self, op2_filename=op2_filename)

        # TODO: stuff to figure out objects
        # TODO: stuff to show gui of table names
        # TODO: clear out objects the user doesn't want
        self.read_mode = 2
        self._close_op2 = True
        self.log.debug('-------- reading op2 with read_mode=2 (array filling) --------')
        OP2_Scalar.read_op2(self, op2_filename=self.op2_filename)

        self.finalize()
        if build_dataframe:
            self.build_dataframe()
        self.create_objects_from_matrices()
        self.combine_results(combine=combine)
        self.log.debug('finished reading op2')

    def create_objects_from_matrices(self):
        """
        creates the following objects:
          - sonitor3 : MONPNT3 object from the MP3F matrix
          - monitor1 : MONPNT1 object from the PMRF, PERF, PFRF, AGRF, PGRF, AFRF matrices
          """
        if 'MP3F' in self.matrices:
            self.monitor3 = MONPNT3(self._frequencies, self.matrices['MP3F'])

        # these are totally wrong...it doesn't go by component; it goes by inertial, external, flexibility, etc.
        if 'PERF' in self.matrices:
            #                                                           :)       ?       :)      :)      ?       ?
            #self.monitor1 = MONPNT1(self.frequencies, self.matrices, ['PMRF', 'AFRF', 'PFRF', 'PGRF', 'AGRF', 'PERF', ])

            #                                                           :)       ?       :)      :)2     ?       ?
            self.monitor1 = MONPNT1(self._frequencies, self.matrices, ['PMRF', 'PERF', 'PFRF', 'AGRF', 'PGRF', 'AFRF', ])

    def finalize(self):
        result_types = self.get_table_types()
        for result_type in result_types:
            result = getattr(self, result_type)
            for obj in itervalues(result):
                if hasattr(obj, 'finalize'):
                    obj.finalize()
        self.del_structs()

    def build_dataframe(self):
        """
        Converts the OP2 objects into pandas DataFrames

        .. todo:: fix issues with:
         - RealDisplacementArray
         - RealPlateStressArray (???)
         - RealPlateStrainArray (???)
         - RealCompositePlateStrainArray (???)

        C:\Anaconda\lib\site-packages\pandas\core\algorithms.py:198: DeprecationWarning: unorderable dtypes;
            returning scalar but in the future this will be an error
        sorter = uniques.argsort()
        """
        no_sort2_classes = ['RealEigenvalues', 'ComplexEigenvalues', 'BucklingEigenvalues']
        result_types = self.get_table_types()
        i = 0
        #nbreak = 0
        for result_type in result_types:
            result = getattr(self, result_type)
            for obj in itervalues(result):
                class_name = obj.__class__.__name__
                #print('working on %s' % class_name)
                obj.object_attributes()
                obj.object_methods()
                i += 1
                if class_name in no_sort2_classes:
                    try:
                        obj.build_dataframe()
                        obj.object_methods()
                    except:
                        self.log.error(obj)
                        self.log.error('build_dataframe is broken for %s' % class_name)
                        raise
                    continue
                if obj.is_sort2():
                    #self.log.warning(obj)
                    self.log.warning('build_dataframe is not supported for %s - SORT2' % class_name)
                    continue
                try:
                    obj.build_dataframe()
                except NotImplementedError:
                    self.log.warning(obj)
                    self.log.warning('build_dataframe is broken for %s' % class_name)
                    raise
                except:
                    self.log.error(obj)
                    self.log.error('build_dataframe is broken for %s' % class_name)
                    raise
                #if i >= nbreak:
                    #return

    def combine_results(self, combine=True):
        """
        we want the data to be in the same format and grouped by subcase, so
        we take

        .. code-block:: python

          stress = {
              # isubcase, analysis_code, sort_method, count, subtitle
              (1, 2, 1, 0, 'SUPERELEMENT 0') : result1,
              (1, 2, 1, 0, 'SUPERELEMENT 10') : result2,
              (1, 2, 1, 0, 'SUPERELEMENT 20') : result3,
              (2, 2, 1, 0, 'SUPERELEMENT 0') : result4,
          }
        and convert it to:

        .. code-block:: python

          stress = {
              1 : result1 + result2 + results3,
              2 : result4,
          }
        """
        self.combine = combine
        result_types = self.get_table_types()

        for result_type in result_types:
            result = getattr(self, result_type)
            case_keys = sorted(result.keys())
            unique_isubcases = []
            for case_key in case_keys:
                #print('case_key =', case_key)
                if isinstance(case_key, tuple):
                    isubcasei, analysis_codei, sort_methodi, counti, isubtitle = case_key
                    value = (analysis_codei, sort_methodi, counti, isubtitle)
                    if value not in self.subcase_key[isubcasei]:
                        #print('isubcase=%s value=%s' % (isubcasei, value))
                        self.subcase_key[isubcasei].append(value)
                else:
                    #print('combine - case_key =', case_keys)
                    break
        if not combine:
            subcase_key2 = {}
            for key, value in iteritems(self.subcase_key):
                subcase_key2[key] = value
            self.subcase_key = subcase_key2
            #print('self.subcase_key =', self.subcase_key)
            #print('skipping combine results')
            return
        del result, case_keys
        isubcases = np.unique(list(self.subcase_key.keys()))
        unique_isubcases = np.unique(isubcases)

        self.log.debug('combine_results')
        for result_type in result_types:
            result = getattr(self, result_type)
            if len(result) == 0:
                continue
            for isubcase in unique_isubcases:
                try:
                    keys = self.subcase_key[isubcase]
                except TypeError:
                    print('isubcase =', isubcase)
                    print('isubcases =', isubcases)
                    print('self.subcase_key =', self.subcase_key)
                    raise

                #print('keys = %s' % keys)
                key0 = tuple([isubcase] + list(keys[0]))

                isubcase, analysis_code, sort_code, count, subtitle = key0
                key1 = (isubcase, analysis_code, 1, count, subtitle)
                key2 = (isubcase, analysis_code, 2, count, subtitle)
                if len(keys) == 1:
                    if key0 not in result:
                        continue
                    # rename the case since we have only one tuple for the result
                    # key0 = tuple([isubcase] + list(key0))
                    result[isubcase] = result[key0]
                    del result[key0]
                elif len(keys) == 2 and key1 in keys and key2 in keys:
                    # continue
                    #print('key0 =', result_type, key0)
                    # res0 = result[key0]

                    isubcase, analysis_code, sort_code, count, subtitle = key0
                    if not (key1 in result and key2 in result):
                        if key1 in result:
                            res1 = result[key1]
                            self.log.info("res=%s has a single case; trivial" % res1.__class__.__name__)
                            result[isubcase] = result[key1]
                            #print('del key1=%s' % str(key1))
                            del result[key1]
                        elif key2 in result:
                            res2 = result[key2]
                            self.log.info("res=%s has a single case; trivial" % res2.__class__.__name__)
                            result[isubcase] = result[key2]
                            #print('del key2=%s' % str(key2))
                            del result[key2]
                        continue

                    res1 = result[key1]
                    if not hasattr(res1, 'combine'):
                        self.log.info("res=%s has no method combine" % res1.__class__.__name__)
                        continue
                    else:
                        self.log.info("res=%s has combine" % res1.__class__.__name__)
                    res2 = result[key2]
                    del result[key1]
                    del result[key2]
                    res1.combine(res2)
                    result[isubcase] = res1
                    # print('r[isubcase] =', result[isubcase])
                else:
                    #self.log.info("continue")
                    continue
            setattr(self, result_type, result)
        #print('subcase_key =', self.subcase_key)

        subcase_key2 = {}
        for result_type in result_types:
            if result_type == 'eigenvalues':
                continue
            result = getattr(self, result_type)
            case_keys = list(result.keys())
            try:
                case_keys = sorted(case_keys)  # TODO: causes DeprecationWarning
            except TypeError:
                self.log.error('result.keys() = %s' % case_keys)

            if len(result) == 0:
                continue
            for isubcase in unique_isubcases:
                if isubcase not in subcase_key2:
                    subcase_key2[isubcase] = []

            for isubcase in unique_isubcases:
                for case_key in case_keys:
                    #print('isubcase=%s case_key=%s' % (isubcase, case_key))
                    assert not isinstance(case_key, string_types), result_type
                    if isinstance(case_key, integer_types):
                        if isubcase == case_key and case_key not in subcase_key2[isubcase]:
                            subcase_key2[isubcase] = [isubcase]
                    else:
                        try:
                            subcasei = case_key[0]
                        except IndexError:
                            msg = 'case_key=%s; type(case_key)=%s; case_key[0] is not the subcase id' % (
                                case_key, type(case_key))
                            raise IndexError(msg)
                        #if not subcasei == isubcase:
                            #continue
                        if case_key not in subcase_key2[subcasei]:
                            subcase_key2[isubcase].append(case_key)
        self.subcase_key = subcase_key2
        #print('subcase_key = %s' % self.subcase_key)

    def print_subcase_key(self):
        self.log.info('---self.subcase_key---')
        for isubcase, keys in sorted(iteritems(self.subcase_key)):
            if len(keys) == 1:
                self.log.info('subcase_id=%s : keys=%s' % (isubcase, keys))
            else:
                self.log.info('subcase_id=%s' % isubcase)
                for key in keys:
                    self.log.info('  %s' % str(key))
        #self.log.info('subcase_key = %s' % self.subcase_key)

    def transform_displacements_to_global(self, i_transform, coords, xyz_cid0=None, debug=False):
        """
        Transforms the ``data`` of displacement-like results into the
        global coordinate system for those nodes with different output
        coordinate systems. Takes indicies and transformation matricies
        for nodes with their output in coordinate systems other than the
        global.

        Used in combination with ``BDF.get_displacement_index_transforms``
                          and/or ``BDF.get_displacement_index``

        Parameters
        ----------
        i_transform : dict{int cid : int ndarray}
            Dictionary from coordinate id to index of the nodes in
            ``BDF.point_ids`` that their output (`CD`) in that
            coordinate system.

        coords : dict{int cid :Coord()}
            Dictionary of coordinate id to the coordinate object
            Use this if CD is only rectangular
            Use this if CD is not rectangular

        xyz_cid0 : (nnodes+nspoints, 3) float ndarray
            the nodes in the global frame
            Don't use this if CD is only rectangular
            Use this if CD is not rectangular
        debug : bool; default=False
            developer debug

        .. warning:: only works if all nodes are included...
                     ``test_pynastrangui isat_tran.dat isat_tran.op2 -f nastran``
        """
        #output = {}
        disp_like_dicts = [
            # should NO results be transformed?
            #self.displacements_NO, self.velocities_NO, self.accelerations_NO,
            #self.spc_forces_NO, self.mpc_forces_NO,

            self.displacements,
            self.displacements_ATO, self.displacements_CRM, self.displacements_PSD, self.displacements_RMS,
            self.displacements_scaled,
            self.displacement_scaled_response_spectra_ABS,
            self.displacement_scaled_response_spectra_NRL,

            self.velocities,
            self.velocities_ATO, self.velocities_CRM, self.velocities_PSD, self.velocities_RMS,
            self.velocity_scaled_response_spectra_ABS,

            self.accelerations,
            self.accelerations_ATO, self.accelerations_CRM, self.accelerations_PSD, self.accelerations_RMS,
            self.acceleration_scaled_response_spectra_ABS,
            self.acceleration_scaled_response_spectra_NRL,

            self.eigenvectors,
            self.eigenvectors_RADCONS, self.eigenvectors_RADEFFM,
            self.eigenvectors_RADEATC, self.eigenvectors_ROUGV1,

            self.spc_forces, self.spc_forces_ATO, self.spc_forces_CRM, self.spc_forces_PSD, self.spc_forces_RMS,
            self.mpc_forces, self.mpc_forces_ATO, self.mpc_forces_CRM, self.mpc_forces_PSD, self.mpc_forces_RMS,

            self.applied_loads, self.load_vectors,
        ]
        for disp_like_dict in disp_like_dicts:
            if not disp_like_dict:
                continue
            #print('-----------')
            for subcase, result in iteritems(disp_like_dict):
                #print('result.name = ', result.class_name)
                data = result.data
                for cid, inode in iteritems(i_transform):
                    if cid in [-1, 0]:
                        continue
                    coord = coords[cid]
                    coord_type = coord.type
                    cid_transform = coord.beta()

                    is_global_cid = False
                    if np.diagonal(cid_transform).sum() == 3.:
                        is_global_cid = True

                    if debug:
                        self.log.debug('coord\n%s' % coord)
                        self.log.debug(cid_transform)
                        self.log.debug('inode = %s' % [str(val).rstrip('L') for val in inode.tolist()])
                        self.log.debug('data.shape = %s' % str(data.shape))
                        self.log.debug('len(inode) = %s' % len(inode))
                        assert np.array_equal(inode, np.unique(inode))
                    if coord_type in ['CORD2R', 'CORD1R']:
                        if is_global_cid:
                            self.log.debug('is_global_cid')
                            continue
                        self.log.debug('rectangular')


                        # isat_tran.op2
                        #  - nspoint = 4
                        #  - ngrid = 5379
                        #
                        #  - ntotal = 5383
                        #  data.shape = (101, 8, 6)
                        translation = data[:, inode, :3]
                        rotation = data[:, inode, 3:]
                        data[:, inode, :3] = translation.dot(cid_transform)
                        data[:, inode, 3:] = rotation.dot(cid_transform)
                    elif coord_type in ['CORD2C', 'CORD1C']:
                        #self.log.debug('cylindrical')
                        if xyz_cid0 is None:
                            msg = ('xyz_cid is required for cylindrical '
                                   'coordinate transforms')
                            raise RuntimeError(msg)
                        xyzi = xyz_cid0[inode, :]
                        rtz_cid = coord.xyz_to_coord_array(xyzi)
                        theta = rtz_cid[:, 1]
                        #self.log.debug('theta = %s' % list(theta))
                        for itime in range(data.shape[0]):
                            translation = data[itime, inode, :3]
                            rotation = data[itime, inode, 3:]
                            #theta_max1 = translation[:, 1].max()
                            #theta_max2 = rotation[:, 1].max()
                            #print('theta_max = ', max(theta_max1, theta_max2))

                            if 0:
                                # actually somewhat close
                                translation[:, 1] += theta
                                rotation[:, 1] += theta
                                translation = coord.coord_to_xyz_array(data[itime, inode, :3])
                                rotation = coord.coord_to_xyz_array(data[itime, inode, 3:])
                            elif 0:
                                # bad for spc (global_radial_cd)
                                translation[:, 1] += theta
                                rotation[:, 1] += theta
                                translation = coord.coord_to_xyz_array(translation)
                                rotation = coord.coord_to_xyz_array(rotation)
                            elif 0:
                                # very wrong...
                                #print(translation.shape)
                                translation[:, 1] += theta
                                rotation[:, 1] += theta
                            elif 1:
                                pass
                            else:
                                raise RuntimeError('no option selected...')

                            #if is_global_cid:
                                #data[itime, inode, :3] = translation
                                #data[itime, inode, 3:] = rotation
                                #print('is_global_cid')
                                #continue
                            data[itime, inode, :3] = translation.dot(cid_transform)
                            data[itime, inode, 3:] = rotation.dot(cid_transform)
                    elif coord_type in ['CORD2S', 'CORD1S']:
                        #print('spherical')
                        if xyz_cid0 is None:
                            msg = ('xyz_cid is required for spherical '
                                   'coordinate transforms')
                            raise RuntimeError(msg)
                        xyzi = xyz_cid0[inode, :]
                        rtp_cid = coord.xyz_to_coord_array(xyzi)
                        theta = rtp_cid[:, 1]
                        phi = rtp_cid[:, 2]
                        for itime in range(data.shape[0]):
                            translation = data[itime, inode, :3]
                            rotation = data[itime, inode, 3:]
                            if 0:
                                translation[:, 1] += theta
                                translation[:, 2] += phi
                                rotation[:, 1] += theta
                                rotation[:, 2] += phi
                            translation = coord.coord_to_xyz_array(translation)
                            rotation = coord.coord_to_xyz_array(rotation)
                            if is_global_cid:
                                data[itime, inode, :3] = translation
                                data[itime, inode, 3:] = rotation
                                continue
                            data[itime, inode, :3] = translation.dot(cid_transform)
                            data[itime, inode, 3:] = rotation.dot(cid_transform)
                    else:
                        raise RuntimeError(coord)
        return

    def transform_gpforce_to_global(self, nids_all, nids_transform, i_transform, coords, xyz_cid0=None):
        """
        Transforms the ``data`` of GPFORCE results into the
        global coordinate system for those nodes with different output
        coordinate systems. Takes indicies and transformation matricies
        for nodes with their output in coordinate systems other than the
        global.

        Used in combination with ``BDF.get_displacement_index_transforms``
                          and/or ``BDF.get_displacement_index``

        Parameters
        ----------
        nids_transform : dict{int cid : int ndarray nds}
            Dictionary from coordinate id to corresponding node ids.

        i_transform : dict{int cid : int ndarray}
            Dictionary from coordinate id to index of the nodes in
            ``BDF.point_ids`` that their output (`CD`) in that
            coordinate system.

        coords : dict{int cid :Coord()}
            Dictionary of coordinate id to the coordinate object
            Use this if CD is only rectangular
            Use this if CD is not rectangular
        """
        disp_like_dicts = [
            # TODO: causes test_op2_solid_shell_bar_01_gpforce_xyz to fail
            #       even though it should be uncommented
            self.grid_point_forces,
        ]
        for disp_like_dict in disp_like_dicts:
            if not disp_like_dict:
                continue
            self.log.debug('-----------')
            for subcase, result in iteritems(disp_like_dict):
                self.log.debug('result.name = %s' % result.class_name)
                data = result.data

                # inode_xyz :
                #    the indices of the nodes in the model grid point list
                for cid, inode_xyz in iteritems(i_transform):
                    self.log.debug('cid = %s' % cid)
                    if cid in [-1, 0]:
                        continue
                    coord = coords[cid]
                    coord_type = coord.type
                    cid_transform = coord.beta()

                    is_global_cid = False
                    if np.diagonal(cid_transform).sum() == 3.:
                        is_global_cid = True
                    nids = np.array(nids_transform[cid])

                    #from pyNastran.op2.tables.ogf_gridPointForces.ogf_objects import RealGridPointForcesArray
                    #result = RealGridPointForcesArray()
                    if result.is_unique: # TODO: doesn't support preload
                        #self.node_element = zeros((self.ntimes, self.ntotal, 2), dtype='int32')
                        nids_all_gp = result.node_element[0, :, 0]

                        self.log.debug('nids_all_gp = %s' % list(nids_all_gp))
                        self.log.debug('nids = %s' % list(nids))

                        # the indices of the grid points that we're transforming
                        inode_gp = np.where(np.in1d(nids_all_gp, nids))[0]
                        self.log.debug('inode_gp = %s' % list(inode_gp))
                        nids_gp = nids_all_gp[inode_gp]
                        self.log.debug('nids_gp = %s' % list(nids_gp))
                        assert np.array_equal(np.unique(nids_gp), np.unique(nids)), 'nids_gp=%s nids=%s' % (nids_gp, nids)
                        self.log.debug('---------')
                        # the transformation index to go from xyz to the grid point forces
                        inode_gp_xyz = np.searchsorted(nids_all, nids_all_gp)
                        self.log.debug('nids_all = %s' % list(nids_all))
                        self.log.debug('nids_all_gp = %s' % list(nids_all_gp))
                        self.log.debug('inode_xyz = %s' % list(inode_xyz))
                        self.log.debug('inode_gp_xyz = %s' % list(inode_gp_xyz))
                        sys.stdout.flush()
                        assert len(inode_gp_xyz) == len(nids_all_gp), len(nids_all_gp)

                    else:
                        raise NotImplementedError(result)

                    if coord_type in ['CORD2R', 'CORD1R']:
                        if is_global_cid:
                            continue
                        #print('coord\n', coord)
                        #print(cid_transform)
                        #print('inode = %s' % inode)
                        #print('rectangular')
                        translation = data[:, inode_gp, :3]
                        rotation = data[:, inode_gp, 3:]
                        data[:, inode_gp, :3] = translation.dot(cid_transform)
                        data[:, inode_gp, 3:] = rotation.dot(cid_transform)
                    elif coord_type in ['CORD2C', 'CORD1C']:
                        #print('cylindrical')
                        if xyz_cid0 is None:
                            msg = ('xyz_cid is required for cylindrical '
                                   'coordinate transforms')
                            raise RuntimeError(msg)
                        xyzi = xyz_cid0[inode_xyz, :]
                        rtz_cid = coord.xyz_to_coord_array(xyzi)
                        theta_xyz = rtz_cid[inode_xyz, 1]
                        theta = rtz_cid[inode_gp_xyz, 1]
                        self.log.debug('coord\n%s' % coord)
                        self.log.debug(cid_transform)
                        #print('theta_xyz = %s' % list(theta_xyz))
                        #print('theta     = %s' % list(theta))

                        for itime in range(data.shape[0]):
                            #inode = np.where(np.in1d(nids_all, 2))[0]
                            #print('start', data[itime, inode_gp, :3])
                            translation = data[itime, inode_gp, :3]
                            rotation = data[itime, inode_gp, 3:]
                            if 0:
                                # horrible
                                translation = coord.coord_to_xyz_array(data[itime, inode_gp, :3])
                                rotation = coord.coord_to_xyz_array(data[itime, inode_gp, 3:])
                                data[itime, inode_gp, :3] = translation.dot(cid_transform)
                                data[itime, inode_gp, 3:] = rotation.dot(cid_transform)
                            elif 0:
                                # expectedly horrible
                                translation[:, 1] += theta
                                rotation[:, 1] += theta
                                translation = coord.coord_to_xyz_array(data[itime, inode_gp, :3])
                                rotation = coord.coord_to_xyz_array(data[itime, inode_gp, 3:])
                                data[itime, inode_gp, :3] = translation.dot(cid_transform)
                                data[itime, inode_gp, 3:] = rotation.dot(cid_transform)
                            elif 0:
                                # actually not bad...
                                translation = coord.xyz_to_coord_array(translation)
                                rotation = coord.xyz_to_coord_array(rotation)
                                translation[:, 1] += theta
                                rotation[:, 1] += theta
                                translation = coord.coord_to_xyz_array(translation)
                                rotation = coord.coord_to_xyz_array(rotation)
                                data[itime, inode_gp, :3] = translation.dot(cid_transform)
                                data[itime, inode_gp, 3:] = rotation.dot(cid_transform)
                            elif 0:
                                # not that bad, worse than previous
                                translation = coord.xyz_to_coord_array(translation)
                                rotation = coord.xyz_to_coord_array(rotation)
                                translation[:, 1] += theta
                                rotation[:, 1] += theta
                                translation = coord.coord_to_xyz_array(translation)
                                rotation = coord.coord_to_xyz_array(rotation)
                                data[itime, inode_gp, :3] = translation.dot(cid_transform.T)
                                data[itime, inode_gp, 3:] = rotation.dot(cid_transform.T)
                            elif 1:
                                # doesn't work...actually pretty close
                                data[itime, inode_gp, :3] = translation.dot(cid_transform)
                                data[itime, inode_gp, 3:] = rotation.dot(cid_transform)
                            elif 0:
                                # very, very close
                                data[itime, inode_gp, :3] = translation.dot(cid_transform.T)
                                data[itime, inode_gp, 3:] = rotation.dot(cid_transform.T)
                            elif 0:
                                # is this just the same as one of the previous?
                                data[itime, inode_gp, :3] = cid_transform.T.dot(translation.T).T
                                data[itime, inode_gp, 3:] = cid_transform.T.dot(rotation.T).T
                            else:
                                raise RuntimeError('no option selected...')

                            #if is_global_cid:
                                #data[itime, inode, :3] = translation
                                #data[itime, inode, 3:] = rotation
                                #continue
                            #data[itime, inode_gp, :3] = translation.dot(cid_transform)
                            #data[itime, inode_gp, 3:] = rotation.dot(cid_transform)
                            #print('end', data[itime, inode_gp, :3])

                    elif coord_type in ['CORD2S', 'CORD1S']:
                        self.log.debug('spherical')
                        if xyz_cid0 is None:
                            msg = ('xyz_cid is required for spherical '
                                   'coordinate transforms')
                            raise RuntimeError(msg)
                        xyzi = xyz_cid0[inode, :]
                        rtp_cid = coord.xyz_to_coord_array(xyzi)
                        theta = rtp_cid[:, 1]
                        phi = rtp_cid[:, 2]
                        for itime in range(data.shape[0]):
                            translation = data[itime, inode, :3]
                            rotation = data[itime, inode, 3:]
                            #if 0:
                                #translation[:, 1] += theta
                                #translation[:, 2] += phi
                                #rotation[:, 1] += theta
                                #rotation[:, 2] += phi
                            translation = coord.coord_to_xyz_array(data[itime, inode, :3])
                            rotation = coord.coord_to_xyz_array(data[itime, inode, 3:])
                            #if is_global_cid:
                                #data[itime, inode, :3] = translation
                                #data[itime, inode, 3:] = rotation
                                #continue
                            data[itime, inode, :3] = translation.dot(cid_transform)
                            data[itime, inode, 3:] = rotation.dot(cid_transform)
                    else:
                        raise RuntimeError(coord)
        self.log.debug('-----------')
        return

def main():  # pragma: no cover
    """testing new ideas"""
    import pyNastran
    pkg_path = pyNastran.__path__[0]

    # we don't want the variable name to get picked up by the class
    _op2_filename = os.path.join(pkg_path, '..', 'models',
                                 'sol_101_elements', 'solid_shell_bar.op2')

    model = OP2()
    model.set_as_vectorized(ask=False)
    model.read_op2(_op2_filename)
    isubcase = 1

    # ============displacement================
    # same for velocity/acceleration/mpc forces/spc forces/applied load
    # maybe not temperature because it's only 1 result...
    displacement = model.displacements[isubcase]
    data = displacement.data
    grid_type = model.displacements[isubcase].grid_type

    # t1, t2, t3, r1, r2, r3
    assert displacement.ntimes == 1, displacement.ntimes

    # get all the nodes for element 1
    inode1 = data.getNodeIndex([1])    # [itransient, node, t1/t2]
    datai = data[0, inode1, :]
    grid_typei = grid_type[inode1]

    # ============solid stress=================
    # same for solid strain
    solid_stress = model.ctetra_stress[isubcase]
    data = solid_stress.data
    cid = model.ctetra_stress[isubcase].cid

    # oxx, oyy, ozz, txy, tyz, txz
    assert solid_stress.ntimes == 1, solid_stress.ntimes

    # get the indexs for cid, element 1
    ielem1 = solid_stress.getElementPropertiesIndex([1])  # element-specific properties
    datai = cid[ielem1]

    # get all the nodes for element 1
    ielem1 = solid_stress.getElementIndex([1])
    # [itransient, elem*node, oxx/oyy, etc.]
    datai = data[0, ielem1, :]

    # get all the nodes for element 1
    ielem1 = solid_stress.getElementIndex([1])
    # [itransient, elem*node, oxx/oyy, etc.]
    datai = data[0, ielem1, :]

    # get all the nodes for element 4 and 5
    ielem45 = solid_stress.getElementIndex([[1, 4, 5]])
    datai = data[0, ielem45, :]

    # get the index for element 1, centroid
    ielem1_centroid = solid_stress.getElementNodeIndex([[1, 0]])
    datai = data[0, ielem1_centroid, :]

    # get the index for element 1, node 1
    ielem1_node1 = solid_stress.getElementNodeIndex([[1, 1]])
    datai = data[0, ielem1_node1, :]

    # get the index for element 1, node 1 and element 1, node 2
    ielem1_node12 = solid_stress.getElementNodeIndex([[1, 1],
                                                      [1, 2],])
    datai = data[0, ielem1_node12, :]

    # ============plate stress=================
    # same for plate strain
    plate_stress = model.cquad4_stress[isubcase]
    data = plate_stress.data

    # oxx, oyy, ozz, txy, tyz, txz
    assert plate_stress.ntimes == 1, plate_stress.ntimes

    # get all the nodes for element 1
    ielem1 = plate_stress.getElementIndex([1])
    # [itransient, elem*node, oxx/oyy, etc.]
    datai = plate_stress[0, ielem1, :]

    # ========composite plate stress============
    # same for plate strain
    comp_plate_stress = model.cquad4_composite_stress[isubcase]
    data = comp_plate_stress.data
    cid = model.cquad4_stress[isubcase].cid

    # get the indexs for cid, element 1
    ielem1 = comp_plate_stress.getElementPropertiesIndex([1])  # element-specific properties
    datai = cid[ielem1]

    # oxx, oyy, ozz, txy, tyz, txz
    assert comp_plate_stress.ntimes == 1, comp_plate_stress.ntimes

    # get all the nodes/layers for element 1
    ielem1 = comp_plate_stress.getElementIndex([1])
    # [itransient, elem*node*layer, oxx/oyy, etc.]
    datai = data[0, ielem1, :]

    # get all the layers for element 1, centroid, and all the layers
    ielem1_centroid = solid_stress.getElementNodeIndex([[1, 0]])
    datai = data[0, ielem1_centroid, :]

    # get the index for element 1, centroid, layer 0
    ielem1_centroid_layer = solid_stress.getElementNodeLayerIndex([[1, 0, 0]])
    datai = data[0, ielem1_centroid_layer, :]

    # get the index for element 1, layer 0, and all the nodes
    ielem1_layer = solid_stress.getElementLayerIndex([[1, 0]])
    datai = data[0, ielem1_layer, :]


if __name__ == '__main__':  # pragma: no cover
    main()
