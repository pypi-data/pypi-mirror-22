from __future__ import absolute_import
from __future__ import print_function
import json
import wrapt
from .io import error


@wrapt.decorator
def bioblend_exception(wrapped, instance, args, kwargs):
    try:
        return wrapped(*args, **kwargs)
    except Exception as e:
        if hasattr(e, 'body'):
            try:
                error(json.loads(e.body)['err_msg'])
            except json.decoder.JSONDecodeError:
                error(str(e))
        else:
            error(str(e))


@wrapt.decorator
def dict_output(wrapped, instance, args, kwargs):
    # TODO enhance
    output = wrapped(*args, **kwargs)
    print((json.dumps(output, indent=4)))
