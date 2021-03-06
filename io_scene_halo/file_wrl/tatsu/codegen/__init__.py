from __future__ import annotations

from ..exceptions import CodegenError
from ..codegen.cgbase import (  # noqa
    DelegatingRenderingFormatter,
    ModelRenderer,
    NullModelRenderer,
    CodeGenerator,
)


def codegen(model, target='python'):
    if target.lower() == 'python':
        from ..codegen import python
        return python.codegen(model)
    else:
        raise CodegenError('Unknown target language: %s' % target)
