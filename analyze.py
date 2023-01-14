import matplotlib.pyplot
import numpy

val = numpy.load('Data/backLegSensorValues.npy')
valF = numpy.load('Data/frontLegSensorValues.npy')

matplotlib.pyplot.plot(val, linewidth=3, label='Backleg')
matplotlib.pyplot.plot(valF, linewidth=3, label='Frontleg')

matplotlib.pyplot.legend()

matplotlib.pyplot.show()

exit()