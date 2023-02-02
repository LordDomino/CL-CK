class BaseUnit:
	"""General base unit for all CL-CK classes."""
	
	_cls_prefix: str | None = None

	_elements: list["BaseUnit"] = []
	_id: int = 0

	_show_repr_id = True
	_show_repr_cls = False

	def __init__(self, strval: str) -> None:
		self.__class__._elements = self.__class__._elements + [self]
		self.__class__._id += 1

		self.id: int = self.__class__._id
		self.strval: str = strval

	def __repr__(self) -> str:
		repr_str = f"{self._cls_prefix}"

		if self._show_repr_id:
			repr_str += f"{self._id:0004}"
		if self._show_repr_cls:
			repr_str = f"{self._cls_prefix} " + repr_str

		repr_str += f" \"{self.strval}\""

		return repr_str