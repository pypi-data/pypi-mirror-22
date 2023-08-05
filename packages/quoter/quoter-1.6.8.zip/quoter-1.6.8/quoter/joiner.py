"""
Module to assist in the super-common operation of
joining values in sequences into strings.
"""

import re
from options import Options
from .util import *
from .quoter import Quoter
from .styleset import *
import six


class Joiner(Quoter):

    """
    A type of Quoter that deals with sequences.
    """

    options = Quoter.options.add(
        sep=', ',      # separator between items
        twosep=None,   # separator between items if only two
        lastsep=None,  # separator between penultimate and final item
        quoter=None,   # quoter for individual items
        endcaps=None,  # quoter for entire joined sequence
    )

    def __init__(self, **kwargs):
        """
        Create a Joiner
        """
        Quoter.__init__(self)
        opts = self.options = self.__class__.options.push(kwargs)


    def __call__(self, seq, **kwargs):
        """
        Join the items of a sequence into a string. Implicitly stringifies any
        not-string values. Allows specification of the separator between items (and
        a special case for the last separator). Allows each item to be optionally
        quoted by a function, and the entire list to be optionally quoted with an
        endcaps function. A separate suffix and prefix may also be provdied.
        """
        opts = self.options.push(kwargs)

        def prep(v):
               """
               Prepare an item by stringifying and optionally quoting it.
               """
               s = stringify(v)
               return opts.quoter(s) if opts.quoter else s

        seqlist = list(seq)
        length = len(seqlist)
        if length == 0:
            core = ''
        elif length == 1:
            core = prep(seqlist[0])
        elif length == 2 and opts.twosep:
            sep = opts.twosep if opts.twosep is not None else opts.sep
            core = sep.join(prep(v) for v in seqlist)
        else:
            start = [ prep(v) for v in seqlist[:-1] ]
            final = prep(seqlist[-1])
            if opts.lastsep is None:
                opts.lastsep = opts.sep
            core = opts.lastsep.join([ opts.sep.join(start), final])
        pstr, mstr = self._whitespace(opts)
        capped = opts.endcaps(core) if opts.endcaps else core
        payload = [mstr, blanknone(opts.prefix), pstr, capped, pstr,
                         blanknone(opts.suffix), mstr]
        return self._output(payload, opts)

    # TODO: Determine if it makes any sense for Joiners to take *args


join = StyleSet(
        factory = Joiner,
        instant = False,
        immediate = Joiner(),
        promote = 'but clone')

# specializations

# A and B. A, B, and C.
and_join = join.and_join = join.but(sep=', ', twosep=' and ', lastsep=', and ')

# A or B. A, B, or C.
or_join = join.or_join = join.but(sep=', ', twosep=' or ', lastsep=', or ')

joinlines = join.joinlines = join.lines = join.but(sep="\n", suffix="\n")

concat = join.concat = join.but(sep='', twosep='', lastsep='')

# TODO: Rationalize with respect to more sophisticated quoter args
# TODO: Add padding and margin, like quoter


items_options = Options(
    sep="\n",  # separator between items
    fmt="{key}: {value!r}",
    header=None,   # header for entire list
    footer=None    # footer for entire list
)


def iter_items(items):
    if hasattr(items, 'items'):  # dict or mapping
        for k, v in items.items():
            yield k, v
    else:
        for k, v in enumerate(items):
            yield k, v


def items(seq, **kwargs):
    opts = items_options.push(kwargs)

    formatted_items = [ opts.fmt.format(key=k, value=v) for k,v in iter_items(seq) ]
    items_str = opts.sep.join(formatted_items)
    if opts.header or opts.footer:
        parts = []
        if opts.header:
            parts.extend([opts.header, opts.sep])
        parts.append(items_str)
        if opts.footer:
            parts.extend([opts.sep, opts.footer])
        items_str = ''.join(parts)
    return items_str

# TODO: needs to be moved into object struture, like quoter
