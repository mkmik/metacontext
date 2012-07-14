#- LANGUAGE match-statement -#

def test(msg):
    match msg:
        case ('test', a):
            print "TEST", msg
        case ('other', a):
            print "OTHER", msg
