def encode(*vals):
    """
    Compute the morton encoding for the data passed into the function.

    Parameters:
        This function can take any number of values, and it is assumed that 
        the arguments are all non-negative integers.

    Returns:
        Returns the morton encoding of the values.
    """
    result = 0

    # make a list of variables for us to manipualte
    vals = list(vals)
    n = len(vals)

    # we start at the left most bit
    bit = 0x01

    # keep going until we run out of 1s
    while sum(vals) != 0:
        for i in range(n):
            #copy the bit
            if vals[i] & 0x1 != 0:
                result = result | bit

            # adjust value and the bit to toggle
            vals[i] = vals[i] >> 1
            bit = bit << 1
    
    return result


def decode(m, n):
    """
    Extract integers from a morton encoding.
    Parameters:
        m - The morton encoded set
        n - The number of integers present
    Returns:
        The list of decoded integers
    """
    # amount to shift by
    shift = 0
    
    # construct the list
    l = [0] * n

    # continue until we run out of bits
    while m > 0:
        for i in range(n):
            l[i] = l[i] | ((m & 1) << shift)
            m = m >> 1
        shift += 1
    
    return l