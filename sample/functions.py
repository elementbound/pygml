def veclen2(x, y):
    return (x**2 + y**2)**0.5

def veclen3(x, y, z):
    return (x**2 + y**2 + z**2)**0.5

class Foo:
    def hi():
        print('Hi!')

def dirvec(dir, pitch):
    f = dcos(pitch)
    v = [
        dcos(dir)*f,
        -dsin(dir)*f,
        dsin(pitch)
    ]

    return v
