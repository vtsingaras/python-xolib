import types
import six


def patch_method_in(obj, method_code):
    ld = dict()
    exec(method_code, None, ld)
    for name in ld:
        setattr(obj, name, types.MethodType(ld[name], obj))


def render_function(xoa_method_name, xoa_method_params):
    function_name = xoa_method_name.replace('.', '_')
    if six.PY2:
        func_template = """def {function_name}(self, **kwargs): return self.call('{xoa_method}', **kwargs)"""
        return func_template.format(function_name=function_name, xoa_method=xoa_method_name)
    else:
        func_template = """def {function_name}(self{sig_args}): return self.call('{xoa_name}'{proxy_args})"""
        sig_args = str()
        proxy_args = str()
        if len(xoa_method_params) > 0:
            sig_args += ', *'
            for param_name, param_attrs in xoa_method_params.items():
                if 'optional' in param_attrs and param_attrs['optional']:
                    sig_args += ', ' + str(param_name) + '=None'
                else:
                    sig_args += ', ' + str(param_name)
                proxy_args += ', ' + str(param_name) + '=' + str(param_name)
        return func_template.format(function_name=function_name, xoa_name=xoa_method_name,
                                    sig_args=sig_args, proxy_args=proxy_args)
