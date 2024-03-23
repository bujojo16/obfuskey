# Obfuskey

## Release notes

### v2.1
#### output.py:
Previously the output file name was the sha256 hash of the original seedphrase. This being an obvious weak-point, it is now a recursive hash first calculated on the original seedphrase and then rehashed with every word in the seedphrase, making it *a bit* more complex to break.
