import math


class Bearing(object):
    '''
    An angle between 0 and 360 degrees

    Examples:

    >>> Bearing(100)
    <Bearing (100.00 degrees clockwise from north) at 0x7f25e22b3710>
    >>> Bearing(100) + Bearing(100)
    <Bearing (200.00 degrees clockwise from north) at 0x7f25e22b3940>
    >>> Bearing(100) + Bearing(300)
    <Bearing (40.00 degrees clockwise from north) at 0x7f25e22b37b8>
    >>> Bearing(0) - Bearing(100)
    <Bearing (260.00 degrees clockwise from north) at 0x7f25e22b3940>
    >>> import math
    >>> Bearing.from_radians(math.pi)
    <Bearing (180.00 degrees clockwise from north) at 0x7f25e22b3828>
    >>> int(Bearing(120.4))
    120
    >>> float(Bearing(120.4))
    120.4
    '''

    def __init__(self, degrees):
        self._degrees = float(degrees % 360)

    @classmethod
    def from_radians(cls, radians):
        return cls(math.degrees(radians))

    @property
    def degrees(self):
        return self._degrees

    def delta(self, other):
        '''
        Return the error between this and another bearing. This will be an
        angle in degrees, positive or negative depending on the direction of
        the error.
        
            self   other
              \      /
               \    /
                \__/
                 \/ <- angle will be +ve

            other   self
              \      /
               \    /
                \__/
                 \/ <- angle will be -ve        

        :param other: bearing to compare to
        :type other: Bearing

        :returns: error angle
        :rtype: float
        '''
        difference = float(other) - float(self)
        while difference < -180:
            difference += 360
        while difference > 180:
            difference -= 360
        return difference

    @property
    def radians(self):
        return math.radians(self.degrees)

    def __float__(self):
        return self._degrees

    def __add__(self, n):
        return Bearing(float(self) + float(n))

    def __radd__(self, n):
        return Bearing(float(self) + float(n))

    def __sub__(self, n):
        return Bearing(float(self) - float(n))

    def __rsub__(self, n):
        return Bearing(float(n) - float(self))

    def __str__(self):
        return '{0:0.2f} degrees clockwise from north'.format(self.degrees)

    def __repr__(self):
        return '<{0}.{1} ({2}) at {3}>'.format(
            self.__module__, type(self).__name__, str(self), hex(id(self)))

    def __int__(self):
        return int(self._degrees)

    def __neg__(self):
        return Bearing(-float(self))

    def __abs__(self):
        return Bearing(abs(float(self)))

    def __lt__(self, other):
        return self._degrees < float(other)

    def __lt__(self, other):
        return self._degrees < float(other)

    def __gt__(self, other):
        return self._degrees > float(other)

    def __le__(self, other):
        return self._degrees <= float(other)

    def __ge__(self, other):
        return self._degrees >= float(other)
