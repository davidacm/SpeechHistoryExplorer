# NVDA configHelper.
# Copyright (C) 2022 David CM

import config

def getConfigValue(path, optName):
	""" this function helps to accessing config values.
	params
	@path: the path to the option.
	@optName: the option name
	"""
	ops = config.conf[path[0]]
	for k in path[1:]:
		ops = ops[k]
	return ops[optName]


def setConfigValue(path, optName, value):
	""" this function helps to accessing and set config values.
	params
	@path: the path to the option.
	@optName: the option name
	@value: the value to set.
	"""
	ops = config.conf[path[0]]
	for k in path[1:]:
		ops = ops[k]
	ops[optName] = value


def registerConfig(clsSpec):
	AF = clsSpec()
	config.conf.spec[AF.path[0]] = AF.createSpec()
	AF.returnValue = True
	return AF


class OptConfig:
	""" just a helper descriptor to create the main class to accesing config values.
	the option name will be taken from the declared variable. if you need to set another name, set it in the first param.
	"""
	def __init__(self, a, b = None):
		"""
		params:
		@a: usually the spec description. But if b is not none, a will be the name of the option.
		@b: the config description when is not None.
		"""
		if b:
			self.name = a
			self.desc = b
		else:
			self.desc = a
			self.name = None

	def __set_name__(self, owner, name):
		if not self.name:
			self.name = name
		owner._confOpts.append(name)

	def __get__(self, obj, type=None):
		if obj.returnValue:
			return getConfigValue(obj.path, self.name)
		return self.name, self.desc

	def __set__(self, obj, value):
		setConfigValue(obj.path, self.name, value)


class BaseConfig:
	""" this class will help to get and set config values.
	the idea behind this is to generalize the config path and config names.
	sometimes, a mistake in the dict to access the values can produce an undetectable bug.
	if returnValue attribute is set to False, this will return the option name instead of the value.
	by default this value is False, to help to create the configuration spec first.
	Set it to true after creating this spec.
	"""

	def __init__(self, path):
		self.returnValue = False
		if isinstance(path, list):
			self.path = path
		else:
			self.path = [path]

	def createSpec(self):
		""" this method creates a config spec with the provided attributes in the class
		"""
		s = {}
		for k in self.__class__._confOpts:
			k = self.__getattribute__(k)
			s[k[0]] = k[1]
		return s
	# an array of the available options.
	_confOpts = []
