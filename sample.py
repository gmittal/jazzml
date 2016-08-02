import random
import numpy as np
import tensorflow as tf

seed_value = 42
tf.set_random_seed(seed_value)
random.seed(seed_value)

def one_hot(v):
    return np.eye(vocab_size)[v]

data = list(np.loadtxt("data/increasing_numbers_dataset.gz")) # import dataset
chars = sorted(list(set(data)))
data_size, vocab_size = len(data), len(chars)
print('Data has %d characters, %d unique.' % (data_size, vocab_size))
char_to_ix = {ch: i for i, ch in enumerate(chars)}
ix_to_char = {i: ch for i, ch in enumerate(chars)}
bestLoss = 1e10; # anything has to be better than an arbitrarily large number

# Hyper-parameters
hidden_size   = 100  # hidden layer's size
seq_length    = 25   # number of steps to unroll
learning_rate = 1e-1

inputs     = tf.placeholder(shape=[None, vocab_size], dtype=tf.float32, name="inputs")
targets    = tf.placeholder(shape=[None, vocab_size], dtype=tf.float32, name="targets")
init_state = tf.placeholder(shape=[1, hidden_size], dtype=tf.float32, name="state")

initializer = tf.random_normal_initializer(stddev=0.1)

with tf.variable_scope("RNN") as scope:
    hs_t = init_state
    ys = []
    for t, xs_t in enumerate(tf.split(0, seq_length, inputs)):
        if t > 0: scope.reuse_variables()  # Reuse variables
        Wxh = tf.get_variable("Wxh", [vocab_size, hidden_size], initializer=initializer)
        Whh = tf.get_variable("Whh", [hidden_size, hidden_size], initializer=initializer)
        Why = tf.get_variable("Why", [hidden_size, vocab_size], initializer=initializer)
        bh  = tf.get_variable("bh", [hidden_size], initializer=initializer)
        by  = tf.get_variable("by", [vocab_size], initializer=initializer)

        hs_t = tf.tanh(tf.matmul(xs_t, Wxh) + tf.matmul(hs_t, Whh) + bh)
        ys_t = tf.matmul(hs_t, Why) + by
        ys.append(ys_t)

hprev = hs_t
output_softmax = tf.nn.softmax(ys[-1])  # Get softmax for sampling

outputs = tf.concat(0, ys)
loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(outputs, targets))

# Minimizer
minimizer = tf.train.AdamOptimizer()
grads_and_vars = minimizer.compute_gradients(loss)

# Gradient clipping
grad_clipping = tf.constant(5.0, name="grad_clipping")
clipped_grads_and_vars = []
for grad, var in grads_and_vars:
    clipped_grad = tf.clip_by_value(grad, -grad_clipping, grad_clipping)
    clipped_grads_and_vars.append((clipped_grad, var))

# Gradient updates
updates = minimizer.apply_gradients(clipped_grads_and_vars)

# Session
sess = tf.Session()
init = tf.initialize_all_variables()
sess.run(init)

# Initial values
n, p = 0, 0
hprev_val = np.zeros([1, hidden_size])

# Initialize
if p + seq_length + 1 >= len(data) or n == 0:
    hprev_val = np.zeros([1, hidden_size])
    p = 0  # reset

# Prepare inputs
input_vals  = [char_to_ix[ch] for ch in data[p:p + seq_length]]
target_vals = [char_to_ix[ch] for ch in data[p + 1:p + seq_length + 1]]

input_vals  = one_hot(input_vals)
target_vals = one_hot(target_vals)


hprev_val = np.loadtxt('data/weights.gz').reshape(1, 100)

# Do sampling
sample_length = 200
start_ix      = 0
sample_seq_ix = [char_to_ix[ch] for ch in data[start_ix:start_ix + seq_length]]
print sample_seq_ix
ixes          = []
sample_prev_state_val = np.copy(hprev_val)

for t in range(sample_length):
    sample_input_vals = one_hot(sample_seq_ix)
    sample_output_softmax_val, sample_prev_state_val = \
        sess.run([output_softmax, hprev],
                 feed_dict={inputs: sample_input_vals, init_state: sample_prev_state_val})

    ix = np.random.choice(range(vocab_size), p=sample_output_softmax_val.ravel())
    print ix
    ixes.append(ix)
    sample_seq_ix = sample_seq_ix[1:] + [ix]

txt = (ix_to_char[ix] for ix in ixes)
txt = list(txt)
print('----\n %s \n----\n' % (sample_seq_ix,))

p += seq_length
n += 1
