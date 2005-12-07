
#A place for code to be called from C-code
#  that implements more complicated stuff.

from multiarray import _flagdict, dtypedescr

_defflags = _flagdict.keys()

_setable = ['WRITEABLE', 'NOTSWAPPED', 'SWAPPED', 'UPDATEIFCOPY', 'ALIGNED',
            'W','N','S','U','A']
_setable2 = ['write','swap','swap','uic','align']*2
_firstltr = {'W':'WRITEABLE',
             'N':'NOTSWAPPED',
             'A':'ALIGNED',
             'C':'CONTIGUOUS',
             'F':'FORTRAN',
             'O':'OWNDATA',
             'U':'UPDATEIFCOPY'}

_anum = _flagdict['ALIGNED']
_nnum = _flagdict['NOTSWAPPED']
_wnum = _flagdict['WRITEABLE']
_cnum = _flagdict['CONTIGUOUS']
_fnum = _flagdict['FORTRAN']
_unum = _flagdict['UPDATEIFCOPY']
_onum = _flagdict['OWNDATA']

class flagsobj(dict):
    def __init__(self, arr, flags, scalar):
        self._arr = arr
        self._flagnum = flags
        for k in _defflags:
            num = _flagdict[k]
            dict.__setitem__(self, k, flags & num == num)
        self.scalar = scalar

    def __getitem__(self, key):
        if not isinstance(key, str):
            raise KeyError, "Unknown flag %s" % key
        if len(key) == 1:
            try:
                return dict.__getitem__(self, _firstltr[key])
            except:
                if (key == 'B'):
                    num = _anum + _nnum + _wnum
                    return self._flagnum & num == num
                elif (key == 'S'):
                    return not (self._flagnum & _nnum == _nnum)
        else:
            try:
                return dict.__getitem__(self, key)
            except: # special cases
                if (key == 'FNC'):
                    return (self._flagnum & _fnum == _fnum) and not \
                           (self._flagnum & _cnum == _cnum)
	        if (key == 'FORC'):
		    return (self._flagnum & _fnum == _fnum) or \
                           (self._flagnum & _cnum == _cnum)
                if (key == 'SWAPPED'):
                    return not (self._flagnum & _nnum == _nnum)
                if (key == 'BEHAVED'):
                    num = _anum + _nnum + _wnum
                    return self._flagnum & num == num
                if (key in ['BEHAVED_RO', 'BRO']):
                    num = _anum + _nnum
                    return self._flagnum & num == num
                if (key in ['CARRAY','CA']):
                    num = _anum + _nnum + _wnum + _cnum
                    return self._flagnum & num == num
                if (key in ['FARRAY','FA']):
                    num = _anum + _nnum + _wnum + _fnum
                    return (self._flagnum & num == num) and not \
                           (self._flagnum & _cnum == _cnum)
        raise KeyError, "Unknown flag: %s" % key
        
    def __setitem__(self, item, val):
        if self.scalar:
            raise ValueError, "Cannot set flags on array scalars."
        val = not not val  # convert to boolean
        if item not in _setable:
            raise KeyError, "Cannot set flag", item
        dict.__setitem__(self, item, val) # Does this matter?

        kwds = {}
        for k, name in enumerate(_setable):
            if item == name:
                kwds[_setable2[k]] = val
        if (item == 'NOTSWAPPED' or item == 'N'):
            kwds['swap'] = not val

        # now actually update array flags
        self._arr.setflags(**kwds)
        

    def get_fnc(self):
        fl = self._flagnum
        return (fl & _fnum == _fnum) and \
               not (fl & _cnum == _cnum)

    def get_forc(self):
        fl = self._flagnum
        return (fl & _cnum == _cnum) or \
               (fl & _fnum == _fnum)

    def get_behaved(self):
        fl = self._flagnum
        return (fl & _anum == _anum) and \
               (fl & _nnum == _nnum) and \
               (fl & _wnum == _wnum)

    def get_behaved_ro(self):
        fl = self._flagnum
        return (fl & _anum == _anum) and \
               (fl & _nnum == _nnum)

    def get_carray(self):
        fl = self._flagnum
        return (fl & _anum == _anum) and \
               (fl & _nnum == _nnum) and \
               (fl & _wnum == _wnum) and \
               (fl & _cnum == _cnum)

    def get_farray(self):
        fl = self._flagnum
        return (fl & _anum == _anum) and \
               (fl & _nnum == _nnum) and \
               (fl & _wnum == _wnum) and \
               (fl & _fnum == _fnum) and \
               not (fl & _cnum == _cnum)

    def get_contiguous(self):
        return (self._flagnum & _cnum == _cnum)

    def get_fortran(self):
        return (self._flagnum & _fnum == _fnum)

    def get_updateifcopy(self):
        return (self._flagnum & _unum == _unum)

    def get_owndata(self):
        return (self._flagnum & _onum == _onum)

    def get_aligned(self):
        return (self._flagnum & _anum == _anum)

    def get_notswapped(self):
        return (self._flagnum & _nnum == _nnum)

    def get_swapped(self):
        return not (self._flagnum & _nnum == _nnum)

    def get_writeable(self):
        return (self._flagnum & _wnum == _wnum)

    def set_writeable(self, val):
        val = not not val
        self._arr.setflags(write=val)

    def set_aligned(self, val):
        val = not not val
        self._arr.setflags(align=val)

    def set_updateifcopy(self, val):
        val = not not val
        self._arr.setflags(uic=val)

    def set_notswapped(self, val):
        val = not val
        self._arr.setflags(swap=val)

    def set_swapped(self, val):
        val = not not val
        self._arr.setflags(swap=val)

    contiguous = property(get_contiguous, None, "")
    fortran = property(get_fortran, None, "")
    updateifcopy = property(get_updateifcopy, set_updateifcopy, "")
    owndata = property(get_owndata, None, "")
    aligned = property(get_aligned, set_aligned, "")
    notswapped = property(get_notswapped, set_notswapped, "")
    swapped = property(get_swapped, set_swapped, "")
    writeable = property(get_writeable, set_writeable, "")

    fnc = property(get_fnc, None, "")
    forc = property(get_forc, None, "")
    behaved = property(get_behaved, None, "")
    behaved_ro = property(get_behaved_ro, None, "")
    carray = property(get_carray, None, "")
    farray = property(get_farray, None, "")
    


# make sure the tuple entries are PyArray_Descr
#	   or convert them
#
# make sure offsets are all interpretable 
#	   as positive integers and
#	   convert them to positive integers if so 
#
#
# return totalsize from last offset and size

# Called in PyArray_DescrConverter function when
#  a dictionary without "names" and "formats"
#  fields is used as a data-type descriptor.
def _usefields(adict):
    allfields = []
    names = []
    formats = []
    offsets = []
    titles = []
    fnames = adict.keys()
    for fname in fnames:
        obj = adict[fname]
        n = len(obj)
        if not isinstance(obj, tuple) or n not in [2,3]:
            raise ValueError, "entry not a 2- or 3- tuple"
        if (n > 2) and (obj[2] == fname):
            continue
        num = int(obj[1])
        if (num < 0):
            raise ValueError, "invalid offset."
        format = dtypedescr(obj[0])
        if (format.itemsize == 0):
            raise ValueError, "all itemsizes must be fixed."
        if (n > 2):
            title = obj[2]
        else:
            title = None
        allfields.append((fname, format, num, title))
    # sort by offsets
    allfields.sort(lambda x,y: cmp(x[2],y[2]))
    return dtypedescr({"names" : [x[0] for x in allfields],
                       "formats" : [x[1] for x in allfields],
                       "offsets" : [x[2] for x in allfields],
                       "titles" : [x[3] for x in allfields]})


# construct an array_protocol descriptor list
#  from the fields attribute of a descriptor
# This calls itself recursively through the descriptor
#  attribute lookup, but should eventually hit
#  a descriptor that has no fields and returns
#  a simple typestring instead. 

def _array_descr(descriptor):
    fields = descriptor.fields
    if fields is None:
        return descriptor.arrtypestr

    #get ordered list of fields with names
    ordered_fields = fields.items()
    # remove duplicates
    new = {}
    for item in ordered_fields:
        # We don't want to include redundant or non-string
        #  entries
        if not isinstance(item[0],str) or (len(item[1]) > 2 \
                                           and item[0] == item[1][2]):
            continue
        new[item[1]] = item[0]
    ordered_fields = [x[0] + (x[1],) for x in new.items()]
    #sort the list on the offset
    ordered_fields.sort(lambda x,y : cmp(x[1],y[1]))

    result = []
    offset = 0
    for field in ordered_fields:
        if field[1] > offset:
            result.append(('','|V%d' % (field[1]-offset)))
        if len(field) > 3:
            name = (field[2],field[3])
        else:
            name = field[2]
        if field[0].subdescr:
            tup = (name, _array_descr(field[0].subdescr[0]),
                   field[0].subdescr[1])
        else:
            tup = (name, _array_descr(field[0]))
        offset += field[0].itemsize
        result.append(tup)

    return result
