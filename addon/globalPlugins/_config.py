import config

def getConfigValue(path, optName):
	""" this function helps to accessing config values.
	params
	@path: the path to the option.
	@optName: the option name
	"""
	ops = config.conf[path[0]]
	for k in path[1:]:
		opts = opts[k]
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
		opts = opts[k]
	ops[optName] = value

class OptConfig:
	""" just a helper descriptor to create the main class to accesing config values.
	"""
	def __init__(self, optName):
		self.optName = optName

	def __get__(self, obj, type=None):
		if obj.returnValue:
			return getConfigValue(obj.path, self.optName)
		return self.optName

	def __set__(self, obj, value):
		setConfigValue(obj.path, self.optName, value)

class appConfig:
	""" this class will help to get and set config values.
	the idea behind this is to generalize the config path and config names.
	sometimes, a mistake in the dict to access the values can produce an undetectable bug.
	if returnValue attribute is set to False, this will return the option name instead of the value.
	by default this value is False, to help to create the configuration spec first.
	Set it to true after creating this spec.
	"""

	def __init__(self):
		self.path = ['speechHistoryExplorer']
		self.returnValue = False

	maxHistoryLength = OptConfig('maxHistoryLength')
	trimWhitespaceFromStart = OptConfig('trimWhitespaceFromStart')
	trimWhitespaceFromEnd = OptConfig('trimWhitespaceFromEnd')
	beepWhenPerformingActions = OptConfig('beepWhenPerformingActions')
	beepPanning = OptConfig('beepPanning')

appConfig = appConfig()


confspec = {
	appConfig.maxHistoryLength: 'integer(default=500)',
	appConfig.trimWhitespaceFromStart: 'boolean(default=false)',
	appConfig.trimWhitespaceFromEnd: 'boolean(default=false)',
	appConfig.beepWhenPerformingActions: 'boolean(default=true)',
	appConfig.beepPanning: 'boolean(default=true)',
}
config.conf.spec[appConfig.path[0]] = confspec
appConfig.returnValue = True
