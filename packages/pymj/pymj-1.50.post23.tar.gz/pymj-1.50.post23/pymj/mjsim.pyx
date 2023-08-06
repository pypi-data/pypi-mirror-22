
cdef class MjSim(object):
    """
    Wrapper around PyMjModel and PyMjData with extra functionality for
    advancing the simulation dynamics and keeping a buffer between steps.

    The XML used to create the internal model is accessible if the model was
    created by load_model_from_xml(), and is at `self.model.xml`.

    MuJoCo can serialize a model to XML for you, and this is done using the
    save_model_to_xml() method.  For example:
        save_model_to_xml(self.model)
    """
    # MjRenderContext for rendering camera views.
    cdef readonly list render_contexts
    cdef readonly object _render_context_window
    cdef readonly object _render_context_offscreen

    # MuJoCo model
    cdef readonly PyMjModel model
    # MuJoCo data
    cdef readonly PyMjData data
    # Number of substeps when calling .step
    cdef readonly int nsubsteps
    # User defined state.
    cdef readonly dict udd_state
    # User defined dynamics callback
    cdef readonly object _udd_callback
    # Allows to store extra information in MjSim.
    cdef readonly dict extras

    def __cinit__(self, PyMjModel model, PyMjData data=None, int nsubsteps=1,
                  udd_callback=None):
        """
        Args:
            - model (PyMjModel): model to simulate.
            - data (PyMjData): stores the simulation data. Will be created
                if not provided.
            - nsubsteps (int): number of substeps to run on `.step`. Buffers
                will be swapped only once per step.
            - udd_callback: callback for the user-defined dynamics. It
                takes an MjSim object as the current state and returns the
                next udd_state after applying dynamics. Useful for reward
                functions that operate over functions of historical state.
        """
        self.nsubsteps = nsubsteps
        self.model = model
        if data is None:
            with wrap_mujoco_warning():
                _data = mj_makeData(self.model.ptr)
            if _data == NULL:
                raise Exception('mj_makeData failed!')
            self.data = WrapMjData(_data, self.model)
        else:
            self.data = data

        self.render_contexts = []
        self._render_context_offscreen = None
        self._render_context_window = None
        self.udd_state = None
        self.udd_callback = udd_callback
        self.extras = {}

    def reset(self):
        """
        Resets the simulation data and clears buffers.
        """
        with wrap_mujoco_warning():
            mj_resetData(self.model.ptr, self.data.ptr)

        self.udd_state = None
        self.step_udd()

    def forward(self):
        """
        Calls `mj_forward`.
        """
        with wrap_mujoco_warning():
            mj_forward(self.model.ptr, self.data.ptr)

    def step(self):
        """
        Calls `mj_step`, with `nsubsteps` as specified on `MjSim` instance creation.

        If qpos or qvel have been modified directly, the user is required to call
        forward before step if their udd_callback requires access to Mujoco state
        set during the forward dynamics.
        """
        self.step_udd()

        with wrap_mujoco_warning():
            for _ in range(self.nsubsteps):
                mj_step(self.model.ptr, self.data.ptr)

    def render(self, width=None, height=None, *, camera_name=None, depth=False,
               mode='offscreen'):
        """
        Renders view from a camera and returns image as an `numpy.ndarray`.

        Args:
        - width (int): desired image width.
        - height (int): desired image height.
        - camera_name (str): name of camera in model. If None, the free
            camera will be used.
        - depth (bool): if True, also return depth buffer

        Returns:
        - rgb (uint8 array): image buffer from camera
        - depth (float array): depth buffer from camera (only returned
            if depth=True)
        """
        if camera_name is None:
            camera_id = None
        else:
            camera_id = self.model.camera_name2id(camera_name)

        if mode == 'offscreen':
            if self._render_context_offscreen is None:
                render_context = MjRenderContextOffscreen(self)
            else:
                render_context = self._render_context_offscreen

            render_context.render(
                width=width, height=height, camera_id=camera_id)
            return render_context.read_pixels(
                width, height, depth=depth)
        elif mode == 'window':
            if self._render_context_window is None:
                from pymj.mjviewer import MjViewer
                render_context = MjViewer(self)
            else:
                render_context = self._render_context_window

            render_context.render()

        else:
            raise ValueError("Mode must be either 'window' or 'offscreen'.")

    def add_render_context(self, render_context):
        self.render_contexts.append(render_context)
        if render_context.offscreen and self._render_context_offscreen is None:
            self._render_context_offscreen = render_context
        elif not render_context.offscreen and self._render_context_window is None:
            self._render_context_window = render_context

    @property
    def udd_callback(self):
        return self._udd_callback

    @udd_callback.setter
    def udd_callback(self, value):
        self._udd_callback = value
        self.udd_state = None
        self.step_udd()

    def step_udd(self):
        if self._udd_callback is None:
            self.udd_state = {}
        else:
            schema_example = self.udd_state
            self.udd_state = self._udd_callback(self)
            # Check to make sure the udd_state has consistent keys and dimension across steps
            if schema_example is not None:
                keys = set(schema_example.keys()) | set(self.udd_state.keys())
                for key in keys:
                    assert key in schema_example, "Keys cannot be added to udd_state between steps."
                    assert key in self.udd_state, "Keys cannot be dropped from udd_state between steps."
                    if isinstance(schema_example[key], Number):
                        assert isinstance(self.udd_state[key], Number), \
                            "Every value in udd_state must be either a number or a numpy array"
                    else:
                        assert isinstance(self.udd_state[key], np.ndarray), \
                            "Every value in udd_state must be either a number or a numpy array"
                        assert self.udd_state[key].shape == schema_example[key].shape, \
                            "Numpy array values in udd_state must keep the same dimension across steps."

    def get_state(self):
        """ Returns a copy of the simulator state. """
        qpos = np.copy(self.data.qpos)
        qvel = np.copy(self.data.qvel)
        if self.model.na == 0:
            act = None
        else:
            act = np.copy(self.data.act)
        udd_state = copy.deepcopy(self.udd_state)

        return MjSimState(self.data.time, qpos, qvel, act, udd_state)

    def set_state(self, value):
        """
        Sets the state from an MjSimState.
        If the MjSimState was previously unflattened from a numpy array, consider
        set_state_from_flattened, as the defensive copy is a substantial overhead
        in an inner loop.

        Args:
        - value (MjSimState): the desired state.
        - call_forward: optionally call sim.forward(). Called by default if
            the udd_callback is set.
        """
        self.data.time = value.time
        self.data.qpos[:] = np.copy(value.qpos)
        self.data.qvel[:] = np.copy(value.qvel)
        if self.model.na != 0:
            self.data.act[:] = np.copy(value.act)
        self.udd_state = copy.deepcopy(value.udd_state)

    def set_state_from_flattened(self, value):
        """ This helper method sets the state from an array without requiring a defensive copy."""
        state = MjSimState.from_flattened(value, self)

        self.data.time = state.time
        self.data.qpos[:] = state.qpos
        self.data.qvel[:] = state.qvel
        if self.model.na != 0:
            self.data.act[:] = state.act
        self.udd_state = state.udd_state
