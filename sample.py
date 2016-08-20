import random
import numpy as np
import tensorflow as tf
import os
import argparse

seed_value = 1
tf.set_random_seed(seed_value)
random.seed(seed_value)

def one_hot(v):
    return np.eye(vocab_size)[v]

# Get command line arguments
parser = argparse.ArgumentParser(description='Samples the LSTM model based on results from train.py')
parser.add_argument('data', action="store", type=str)

# Grab the compressed file contents
filePath = os.getcwd() + "/" + parser.parse_args().data

data = [ int(x) for x in np.loadtxt(filePath+"/data.gz") ]# import dataset
vocab = np.loadtxt(filePath+"/vocab.gz")
chars = sorted(list(set(data)))
data_size, vocab_size = len(data), len(chars)
print('Data has %d characters, %d unique.' % (data_size, vocab_size))
char_to_ix = {ch: i for i, ch in enumerate(chars)}
ix_to_char = {i: ch for i, ch in enumerate(chars)}
bestLoss = 1e10; # anything has to be better than an arbitrarily large number

# Hyper-parameters
hidden_size   = 100  # hidden layer's size
seq_length    = 50   # number of steps to unroll
learning_rate = 1e-1

inputs     = tf.placeholder(shape=[None, vocab_size], dtype=tf.float32, name="inputs")
targets    = tf.placeholder(shape=[None, vocab_size], dtype=tf.float32, name="targets")
init_state = tf.placeholder(shape=[1, hidden_size], dtype=tf.float32, name="state")
Wxh_p = tf.placeholder(shape=[vocab_size, hidden_size], dtype=tf.float32, name="Wxh")
Whh_p = tf.placeholder(shape=[hidden_size, hidden_size], dtype=tf.float32, name="Whh")
Why_p = tf.placeholder(shape=[hidden_size, vocab_size], dtype=tf.float32, name="Why")
bh_p  = tf.placeholder(shape=[hidden_size], dtype=tf.float32, name="bh")
by_p  = tf.placeholder(shape=[vocab_size], dtype=tf.float32, name="by")

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

        Wxh_a = Wxh.assign(Wxh_p)
        Whh_a = Whh.assign(Whh_p)
        Why_a = Why.assign(Why_p)
        bh_a = bh.assign(bh_p)
        by_a = by.assign(by_p)

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


# Import weights + bias
sess.run(Wxh_a, feed_dict={Wxh_p: np.loadtxt(os.getcwd()+"/data/Wxh.gz").astype(np.float32)})
sess.run(Whh_a, feed_dict={Whh_p: np.loadtxt(os.getcwd()+"/data/Whh.gz").astype(np.float32)})
sess.run(Why_a, feed_dict={Why_p: np.loadtxt(os.getcwd()+"/data/Why.gz").astype(np.float32)})
sess.run(bh_a, feed_dict={bh_p: np.loadtxt(os.getcwd()+"/data/bh.gz").astype(np.float32)})
sess.run(by_a, feed_dict={by_p: np.loadtxt(os.getcwd()+"/data/by.gz").astype(np.float32)})


hprev_val, loss_val, _ = sess.run([hprev, loss, updates],
                                  feed_dict={inputs: input_vals,
                                             targets: target_vals,
                                             init_state: hprev_val})

print loss_val
# print list(vocab)

# Do sampling
sample_length = 40
start_ix      = 0
sample_seq_ix = [char_to_ix[ch] for ch in data[start_ix:start_ix + seq_length]]
ixes          = []
sample_prev_state_val = np.copy(hprev_val)

for t in range(sample_length):
    sample_input_vals = one_hot(sample_seq_ix)
    sample_output_softmax_val, sample_prev_state_val = sess.run([output_softmax, hprev], feed_dict={inputs: sample_input_vals, init_state: sample_prev_state_val})

    ix = np.random.choice(range(vocab_size), p=sample_output_softmax_val.ravel())

    ixes.append(ix)
    sample_seq_ix = sample_seq_ix[1:] + [ix]

txt = (ix_to_char[ix] for ix in ixes)
txt = list(txt)
new_results = []
print txt
for x in range(0, len(txt)):
    print vocab[int(txt[x])]
    pass

p += seq_length
n += 1
