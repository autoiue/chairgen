class MyLayer(Layer):
    def __init__(self, output_dim, **kwargs):
        self.output_dim = output_dim
        super(MyLayer, self).__init__(**kwargs)

    def build(self, input_shape):
        # Create a trainable weight variable for this layer.
        self.W = self.add_weight(shape=(input_shape[1], self.output_dim),
                                 initializer='random_uniform',
                                 trainable=True)
        super(MyLayer, self).build()  # Be sure to call this somewhere!

    def call(self, x, mask=None):
        return K.dot(x, self.W)

    def get_output_shape_for(self, input_shape):
        return (input_shape[0], self.output_dim)




def repeat(x, n):
    """Repeats a 2D tensor.
    if `x` has shape (samples, dim) and `n` is `2`,
    the output will have shape `(samples, 2, dim)`.
    # Returns
        A tensor.
    """
    assert ndim(x) == 2
    x = tf.expand_dims(x, 1)
    pattern = stack([1, n, 1])
    return tf.tile(x, pattern)

def expand_dims(x, dim=-1):
    """Adds a 1-sized dimension at index "dim".
    # Returns
        A tensor with expended dimensions.
    """
    return tf.expand_dims(x, dim)