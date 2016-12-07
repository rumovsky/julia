# julia
Class for creating gifs with Julia sets.

Simplest example of use, you can also find it in main.py:
```python
from gif_builder import GifBuilder

gb = GifBuilder()
gb.build('examples/ani5.gif')
```
This is actually a full lifecycle of `GifBuilder`. All calculations are being done in the only class method, so you can change any properties of GifBuilder between creating it and calling `build()`.
