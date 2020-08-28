def debug( content ):
    print( "[*] " + str(content) , flush=True)
def bad( content ):
    print( "[-] " + str(content) , flush=True)
def good( content ):
    print( "[+] " + str(content) , flush=True)

# sample output:
# [*] Gimme yo money
# [-] Money taken by chad.
# [+] Chad receives the money.
