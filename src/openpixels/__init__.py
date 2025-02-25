from .client import AsyncOpenPixels

__all__ = ["AsyncOpenPixels"]

# Update the __module__ attribute for exported symbols so that
# error messages point to this module instead of the module
# it was originally defined in, e.g.
# openai._exceptions.NotFoundError -> openai.NotFoundError
# __locals = locals()
# for __name in __all__:
#     if not __name.startswith("__"):
#         try:
#             __locals[__name].__module__ = "openpixels"
#         except (TypeError, AttributeError):
#             # Some of our exported symbols are builtins which we can't set attributes for.
#             pass
