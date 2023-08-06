
class MjSimState(namedtuple('SimStateBase', 'qpos qvel udd_state')):
    """ Represents the full state of the simulator."""
    __slots__ = ()

    # need to implement this because numpy doesn't support == on arrays
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented

        if set(self.udd_state.keys()) != set(other.udd_state.keys()):
            return False

        for k in self.udd_state.keys():
            if isinstance(self.udd_state[k], Number) and self.udd_state[k] != other.udd_state[k]:
                return False
            elif not np.array_equal(self.udd_state[k], other.udd_state[k]):
                return False

        return np.array_equal(self.qpos, other.qpos) and np.array_equal(self.qvel, other.qvel)

    def __ne__(self, other):
        return not self.__eq__(other)

    def flatten(self):
        """ Flattens a state into a numpy array of numbers."""
        return np.concatenate((self.qpos, self.qvel, MjSimState._flatten_dict(self.udd_state)))

    @staticmethod
    def _flatten_dict(d):
        a = []
        for k in sorted(d.keys()):
            v = d[k]
            if isinstance(v, Number):
                a.extend([v])
            else:
                a.extend(v.ravel())

        return np.array(a)

    @staticmethod
    def from_flattened(array, sim):
        dim_qpos = sim.data.qpos.shape[0]
        dim_qvel = sim.data.qvel.shape[0]

        qpos = array[:dim_qpos]
        qvel = array[dim_qpos:dim_qpos + dim_qvel]
        flat_udd_state = array[dim_qpos + dim_qvel:]
        udd_state = MjSimState._unflatten_dict(flat_udd_state, sim.udd_state)

        return MjSimState(qpos, qvel, udd_state)

    @staticmethod
    def _unflatten_dict(a, schema_example):
        d = {}
        idx = 0
        for k in sorted(schema_example.keys()):
            schema_val = schema_example[k]
            if isinstance(schema_val, Number):
                val = a[idx]
                idx += 1
                d[k] = val
            else:
                assert isinstance(schema_val, np.ndarray)
                val_array = a[idx:idx+schema_val.size]
                idx += schema_val.size
                val = np.array(val_array).reshape(schema_val.shape)
                d[k] = val
        return d

