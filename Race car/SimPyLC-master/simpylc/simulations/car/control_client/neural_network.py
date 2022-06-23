class Network:
    def __init__(self):
        self.layers = []
        self.loss = None
        self.loss_prime = None

    # add layer to neural network
    def add_layer(self, layer):
        self.layers.append(layer)

    # create loss
    def create_loss(self, loss, loss_prime):
        self.loss = loss
        self.loss_prime = loss_prime

    # train output
    def get_output(self, input_data):
        # dimensions input data
        samples = len(input_data)
        result = []

        # for each sample in range of samples
        for i in range(samples):
            # do forward propagation
            output = input_data[i]
            for layer in self.layers:
                output = layer.forward_propagation(output)
            result.append(output)

        return result

    # train the neural network
    def train_network(self, in_train, out_train, cycles, learning_rate):
        # dimensions of samples
        samples = len(in_train)

        # start training
        for i in range(cycles):
            total_error = 0
            for j in range(samples):
                # do forward propagation
                output = in_train[j]
                for layer in self.layers:
                    output = layer.forward_propagation(output)

                # compute loss (for display purpose only)
                total_error += self.loss(out_train[j], output)

                # do backward propagation
                part_error = self.loss_prime(out_train[j], output)
                for layer in reversed(self.layers):
                    part_error = layer.backward_propagation(part_error, learning_rate)

            # calculate average error on all samples
            total_error /= samples
