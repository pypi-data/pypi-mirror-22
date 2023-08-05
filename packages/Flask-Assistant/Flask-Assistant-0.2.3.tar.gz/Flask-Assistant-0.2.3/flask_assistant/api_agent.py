from flask import json

from flask_assistant.core import Assistant

class ApiAiAgent(Assistant):
    """Creates an object used to communicate with API.Assistant.

        Agents receive requests directly from API.AI, and respond with API.AI responses
        """
    def __init__(self, app=None,):
        super(Agent, self).__init__(app)


    @property
    def context_in(self):
        """Local Proxy refering to context objects contained within current session"""
        return getattr(_app_ctx_stack.top, '_assist_context_in', [])

    @context_in.setter
    def context_in(self, value):
        _app_ctx_stack.top._assist_context_in = value

    @property
    def context_manager(self):
        """LocalProxy refering to the app's instance of the  :class: `ContextManager`.

        Interface for adding and accessing contexts and their parameters
        """
        return getattr(_app_ctx_stack.top, '_assist_context_manager', ContextManager())

    @context_manager.setter
    def context_manager(self, value):
        _app_ctx_stack.top._assist_context_manager = value

    @property
    def session_id(self):
        return getattr(_app_ctx_stack.top, '_assist_session_id', None)

    def _register_context_to_func(self, intent_name, context=[]):
        required = self._required_contexts.get(intent_name)
        if required:
            required.extend(context)
        else:
            self._required_contexts[intent_name] = []
            self._required_contexts[intent_name].extend(context)

    def context(self, *context_names):

        def decorator(f):
            func_requires = self._func_contexts.get(f)

            if not func_requires:
                self._func_contexts[f] = []

            self._func_contexts[f].extend(context_names)

            def wrapper(*args, **kw):
                return f(*args, with_context=context_names, **kw)
            return wrapper
        return decorator


    def prompt_for(self, next_param, intent):
        """Decorates a function to prompt for an action's required parameter.

        The wrapped function is called if next_param was not recieved with the given intent's
        request and is required for the fulfillment of the intent's action.

        Arguments:
            next_param {str} -- name of the parameter required for action function
            intent_name {str} -- name of the intent the dependent action belongs to
        """
        def decorator(f):
            prompts = self._intent_prompts.get(intent)
            if prompts:
                prompts[next_param] = f
            else:
                self._intent_prompts[intent] = {}
                self._intent_prompts[intent][next_param] = f

            @wraps(f)
            def wrapper(*args, **kw):
                self._flask_assitant_view_func(*args, **kw)
            return f
        return decorator

    def fallback(self):
        def decorator(f):
            self._fallback_response = f
            return f

    def _api_request(self, verify=True):
        raw_body = flask_request.data
        _api_request_payload = json.loads(raw_body)

        return _api_request_payload

    def _match_view_func(self):

        view_func = None

        if self.context_in:
            view_func = self._choose_context_view()

        elif self._missing_params:
            prompts = self._intent_prompts.get(self.intent)
            if prompts:
                param_choice = self._missing_params.pop()
                view_func = prompts.get(param_choice)

        elif len(self._intent_action_funcs[self.intent]) == 1:
            view_func = self._intent_action_funcs[self.intent][0]

        if not view_func:
            view_func = self._intent_action_funcs[self.intent][0]
            _errordump('No view func matched')
            _errordump({
                'intent recieved': self.intent,
                'recieved parameters': self.request['result']['parameters'],
                'required args': self._func_args(view_func),
                'conext_in': self.context_in,
                'matched view_func': view_func.__name__
            })

        return view_func

    def _dump_view_info(self, view_func=lambda: None):
        _infodump('Result: Matched {} intent to {} func'.format(self.intent, view_func.__name__))


    def _parse_request_payload(self):
        self.request = self._api_request(verify=False)
        _dbgdump(self.request['result'])

        self.intent = self.request['result']['metadata']['intentName']
        self.context_in = self.request['result'].get('contexts', [])
        self._update_contexts()


    def _update_contexts(self):
        temp = self.context_manager
        temp.update(self.context_in)
        self.context_manager = temp


    @property
    def _context_views(self):
        """Returns view functions for which the context requirements are met"""
        possible_views = []
        recieved_contexts = [c['name'] for c in self.context_in]
        # recieved_contexts = [c['name'] for c in self.context_manager.active]


        for func in self._func_contexts:
            requires = list(self._func_contexts[func])
            met = []
            for req_context in requires:
                if req_context in recieved_contexts:
                    met.append(req_context)

            if set(met) == set(requires) and len(requires) <= len(recieved_contexts):
                # if not requires:
                # import ipdb; ipdb.set_trace()
                possible_views.append(func)

        return possible_views

    def _choose_context_view(self):
        choice = None
        for view in self._context_views:
            if view in self._intent_action_funcs[self.intent]:
                choice = view
        if choice:
            return choice
        else:
            _errordump('')
            _errordump('No view matched for {} with context'.format(self.intent))
            _errordump('intent: {}'.format(self.intent))
            _errordump('possible biews: {}'.format(self._context_views))
            _errordump('intent action funcs: {}'.format(self._intent_action_funcs[self.intent]))

    @property
    def _missing_params(self):  # TODO: fill missing slot from default
        params = self.request['result']['parameters']
        missing = []
        for p_name in params:
            if params[p_name] == '':
                missing.append(p_name)

        return missing

    def _func_args(self, f):
        argspec = inspect.getargspec(f)
        return argspec.args

    def _map_intent_to_view_func(self, view_func):
        arg_names = self._func_args(view_func)
        arg_values = self._map_params_to_view_args(arg_names)
        return partial(view_func, *arg_values)

    def _map_params_to_view_args(self, arg_names): # TODO map to correct name
        arg_values = []
        mapping = self._intent_mappings.get(self.intent)
        params = self.request['result']['parameters']

        for arg_name in arg_names:
            entity_mapping = mapping.get(arg_name, arg_name)
            # param name cant have '.',
            # so when registered, the sys. is stripped,
            # and must be stripped when looking up in request
            mapped_param_name = entity_mapping.replace('sys.', '') 
            value = params.get(mapped_param_name)  # params declared in GUI present in request
            
            if not value:  # params not declared, so must look in contexts
                value = self._map_arg_from_context(arg_name)
            arg_values.append(value)

        return arg_values

    def _map_arg_from_context(self, arg_name):
        for context_obj in self.context_in:
            if arg_name in context_obj['parameters']:
                return context_obj['parameters'][arg_name]


def _dbgdump(obj, indent=2, default=None, cls=None):
    msg = json.dumps(obj, indent=indent, default=default, cls=cls)
    logger.debug(msg)


def _infodump(obj, indent=2, default=None, cls=None):
    msg = json.dumps(obj, indent=indent, default=default, cls=cls)
    logger.info(msg)


def _warndump(obj, indent=2, default=None, cls=None):
    msg = json.dumps(obj, indent=indent, default=default, cls=cls)
    logger.warn(msg)


def _errordump(obj, indent=2, default=None, cls=None):
    msg = json.dumps(obj, indent=indent, default=default, cls=cls)
    logger.error(msg)


        