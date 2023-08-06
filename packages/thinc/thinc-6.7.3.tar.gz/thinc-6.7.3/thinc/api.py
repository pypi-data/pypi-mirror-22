import copy

from .neural._classes.feed_forward import FeedForward
from .neural._classes.model import Model
from . import check
from .check import equal_axis
from . import describe


class FunctionLayer(Model):
    '''Wrap functions into weightless Model instances, for use as network
    components.'''
    def __init__(self, begin_update, predict=None, predict_one=None,
            nI=None, nO=None, *args, **kwargs):
        self.begin_update = begin_update
        if predict is not None:
            self.predict = predict
        if predict_one is not None:
            self.predict_one = predict_one
        self.nI = nI
        self.nO = nO
        Model.__init__(self)


def layerize(begin_update=None, *args, **kwargs):
    '''Wrap a function into a layer'''
    if begin_update is not None:
        return FunctionLayer(begin_update, *args, **kwargs)
    def wrapper(begin_update):
        return FunctionLayer(begin_update, *args, **kwargs)
    return wrapper


def metalayerize(user_func):
    '''Wrap a function over a sequence of layers and an input into a layer.'''
    def returned(layers, *args, **kwargs):
        def begin_update(X, *args, **kwargs):
            return user_func(layers, X, *args, **kwargs)
        return FunctionLayer(begin_update, *args, **kwargs)
    return returned


@layerize
def flatten_add_lengths(seqs, pad=0, drop=0.):
    ops = Model.ops
    lengths = ops.asarray([len(seq) for seq in seqs], dtype='i')
    def finish_update(d_X, sgd=None):
        return ops.unflatten(d_X, lengths, pad=pad)
    X = self.ops.flatten(seqs, pad=pad)
    return (X, lengths), finish_update


def with_getitem(idx, layer):
    def begin_update(items, drop=0.):
        X, finish = layer.begin_update(items[idx], drop=drop)
        return items[:idx] + (X,) + items[idx+1:], finish
    model = layerize(begin_update)
    model._layers.append(layer)
    def on_data(self, items, y):
        for hook in layer.on_data_hooks:
            hook(layer, items[idx], y)
    model.on_data_hooks.append(on_data)
    return model


def noop(*layers):
    '''Transform a sequences of layers into a null operation.'''
    def begin_update(X, drop=0.):
        return X, lambda D, *a, **k: D
    return begin_update


def chain(*layers):
    '''Compose two models `f` and `g` such that they become layers of a single
    feed-forward model that computes `g(f(x))`.

    Raises exception if their dimensions don't match.
    '''
    if len(layers) == 0:
        return FeedForward([])
    elif len(layers) == 1:
        return layers[0]
    else:
        return FeedForward(layers)


def clone(orig, n):
    '''Construct `n` copies of a layer, with distinct weights.

    i.e. `clone(f, 3)(x)` computes `f(f'(f''(x)))`.
    '''
    if n == 0:
        return layerize(noop())
    layers = [orig]
    for i in range(n-1):
        layers.append(copy.deepcopy(orig))
        layers[-1].set_id()
    return FeedForward(layers)


def concatenate(*layers): # pragma: no cover
    '''Compose two or more models `f`, `g`, etc, such that their outputs are
    concatenated, i.e. `concatenate(f, g)(x)` computes `hstack(f(x), g(x))`
    '''
    if not layers:
        return noop()
    ops = layers[0].ops
    def begin_update(X, *a, **k):
        forward, backward = split_backward(layers)
        values = [fwd(X, *a, **k) for fwd in forward]

        output = ops.xp.hstack(values)
        shapes = [val.shape for val in values]

        def finish_update(gradient, *args, **kwargs):
            layer_grads = []
            start = 0
            for bwd, shape in zip(backward, shapes):
                end = start + shape[1]
                if bwd is not None:
                    d = bwd(ops.xp.ascontiguousarray(gradient[:, start : end]),
                            *args, **kwargs)
                    if d is not None and hasattr(X, 'shape'):
                        if not layer_grads:
                            layer_grads.append(d)
                        else:
                            layer_grads[-1] += d
                start = end
            if layer_grads:
                return ops.asarray(layer_grads[-1])
            else:
                return None
        return output, finish_update
    layer = FunctionLayer(begin_update)
    layer._layers = list(layers)
    def on_data(self, X, y=None):
        for layer in self._layers:
            for hook in layer.on_data_hooks:
                hook(layer, X, y)
    layer.on_data_hooks.append(on_data)
    return layer


def add(*layers):
    if not layers:
        return noop()
    ops = layers[0].ops
    def forward(X, drop=0.):
        outs, callbacks = zip(*[lyr.begin_update(X, drop=drop) for lyr in layers])
        out = outs[0]
        for o in outs:
            out += o

        def backward(d_out, sgd=None):
            grads = [bp(d_out, sgd=sgd) for bp in callbacks if bp is not None]
            grads = [g for g in grads if g is not None]
            if grads:
                total = grads[0]
                for g in grads:
                    total += g
                return total
            else:
                return None
        return out, backward
    model = layerize(forward)
    model._layers = list(layers)
    def on_data(self, X, y):
        for layer in layers:
            for hook in layer.on_data_hooks:
                hook(layer, X, y)
    model.on_data_hooks.append(on_data)
    return model


def split_backward(layers): # pragma: no cover
    '''Separate a sequence of layers' `begin_update` methods into two lists of
    functions: one that computes the forward values, and the other that completes
    the backward pass. The backward sequence is only populated after the forward
    functions have been applied.
    '''
    backward = []
    forward = [sink_return(op.begin_update, backward.append)
               for op in layers]
    return forward, backward


def sink_return(func, sink, splitter=None): # pragma: no cover
    '''Transform a function `func` that returns tuples into a function that returns
    single values. Call a function `sink` on the unused values.
    '''
    def wrap(*args, **kwargs):
        output = func(*args, **kwargs)
        if splitter is None:
            to_keep, to_sink = output
        else:
            to_keep, to_sink = splitter(*output)
        sink(to_sink)
        return to_keep
    return wrap


def Arg(i):
    @layerize
    def begin_update(batched_inputs, drop=0.):
        inputs = list(zip(*batched_inputs))
        return inputs[i], None
    return begin_update


def with_flatten(layer, pad=0, ndim=4):
    def begin_update(seqs_in, drop=0.):
        lengths = layer.ops.asarray([len(seq) for seq in seqs_in])
        X, bp_layer = layer.begin_update(layer.ops.flatten(seqs_in, pad=pad),
                                         drop=drop)
        if bp_layer is None:
            return layer.ops.unflatten(X, lengths, pad=pad), None
        def finish_update(d_seqs_out, sgd=None):
            d_X = bp_layer(layer.ops.flatten(d_seqs_out, pad=pad), sgd=sgd)
            if d_X is None:
                return None
            else:
                return layer.ops.unflatten(d_X, lengths, pad=pad)
        return layer.ops.unflatten(X, lengths, pad=pad), finish_update
    model = layerize(begin_update)
    model._layers.append(layer)
    model.on_data_hooks.append(_with_flatten_on_data)
    model.name = 'flatten'
    return model

def _with_flatten_on_data(model, X, y):
    X = model.ops.flatten(X)
    for layer in model._layers:
        for hook in layer.on_data_hooks:
            hook(layer, X, y)
        X = layer(X)


def get_word_ids(ops, pad=1, token_drop=0., ignore=None):
    # TODO: Is this made obsolete by the FeatureExtractor?
    def forward(docs, drop=0.):
        '''Get word forms.'''
        seqs = []
        ops = Model.ops
        for doc in docs:
            if ignore is not None:
                doc = [token for token in doc if not ignore(token)]
            #seq = [0] * pad
            seq = [(token.lex_id or token.orth) for token in doc]
            #seq += [0] * pad
            seqs.append(ops.asarray(seq, dtype='uint64'))
        return seqs, None
    return layerize(forward)



def FeatureExtracter(attrs):
    def forward(docs, drop=0.):
        features = [doc.to_array(attrs) for doc in docs]
        def backward(d_features, sgd=None):
            return d_features
        return features, backward
    return layerize(forward)


