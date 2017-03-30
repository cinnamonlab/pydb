class _Singleton(type):
    _instances = {}
    def __call__(klass, *args, **kwargs):
        if klass not in klass._instances:
            klass._instances[klass] = super(_Singleton, klass).__call__(*args, **kwargs)
        return klass._instances[klass]

class Singleton(_Singleton('SingletonMeta', (object,), {})):pass
