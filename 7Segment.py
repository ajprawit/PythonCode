# segment representation of each digit
# The original table was for some C library but I can't find it anywhere
# to give credit to the author. If you recognize it, leave me a comment please.

#  --a--
# |     |
# f     b
# |     |
#  --g--
# |     |
# e     c
# |     |
#  --d--  p

segmentDigits = [
    #a b c d e f g p Segments
    [0, 0, 0, 0, 0, 0, 1, 1], # 0
    [1, 0, 0, 1, 1, 1, 1, 1], # 1
    [0, 0, 1, 0, 0, 1, 0, 1], # 2
    [0, 0, 0, 0, 1, 1, 0, 1], # 3
    [1, 0, 0, 1, 1, 0, 0, 1], # 4
    [0, 1, 0, 0, 1, 0, 0, 1], # 5
    [0, 1, 0, 0, 0, 0, 0, 1], # 6
    [0, 0, 0, 1, 1, 1, 1, 1], # 7
    [0, 0, 0, 0, 0, 0, 0, 1], # 8
    [0, 0, 0, 0, 1, 0, 0, 1], # 9
    [0, 0, 0, 1, 0, 0, 0, 1], # A
    [1, 1, 0, 0, 0, 0, 0, 1], # b
    [0, 1, 1, 0, 0, 0, 1, 1], # C
    [1, 0, 0, 0, 0, 1, 0, 1], # d
    [0, 1, 1, 0, 0, 0, 0, 1], # E
    [0, 1, 1, 1, 0, 0, 0, 1], # F
    [1, 1, 1, 1, 1, 1, 1, 1], # blank
];

GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)

# blocks activation pins
blockActivationPins = [ 3, 5, 7 ]

# setup all blocks
for i in range(0, len(blockActivationPins)):
    GPIO.setup(blockActivationPins[i], GPIO.OUT)
    GPIO.output(blockActivationPins[i], False)

# segments activation pins
segmentPins = [ 12, 13, 15, 16, 22, 21, 19, 18 ]

# setup all segments
for i in range(0, len(segmentPins)):
    GPIO.setup(segmentPins[i], GPIO.OUT)
    GPIO.output(segmentPins[i], True)

def get_minute_load():
    p = subprocess.Popen(['uptime'], stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
    out, err = p.communicate()
    return out.split(' ')[11]

# main loop
# to terminate the loop press CTRL+C
while True:
    # load = '1.23'
    load = get_minute_load()
    # remove decimal point from load
    # loadSimplified = '123'
    loadSimplified = load.replace('.', '');
    # position of decimal point
    decPoint = load.find('.')

    # each block
    for segment in range(0,3):
        char = loadSimplified[segment]
        # appropriate segments to lit for this digit
        segmentsToLit = segmentDigits[int(char)]

        # activate block
        GPIO.output(blockActivationPins[segment], True)

        # set decimal point
        if segment == decPoint - 1:
            GPIO.output(segmentPins[7], False)
        else:
            GPIO.output(segmentPins[7], True)

        # iterate all segments in this block
        for led in range(0, 7):
            # True or False based on segmentDigits table
            val = bool(segmentsToLit[led])
            GPIO.output(segmentPins[led], val)

        # short pause
        time.sleep(0.005)

        # deactivate block
        GPIO.output(blockActivationPins[segment], False)
