


from typing import List
from pyd.base_models import BaseJanre, BaseMovie


class ResponseMovie(BaseMovie):
    janres: List[BaseJanre]