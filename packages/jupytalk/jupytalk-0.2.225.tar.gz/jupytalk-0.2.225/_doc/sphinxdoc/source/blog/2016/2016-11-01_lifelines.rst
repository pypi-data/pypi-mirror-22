
.. blogpost::
    :title: lifelines plotting is failing
    :keywords: lifelines, plotting
    :date: 2016-11-01
    :categories: module

    The unit test checking the notebook showing
    lifelines recently started to fail.
    This was caused by a matplotlib update.
    Check `issue 191 <https://github.com/CamDavidsonPilon/lifelines/issues/191#issuecomment-145275656>`_.
    The issue is fixed on github but the module has not been updated yet.
    It can be fixed by manually updating the file
    `plotting.py <https://github.com/CamDavidsonPilon/lifelines/blob/master/lifelines/plotting.py#L220>`_.
