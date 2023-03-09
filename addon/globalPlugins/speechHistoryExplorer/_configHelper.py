# NVDA configHelper.
# Copyright (C) 2022 - 2023 David CM

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


def registerConfig(clsSpec, path=None):
	AF = clsSpec(path)
	config.conf.spec[AF.__path__[0]] = AF.createSpec()
	AF.returnValue = True
	return AF


class OptConfig:
	""" just a helper descriptor to create the main class to accesing config values.
	the option name will be taken from the declared variable.
	"""
	def __init__(self, desc):
		"""
		params:
		@desc: the spec description.
		"""
		self.desc = desc

	def __set_name__(self, owner, name):
		self.name = name
		owner.__confOpts__.append(name)

	def __get__(self, obj, type=None):
		if obj.returnValue:
			return getConfigValue(obj.__path__, self.name)
		return self.name, self.desc

	def __set__(self, obj, value):
		setConfigValue(obj.__path__, self.name, value)


class BaseConfig:
	""" this class will help to get and set config values.
	the idea behind this is to generalize the config path and config names.
	sometimes, a mistake in the dict to access the values can produce an undetectable bug.
	if returnValue attribute is set to False, this will return the option name instead of the value.
	by default this value is False, to help to create the configuration spec first.
	Set it to true after creating this spec.
	"""
	__path__ = None
	def __init__(self, path=None):
		self.returnValue = False
		if not path:
			path = self.__class__.__path__
		if not path:
			raise Exception("Path for the config is not defined")
		if isinstance(path, list):
			self.__path__ = path
		else:
			self.__path__ = [path]

	def createSpec(self):
		""" this method creates a config spec with the provided attributes in the class
		"""
		s = {}
		for k in self.__class__.__confOpts__:
			k = self.__getattribute__(k)
			s[k[0]] = k[1]
		return s
	# an array of the available options.
	__confOpts__ = []


def configSpec(pathOrCls):
	""" a decorator to help with the generation of the class config spec.
	adds a get and set descriptor for eatch attribute in the config class.
	except the attributes starting with "__".
	params:
	@pathOrCls: the config path,
	or if the decorator is called without params, then the decorated class.
	path as an argument in the decorator has a higher priority than the __path__ declared in the class.
	"""
	def configDecorator(cls):
		class ConfigSpec(BaseConfig):
			pass

		for k in cls.__dict__:
			if k.startswith("__"): continue
			v = getattr(cls, k)
			d = OptConfig(v)
			d.__set_name__(ConfigSpec, k)
			setattr(ConfigSpec, k, d)
		ConfigSpec.__path__ = path
		return ConfigSpec
	if isinstance(pathOrCls, str):
		path = pathOrCls
		return configDecorator
	else:
		path = pathOrCls.__path__
		return configDecorator(pathOrCls)
