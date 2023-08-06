# python-discrete

This is a Pure Python implementation of several discrete probability
distributions. There are no external dependencies.

Why would you use this over, say, numpy and scipy? The main reason would
be is if, for whatever reason, you're unable to install C extensions
(for example, you need to work with 32-bit Python on a 64-bit system)
and just need to generate random events. The Python ```random``` module
supports generating events for several continuous random distributions
not discrete ones, hence this module.

## Usage

All implemented distributions are a subclass of the abstract Discrete class,
with ```pdf(k)```, ```cdf(k)```, and ```generate(n)``` methods. The generate
method returns an array of size ```n``` populated with randomly distributed
variables from the distribution.

Currently the Poisson and Binomial distributions are implemented. More
will likely be added in the future.

## Legal

discrete is released under the MIT License; see attached LICENSE file.
