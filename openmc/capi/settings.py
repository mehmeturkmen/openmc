from ctypes import (c_int, c_int32, c_int64, c_double, c_char_p, c_bool,
                    POINTER)

from . import _dll
from .core import _DLLGlobal
from .error import _error_handler

_RUN_MODES = {1: 'fixed source',
              2: 'eigenvalue',
              3: 'plot',
              4: 'particle restart',
              5: 'volume'}

_dll.openmc_set_seed.argtypes = [c_int64]
_dll.openmc_get_seed.restype = c_int64


class _Settings(object):
    # Attributes that are accessed through a descriptor
    batches = _DLLGlobal(c_int32, 'n_batches')
    entropy_on = _DLLGlobal(c_bool, 'openmc_entropy_on')
    generations_per_batch = _DLLGlobal(c_int32, 'gen_per_batch')
    inactive = _DLLGlobal(c_int32, 'n_inactive')
    particles = _DLLGlobal(c_int64, 'n_particles')
    restart_batch = _DLLGlobal(c_int, 'openmc_restart_batch')
    restart_run = _DLLGlobal(c_bool, 'openmc_restart_run')
    verbosity = _DLLGlobal(c_int, 'openmc_verbosity')

    @property
    def run_mode(self):
        i = c_int.in_dll(_dll, 'openmc_run_mode').value
        try:
            return _RUN_MODES[i]
        except KeyError:
            return None

    @run_mode.setter
    def run_mode(self, mode):
        current_idx = c_int.in_dll(_dll, 'openmc_run_mode')
        for idx, mode_value in _RUN_MODES.items():
            if mode_value == mode:
                current_idx.value = idx
                break
        else:
            raise ValueError('Invalid run mode: {}'.format(mode))

    @property
    def seed(self):
        return _dll.openmc_get_seed()

    @seed.setter
    def seed(self, seed):
        _dll.openmc_set_seed(seed)


settings = _Settings()
