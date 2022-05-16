from __future__ import annotations

from typing import Final, List

import api

HOLIDAYS_MODE: Final = 'W'

class AldesProduct:

    _MODES = {
        'Holidays' : HOLIDAYS_MODE,
        'Daily'    : 'V',
        'Boost'    : 'Y',
        'Guest'    : 'X'
    }

    _DISPLAY_NAMES = {
        'INSPIRAIR_HOME_S' : 'InspirAIR® Home S'
    }

    def __init__(self, aldesApi: api.AldesApi, id: str, name: str, mode: str):
        self._aldesApi = aldesApi
        self._id       = id
        self._name     = name
        self._mode     = mode
    
    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    def get_display_name(self) -> str:
        return self._DISPLAY_NAMES.get(self._name, self._name)
    
    def get_display_modes(self) -> List[str]:
        return list(self._MODES.keys())

    def get_display_mode(self) -> str:
        for display_mode, mode in self._MODES.items():
            if mode == self._mode:
                return display_mode
        
        raise ValueError(f'Mode {self._mode} is not managed, please report.')
    
    async def maybe_set_mode_from_display(self, display_mode: str) -> None:
        await self._aldesApi.request_set_mode(self._id, self._MODES[display_mode])
    
    async def update(self) -> None:
        data = await self._aldesApi.get_product(self._id)
        if (mode := data.get('mode')) is not None:
            self._mode = mode
