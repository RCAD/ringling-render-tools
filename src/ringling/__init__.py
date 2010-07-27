__VERSION__ = (0,0,2)
__VERSION_TAG__ = "dev"

def get_version():
    version_string = __name__+' '+'.'.join([str(n) for n in __VERSION__])
    if __VERSION_TAG__:
        version_string += __VERSION_TAG__
    return version_string