from typing import Iterable, Callable, Tuple
import numpy as np

__all__ = ['table', 'group']

class _table_state:
    pass

class _empty_iterator:
    def __iter__(self):
        return self
    def __next__(self):
        raise StopIteration

class _symbol_iterator:
    def __init__(self, iterable, begin, end, step):
        self._iterable = iterable
        self._iterator = iter(np.arange(begin, end, step))
    
    def __iter__(self):
        return self
    
    def __next__(self):
        value = next(self._iterator)
        setattr(self._iterable._state, self._iterable.symbol, value)
        return value

class _symbol_iterable:
    """\
    helper iterator for single entry.
    """

    def __init__(self, state:_table_state, args):
        self._state = state
        self._symbol = args[0]
        if len(args) == 2:
            self._begin = 0
            self._end = args[1]
            self._step = 1
        elif len(args) == 3:
            self._begin = args[1]
            self._end = args[2]
            self._step = 1
        elif len(args) == 4:
            self._begin = args[1]
            self._end = args[2]
            self._step = args[3]
        else:
            raise ValueError(f'invalid argument: {args}, the length is most be 4.')
    
    def _expr_to_number(self, expr):
        if isinstance(expr, Callable):
            return expr(self._state)
        else:
            return expr

    @property
    def symbol(self):
        return self._symbol
    
    @property
    def begin(self):
        return self._expr_to_number(self._begin)

    @property
    def end(self):
        return self._expr_to_number(self._end)

    @property
    def step(self):
        return self._expr_to_number(self._step)

    def __iter__(self):
        begin = self.begin
        end = self.end
        step = self.step
        setattr(self._state, self._symbol, begin)
        return _symbol_iterator(self, begin, end, step)


class table_iterator:
    def __init__(self, *args):
        self._iterables = []
        self._iterators = []
        self._current = []
        self._state = _table_state()

        # initialize the iterators
        for arg in args:
            if isinstance(arg, Iterable):
                if isinstance(arg, str):
                    self._iterables.append(arg)
                else:
                    assert len(arg)>=2, f'need at least 2 elements in argument or is string: {arg}'
                if isinstance(arg[0],str):
                    self._iterables.append(_symbol_iterable(self._state, arg))
                else:
                    self._iterables.append(np.arange(*arg))
            else:
                self._iterables.append(np.arange(arg))

        # initialize the iterators
        self._iterators = [iter(iterable) for iterable in self._iterables]

        # initialize the current
        try:
            # leave the last iterator untouched
            self._current = [next(iterator) for iterator in self._iterators[:-1]]
            self._current.append(None)

            self._n = len(args)
            self._ptr = len(args) - 1

        except StopIteration:
            # invalid arguments, result in empty iterator
            self._iterators = [_empty_iterator()]
            self._current = [None]
            self._n = 1
            self._ptr = 0
            return


    def __iter__(self):
        return self
    
    def _next(self):
        try:
            self._current[self._ptr] = next(self._iterators[self._ptr])
            return True
        except StopIteration:
            return False

    def _continue(self) -> bool:
        """jump to next element.

        Returns:
            bool: return ``True`` if continue successfully or ``False`` if iteration completes.
        """
        try:
            self._current[self._ptr] = next(self._iterators[self._ptr])
            return True
        except StopIteration:
            self._ptr -= 1
            while (self._ptr >=0) and (not self._next()):
                self._ptr -= 1
            if self._ptr < 0:
                return False
            else:
                try:
                    for i in range(self._ptr+1, self._n):
                        self._iterators[i] = iter(self._iterables[i])
                        self._current[i] = next(self._iterators[i])
                    self._ptr = i
                    return True
                except StopIteration:
                    return False
    
    def break_(self,level=-1) ->bool:
        """break at ``level``-th loop.

        Args:
            level (int, optional): Defaults to -1.

        Returns:
            bool: return ``True`` if break successfully or ``False`` if iteration completes.
        """
        assert level<self._n and level>-self._n, f'level must be in range [-{self._n}, {self._n})'
        if level >=0:
            level = level - self._n
        self._ptr += level
        while (self._ptr >=0) and (not self._next()):
            self._ptr -= 1
        if self._ptr < 0:
            return False
        else:
            try:
                for i in range(self._ptr+1, self._n):
                    self._iterators[i] = iter(self._iterables[i])
                    # leave the last iterator untouched
                    if i != self._n -1:
                        self._current[i] = next(self._iterators[i])
                self._ptr = i
                return True
            except StopIteration:
                return False

    def __next__(self):
        if self._continue():
            return tuple(self._current)
        else:
            raise StopIteration



class table:
    def __init__(self, *args):
        self.args = args

    def __iter__(self):
        return table_iterator(*self.args)

def _group_impl(items, level, max_level):
    if level == max_level:
        return items

    else:
        if not isinstance(items, Iterable):
            raise ValueError('dim too high.')
        else:
            ret = []
            part = []
            iterator = iter(items)
            try:
                item = next(iterator)
                while True:
                    try:
                        x = item[level]
                    except:
                        raise ValueError('dim too high.')
                    part.append(item)
                    while True:
                            item =next(iterator)
                            if x==item[level]:
                                part.append(item)
                                continue
                            else:
                                ret.append(_group_impl(part, level+1, max_level))
                                part = []
                                break
            except StopIteration:
                if len(part) >0:
                    ret.append(_group_impl(part, level+1, max_level))
                return ret


def group(items, *, dim=1):
    return _group_impl(items, 0, dim-1)

