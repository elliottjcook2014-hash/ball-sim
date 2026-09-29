update_hooks = []


def register_update_hook(func):
    update_hooks.append(func)
    return func
