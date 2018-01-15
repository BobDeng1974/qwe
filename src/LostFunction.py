import numpy as np
class LostFunction(object):
    @staticmethod
    def linear(AL, Y):
        m = Y.shape[1]
        cost = (-1 / m) * np.sum(np.square(np.subtract(AL,Y)))
        return cost
    @staticmethod
    def linear_derivative(AL, Y):
        """

        :param y_predit:
        :param y_label:
        :return:
        """
        pass
        return AL - Y

    @staticmethod
    def cross_entropy(AL, Y):
        m = Y.shape[0]
        try:
            cost = np.multiply(Y, np.log(AL)) + np.multiply(1 - Y, np.log(1 - AL))
            cost_mean = (-1 / m) * np.sum(cost)
            return cost_mean
        except FloatingPointError as e:
            print(Y,AL)
            raise e
    @staticmethod
    def cross_entropy_derivative(AL, Y):
        """
        C(x) = -Sigma(y * log(h(x)) + (1 - y) * log(1 - h(x)))
        dC/dh = y-h
        :param y_predit:
        :param y_label:
        :return:
        """
        # return Y * 1./AL + (Y - 1) * (1 - AL)
        return -(np.divide(Y, AL) - np.divide(1 - Y, 1 - AL))

if __name__ == '__main__':
    np.random.seed(10)
    AL = np.array([[.8,.9,0.4]]).T
    Y = np.asarray([[1, 1, 1]]).T
    print(Y.shape)
    print(LostFunction.cross_entropy(AL,Y))
    print(LostFunction.cross_entropy_derivative(AL,Y))