
def NormalizeRange(OrginalSet, MapToRange=list(range(1,10))):
    ''' Algorithm Breakdown
    variables:
        -   X:  orginal set of numbers
        -   Y:  map to set
        -   A:  orginal range min
        -   B:  orginal range max
        -   C:  map to range min
        -   D:  map to rnage max
        -   x:  number in orginal set X
        -   y:  x normailzed value
    '''
    # Assign variable
    X = OrginalSet
    Y = MapToRange
    NormalizedRange = []
    A, B = min(X), max(X)
    C, D = min(Y), max(Y)

    NormalizedRange = [(C + (((x-A) * (D - C)) / (B - A))) for x in X]
    return NormalizedRange

def NormalizeNumber(TargetNumber, Min, Max, MapToRange=list(range(1,10))):
    ''' Algorithm Breakdown
      variables:
          -   X:  orginal set of numbers
          -   Y:  map to set
          -   A:  orginal range min
          -   B:  orginal range max
          -   C:  map to range min
          -   D:  map to range max
          -   x:  number in orginal set X
          -   y:  x normailzed value
      '''
    # Assign variable
    x = TargetNumber
    Y = MapToRange
    NormalizedRange = []
    A, B = Min, Max
    C, D = min(Y), max(Y)
    NormalizedNum = (C + (((x - A) * (D - C)) / (B - A)))
    return NormalizedNum


if __name__ == '__main__':
    print(NormalizeNumber(45,10,85))