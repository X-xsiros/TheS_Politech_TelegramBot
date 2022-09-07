def alarm(name):
    File = open(name)
    Names = File.readlines()
    Trag = ''
    for i in Names:
        Trag = Trag +'@'+ i[0:-1]+ ' '
    return(Trag)


