from collections import Iterable
import six
from .exc import IntervalException


strip = lambda a: a.strip()


class IntervalParser(object):
    def parse_object(self, obj):
        return obj.lower, obj.upper, obj.lower_inc, obj.upper_inc

    def parse_string(self, value):
        if ',' not in value:
            return self.parse_hyphen_range(value)
        else:
            return self.parse_bounded_range(value)

    def parse_sequence(self, seq):
        lower, upper = seq
        if isinstance(seq, tuple):
            return lower, upper, False, False
        else:
            return lower, upper, True, True

    def parse_single_value(self, value):
        return value, value, True, True

    def parse_bounded_range(self, value):
        values = value.strip()[1:-1].split(',')
        try:
            lower, upper = map(strip, values)
        except ValueError as e:
            raise IntervalException(e.message)

        return lower, upper, value[0] == '[', value[-1] == ']'

    def parse_hyphen_range(self, value):
        values = value.split('-')
        if len(values) == 1:
            lower = upper = value.strip()
        else:
            try:
                lower, upper = map(strip, values)
            except ValueError as e:
                raise IntervalException(str(e))
        return lower, upper, True, True

    def __call__(self, bounds, lower_inc, upper_inc):
        if isinstance(bounds, six.string_types):
            return self.parse_string(bounds)
        elif isinstance(bounds, Iterable):
            return self.parse_sequence(bounds)
        elif hasattr(bounds, 'lower') and hasattr(bounds, 'upper'):
            return self.parse_object(bounds)
        else:
            return self.parse_single_value(bounds)
