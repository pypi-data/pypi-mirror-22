import copy
import inspect
import re
import uuid
from functools import partial

import numpy as np
import scipy.spatial

import elfi.client
from elfi.graphical_model import GraphicalModel
from elfi.model.utils import rvs_from_distribution, distance_as_discrepancy
from elfi.store import OutputPool
from elfi.utils import scipy_from_str, observed_name

__all__ = ['ElfiModel', 'ComputationContext', 'Constant', 'Operation', 'Prior',
           'Simulator', 'Summary', 'Discrepancy', 'Distance', 'get_current_model',
           'set_current_model']

""" This module contains the classes for creating generative models in ELFI. The class that
contains the whole representation of this generative model is named `ElfiModel`.

The low level representation of the generative model is a `networkx.DiGraph` with nodes
represented as Python dictionaries that are called node state dictionaries. This
representation is held in `ElfiModel.source_net`. Before the generative model can be ran,
it needs to be compiled and loaded with data (e.g. observed data, precomputed data, batch
index, batch size etc). The compilation and loading of data is the responsibility of the
`Client` implementation and makes it possible in essence to translate ElfiModel to any
kind of computational backend. Finally the class `elfi.Executor` is responsible for
running the compiled and loaded model and producing the outputs of the nodes.

A user typically creates this low level representation by working with subclasses of
`NodeReference`. These are easy to use UI classes of ELFI. Under the hood they create
proper node state dictionaries stored into the `source_net`. The callables such as
simulators or summaries that the user provides to these classes are called operations.


The model graph representation
------------------------------

The `source_net` is a directed acyclic graph (DAG) and holds the state dictionaries of the nodes
and the edges between the nodes. An edge represents a dependency. For example and edge
from a prior node to the simulator node represents that the simulator requires a value
from the prior to be able to run. The edge name corresponds to a parameter name for the
operation, with integer names interpreted as positional parameters.

In the standard compilation process, the `source_net` is augmented with additional nodes
such as batch_size or random_state, that are then added as dependencies for those
operations that require them. In addition the state dicts will be turned into either a
runnable operation or a precomputed value.

The execution order of the nodes in the compiled graph follows the topological ordering of
the DAG (dependency order) and is guaranteed to be the same every time. Note that because
the default behaviour is that nodes share a random state, changing a node that uses shared
random state will affect the result of any later node in the ordering using the same
shared random state even if they would not be depended based on the graph topology. If
this is an issue, separate random states can be created.


State dictionary
----------------

The state of a node is a Python dictionary. It describes the type of the node and any
other relevant state information, such as the user provided callable operation (e.g.
simulator or summary statistic) and any additional parameters the operation needs to be
provided in the compilation.

The following are reserved keywords of the state dict that serve as instructions for the
ELFI compiler. They begin with an underscore. Currently these are:

_operation : callable
    Operation of the node producing the output. Can not be used if _output is present.
_output : variable
    Constant output of the node. Can not be used if _operation is present.
_class : class
    The subclass of `NodeReference` that created the state.
_stochastic : bool, optional
    Indicates that the node is stochastic. ELFI will provide a random_state argument
    for such nodes, which contains a RandomState object for drawing random quantities.
    This node will appear in the computation graph. Using ELFI provided random states
    makes it possible to have repeatable experiments in ELFI.
_observable : bool, optional
    Indicates that there is observed data for this node or that it can be derived from the
    observed data. ELFI will create a corresponding observed node into the compiled graph.
    These nodes are dependencies of discrepancy nodes.
_uses_batch_size : bool, optional
    Indicates that the node operation requires `batch_size` as input. A corresponding edge
    from batch_size node to this node will be added to the compiled graph.
_uses_meta : bool, optional
    Indicates that the node operation requires meta information dictionary about the
    execution. This includes, model name, batch index and submission index.
    Useful for e.g. creating informative and unique file names. If the operation is
    vectorized with `elfi.tools.vectorize`, then also `index_in_batch` will be added to
    the meta information dictionary.
_uses_observed : bool, optional
    Indicates that the node requires the observed data of its parents in the source_net as
    input. ELFI will gather the observed values of its parents to a tuple and link them to
    the node as a named argument observed.
_parameter : bool, optional
    Indicates that the node is a parameter node


The compilation and data loading phases
---------------------------------------

The compilation of the computation graph is separated from the loading of the data for
making it possible to reuse the compiled model. The loader objects are passed the
context, compiled net,

"""

_current_model = None


def get_current_model():
    global _current_model
    if _current_model is None:
        _current_model = ElfiModel()
    return _current_model


def set_current_model(model=None):
    global _current_model
    if model is None:
        model = ElfiModel()
    if not isinstance(model, ElfiModel):
        raise ValueError('{} is not an instance of ElfiModel'.format(ElfiModel))
    _current_model = model


def random_name(length=4, prefix=''):
    return prefix + str(uuid.uuid4().hex[0:length])


# TODO: make this a property of algorithm that runs the inference
class ComputationContext:
    """

    Attributes
    ----------
    seed : int
    batch_size : int
    observed : dict
    pool : elfi.OutputPool
    num_submissions : int
        Number of submissions using this context.


    """
    def __init__(self, seed=None, batch_size=None, observed=None, pool=None):
        """

        Parameters
        ----------
        seed : int, False, None (default)
            - When None, generates a random integer seed.
            - When False, numpy's global random_state will be used in all computations.
              Used for testing.
        batch_size : int
        observed : dict
        pool : elfi.OutputPool

        """

        # Extract the seed from numpy RandomState. Alternative would be to use
        # os.urandom(4) casted as int.
        self.seed = seed or np.random.RandomState().get_state()[1][0]
        self.batch_size = batch_size or 1
        self.observed = observed or {}

        # Count the number of submissions from this context
        self.num_submissions = 0
        # Must be the last one to be set because uses this context in initialization
        self.pool = pool

    @property
    def pool(self):
        return self._pool

    @pool.setter
    def pool(self, pool):
        if pool is not None:
            pool.init_context(self)
        self._pool = pool

    def callback(self, batch, batch_index):
        if self.pool:
            self.pool.add_batch(batch, batch_index)

    def copy(self):
        return copy.copy(self)


class ElfiModel(GraphicalModel):
    def __init__(self, name=None, source_net=None, computation_context=None,
                 set_current=True):
        """Create a new ElfiModel instance

        Parameters
        ----------
        name : str, optional
        source_net : nx.DiGraph, optional
        computation_context : elfi.ComputationContext, optional
        set_current : bool, optional
            Sets this model as the current ELFI model
        """

        super(ElfiModel, self).__init__(source_net)
        self.name = name or "model_{}".format(random_name())
        # TODO: remove computation context from model
        self.computation_context = computation_context or ComputationContext()

        if set_current:
            set_current_model(self)

    @property
    def name(self):
        return self.source_net.graph['name']

    @name.setter
    def name(self, name):
        self.source_net.graph['name'] = name

    def generate(self, batch_size=1, outputs=None, with_values=None):
        """Generates a batch using the global seed. Useful for testing.

        Parameters
        ----------
        batch_size : int
        outputs : list
        with_values : dict

        """

        if outputs is None:
            outputs = self.source_net.nodes()
        elif isinstance(outputs, str):
            outputs = [outputs]
        if not isinstance(outputs, list):
            raise ValueError('Outputs must be a list of node names')

        context = self.computation_context.copy()
        # Use the global random_state
        context.seed = False
        context.batch_size = batch_size
        if with_values is not None:
            pool = OutputPool(with_values.keys())
            pool.add_batch(with_values, 0)
            context.pool = pool

        client = elfi.client.get_client()
        compiled_net = client.compile(self.source_net, outputs)
        loaded_net = client.load_data(compiled_net, context, batch_index=0)
        return client.compute(loaded_net)

    def get_reference(self, name):
        cls = self.get_node(name)['_class']
        return cls.reference(name, self)

    def update_node(self, node, updating_node):
        # Change the observed data
        self.observed.pop(node, None)
        if updating_node in self.observed:
            self.observed[node] = self.observed.pop(updating_node)

        super(ElfiModel, self).update_node(node, updating_node)


    @property
    def observed(self):
        return self.computation_context.observed

    @property
    def parameters(self):
        """Returns a list of parameters in an alphabetical order."""
        return sorted([n for n in self.nodes if '_parameter' in self.get_state(n)])

    @parameters.setter
    def parameters(self, parameters):
        """Set the model parameter nodes.
        
        For each node name in parameters, the corresponding node will be marked as being a
        parameter node. Other nodes will be marked as not being parameter nodes.
        
        Parameters
        ----------
        parameters : iterable
            Iterable of parameter names
        
        Returns
        -------
        None
        """
        parameters = set(parameters)
        for n in self.nodes:
            state = self.get_state(n)
            if n in parameters:
                parameters.remove(n)
                state['_parameter'] = True
            else:
                if '_parameter' in state: state.pop('_parameter')
        if len(parameters) > 0:
            raise ValueError('Parameters {} not found from the model'.format(parameters))

    def __copy__(self):
        kopy = super(ElfiModel, self).__copy__(set_current=False)
        kopy.computation_context = self.computation_context.copy()
        kopy.name = "{}_copy_{}".format(self.name, random_name())
        return kopy

    def __getitem__(self, node_name):
        return self.get_reference(node_name)


class InstructionsMapper:
    @property
    def state(self):
        raise NotImplementedError()

    @property
    def uses_meta(self):
        return self.state.get('_uses_meta', False)

    @uses_meta.setter
    def uses_meta(self, val):
        self.state['_uses_meta'] = True


class NodeReference(InstructionsMapper):
    """This is a base class for reference objects to nodes that a user of ELFI will
    typically use, e.g. `elfi.Prior` or `elfi.Simulator` to create state dictionaries for
    nodes.

    Each node has a state dictionary that describes how the node ultimately produces its
    output (see module documentation for more details). The state is stored in the
    `ElfiModel` so that serializing the model is straightforward. `NodeReference` and it's
    subclasses are convenience classes that make it easy to manipulate the state. They
    only contain a reference to the corresponding state in the `ElfiModel`.

    Examples
    --------
    ::

        elfi.Simulator(fn, arg1, ...)

    creates a node to `self.model.source_net` with the following state dictionary::

        dict(_operation=fn, _class=elfi.Simulator, ...)

    and adds and edge from arg1 to to the new simulator node in the
    `self.model.source_net`.

    """
    def __init__(self, *parents, state=None, model=None, name=None):
        """

        Parameters
        ----------
        parents : variable
        name : string
            If name ends in an asterisk '*' character, the asterisk will be replaced with
            a random string and the name is ensured to be unique within the model.
        state : dict
        model : elfi.ElfiModel

        Examples
        --------
        >>> node = NodeReference(name='name*') # doctest: +SKIP
        >>> node.name # doctest: +SKIP
        name_1f4rgh

        """
        state = state or {}
        state['_class'] = self.__class__
        model = self._determine_model(model, parents)

        name = self._give_name(name, model)
        model.add_node(name, state)

        self._init_reference(name, model)
        self._add_parents(parents)

    def _add_parents(self, parents):
        for parent in parents:
            if not isinstance(parent, NodeReference):
                parent_name = self._new_name('_' + self.name)
                parent = Constant(parent, name=parent_name, model=self.model)
            self.model.add_edge(parent.name, self.name)

    def _determine_model(self, model, parents):
        if not isinstance(model, ElfiModel) and model is not None:
            return ValueError('Invalid model passed {}'.format(model))

        # Check that parents belong to the same model and inherit the model if needed
        for p in parents:
            if isinstance(p, NodeReference):
                if model is None:
                    model = p.model
                elif model != p.model:
                    raise ValueError('Parents are from different models!')

        if model is None:
            model = get_current_model()

        return model

    @property
    def parents(self):
        """

        Returns
        -------
        parents : list
            List of positional parents
        """
        return [self.model[p] for p in self.model.parent_names(self.name)]

    @classmethod
    def reference(cls, name, model):
        """Creates a reference for an existing node

        Parameters
        ----------
        name : string
            name of the node
        model : ElfiModel

        Returns
        -------
        NodePointer instance
        """
        instance = cls.__new__(cls)
        instance._init_reference(name, model)
        return instance

    def become(self, other_node):
        """Replaces self state with other_node's state and updates the class

        Parameters
        ----------
        other_node : NodeReference

        """
        if other_node.model is not self.model:
            raise ValueError('The other node belongs to a different model')

        self.model.update_node(self.name, other_node.name)

        # Update the reference class
        _class = self.state.get('_class', NodeReference)
        if not isinstance(self, _class):
            self.__class__ = _class

        # Update also the other node reference
        other_node.name = self.name
        other_node.model = self.model

    def _init_reference(self, name, model):
        """Initializes all internal variables of the instance

        Parameters
        ----------
        name : name of the node in the model
        model : ElfiModel

        """
        self.name = name
        self.model = model

    def generate(self, batch_size=1, with_values=None):
        """Generates a batch. Useful for testing.

        Parameters
        ----------
        batch_size : int
        with_values : dict

        """
        result = self.model.generate(batch_size, self.name, with_values=with_values)
        return result[self.name]

    def _give_name(self, name, model):
        if name is not None:
            if name[-1] == '*':
                # Generate unique name
                name = self._new_name(name[:-1], model)
            return name

        # Test if context info is available and try to give the same name as the variable
        # Please note that this is only a convenience method which is not guaranteed to
        # work in all cases. If you require a specific name, pass the name argument.
        frame = inspect.currentframe()
        if frame:
            # Frames are available
            # Take the callers frame
            frame = frame.f_back.f_back
            info = inspect.getframeinfo(frame, 1)

            # Skip super calls to find the assignment frame
            while re.match('\s*super\(', info.code_context[0]):
                frame = frame.f_back
                info = inspect.getframeinfo(frame, 1)

            # Match simple direct assignment with the class name, no commas or semicolons
            # Also do not accept a name starting with an underscore
            rex = '\s*([^\W_][\w]*)\s*=\s*\w?[\w\.]*{}\('.format(self.__class__.__name__)
            match = re.match(rex, info.code_context[0])
            if match:
                name = match.groups()[0]
                # Return the same name as the assgined reference
                if not model.has_node(name):
                    return name

        # Inspecting the name failed, return a random name
        return self._new_name(model=model)

    def _new_name(self, basename='', model=None):
        model = model or self.model
        if not basename:
            basename = '_{}'.format(self.__class__.__name__.lower())
        while True:
            name = "{}_{}".format(basename, random_name())
            if not model.has_node(name): break
        return name

    @property
    def state(self):
        if self.model is None:
            raise ValueError('{} {} is not initialized'.format(self.__class__.__name__,
                                                               self.name))
        return self.model.get_node(self.name)

    def __getitem__(self, item):
        """Get item from the state dict of the node
        """
        return self.state[item]

    def __setitem__(self, item, value):
        """Set item into the state dict of the node
        """
        self.state[item] = value

    def __repr__(self):
        return "{}(name='{}')".format(self.__class__.__name__, self.name)

    def __str__(self):
        return self.name


class StochasticMixin(NodeReference):
    def __init__(self, *parents, state, **kwargs):
        # Flag that this node is stochastic
        state['_stochastic'] = True
        super(StochasticMixin, self).__init__(*parents, state=state, **kwargs)


class ObservableMixin(NodeReference):
    """
    """

    def __init__(self, *parents, state, observed=None, **kwargs):
        # Flag that this node can be observed
        state['_observable'] = True
        super(ObservableMixin, self).__init__(*parents, state=state, **kwargs)

        # Set the observed value
        if observed is not None:
            self.model.computation_context.observed[self.name] = observed

    @property
    def observed(self):
        obs_name = observed_name(self.name)
        result = self.model.generate(0, obs_name)
        return result[obs_name]


# User interface nodes


class Constant(NodeReference):
    def __init__(self, value, **kwargs):
        state = dict(_output=value)
        super(Constant, self).__init__(state=state, **kwargs)


class Operation(NodeReference):
    """A generic operation node.
    """
    def __init__(self, fn, *parents, **kwargs):
        state = dict(_operation=fn)
        super(Operation, self).__init__(*parents, state=state, **kwargs)


class RandomVariable(StochasticMixin, NodeReference):
    def __init__(self, distribution, *params, size=None, **kwargs):
        """

        Parameters
        ----------
        distribution : str or scipy-like distribution object
        params : params of the distribution
        size : int, tuple or None, optional
            size of a single random draw. None (default) means a scalar.

        """

        state = dict(distribution=distribution,
                     size=size,
                     _uses_batch_size=True)
        state['_operation'] = self.compile_operation(state)
        super(RandomVariable, self).__init__(*params, state=state, **kwargs)

    @staticmethod
    def compile_operation(state):
        size = state['size']
        distribution = state['distribution']
        if not (size is None or isinstance(size, tuple)):
            size = (size, )

        # Note: sending the scipy distribution object also pickles the global numpy random
        # state with it. If this needs to be avoided, the object needs to be constructed
        # on the worker.
        if isinstance(distribution, str):
            distribution = scipy_from_str(distribution)

        if not hasattr(distribution, 'rvs'):
            raise ValueError("Distribution {} "
                             "must implement a rvs method".format(distribution))

        op = partial(rvs_from_distribution, distribution=distribution, size=size)
        return op

    @property
    def distribution(self):
        distribution = self['distribution']
        if isinstance(distribution, str):
            distribution = scipy_from_str(distribution)
        return distribution

    @property
    def size(self):
        return self['size']

    def __repr__(self):
        d = self.distribution

        if isinstance(d, str):
            name = "'{}'".format(d)
        elif hasattr(d, 'name'):
            name = "'{}'".format(d.name)
        elif isinstance(d, type):
            name = d.__name__
        else:
            name = d.__class__.__name__

        return super(RandomVariable, self).__repr__()[0:-1] + ", {})".format(name)


class Prior(RandomVariable):
    def __init__(self, distribution="uniform", *params, **kwargs):
        super(Prior, self).__init__(distribution, *params, **kwargs)
        self['_parameter'] = True


class Simulator(StochasticMixin, ObservableMixin, NodeReference):
    def __init__(self, fn, *params, **kwargs):
        state = dict(_operation=fn, _uses_batch_size=True)
        super(Simulator, self).__init__(*params, state=state, **kwargs)


class Summary(ObservableMixin, NodeReference):
    def __init__(self, fn, *parents, **kwargs):
        if not parents:
            raise ValueError('This node requires that at least one parent is specified.')
        state = dict(_operation=fn)
        super(Summary, self).__init__(*parents, state=state, **kwargs)


class Discrepancy(NodeReference):
    def __init__(self, discrepancy, *parents, **kwargs):
        """Discrepancy node.

        Parameters
        ----------
        discrepancy : callable
            Signature of the discrepancy function is of the form:
            `discrepancy(summary_1, summary_2, ..., observed)`, where:
            summary_i : array-like
                containing n simulated values of summary_i in its elements, where n is the
                batch size.

            The callable should return a vector of n discrepancies between the simulated
            summaries and the observed summaries.
        observed : tuple
            tuple (observed_summary_1, observed_summary_2, ...)

        See Also
        --------
        See the `elfi.Distance` for creating common distance discrepancies.

        """
        if not parents:
            raise ValueError('This node requires that at least one parent is specified.')
        state = dict(_operation=discrepancy, _uses_observed=True)
        super(Discrepancy, self).__init__(*parents, state=state, **kwargs)


# TODO: add weights
class Distance(Discrepancy):
    def __init__(self, distance, *summaries, p=None, w=None, V=None, VI=None, **kwargs):
        """Distance node.

        The summaries will be first stacked to a single 2D array with the simulated
        summaries in the rows for every simulation and the distance is taken row
        wise against the corresponding observed summary vector.

        Parameters
        ----------
        distance : callable, str
            Signature of the callable distance function is of the form: `distance(X, Y)`,
            where
            X : np.ndarray
                n x m array containing n simulated values (summaries) in rows
            Y : np.ndarray
                1 x m array that containing the observed values (summaries) in the row
            If string, it must be a valid metric for `scipy.spatial.distance.cdist`.

            The callable should return a vector of distances between the simulated
            summaries and the observed summaries.
        summaries
        p : double, optional
            The p-norm to apply Only for distance Minkowski (`'minkowski'`), weighted
            and unweighted. Default: 2.
        w : ndarray, optional
            The weight vector. Only for weighted Minkowski (`'wminkowski'`). Mandatory.
        V : ndarray, optional
            The variance vector. Only for standardized Euclidean (`'seuclidean'`).
            Mandatory.
        VI : ndarray, optional
            The inverse of the covariance matrix. Only for Mahalanobis. Mandatory.

        Examples
        --------
        >>> d = elfi.Distance('euclidean', summary1, summary2...) # doctest: +SKIP

        >>> d = elfi.Distance('minkowski', summary, p=1) # doctest: +SKIP

        Notes
        -----
        Your summaries need to be scalars or vectors for this method to work.

        See Also
        --------
        https://docs.scipy.org/doc/scipy/reference/generated/generated/scipy.spatial.distance.cdist.html

        """
        if not summaries:
            raise ValueError("This node requires that at least one parent is specified.")

        if isinstance(distance, str):
            if distance == 'wminkowski' and w is None:
                raise ValueError('Parameter w must be specified for distance=wminkowski.')
            if distance == 'seuclidean' and V is None:
                raise ValueError('Parameter V must be specified for distance=seuclidean.')
            if distance == 'mahalanobis' and VI is None:
                raise ValueError('Parameter VI must be specified for distance=mahalanobis.')
            cdist_kwargs = dict(metric=distance, p=p, w=w, V=V, VI=VI)
            dist_fn = partial(scipy.spatial.distance.cdist, **cdist_kwargs)
        else:
            dist_fn = distance
        discrepancy = partial(distance_as_discrepancy, dist_fn)
        super(Distance, self).__init__(discrepancy, *summaries, **kwargs)
        # Store the original passed distance
        self.state['distance'] = distance
