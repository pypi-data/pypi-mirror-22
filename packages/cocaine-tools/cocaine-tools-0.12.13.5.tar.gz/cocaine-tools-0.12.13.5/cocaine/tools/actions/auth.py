import json

import click
from cerberus import Validator

from cocaine.tools.error import ToolsError
from tornado import gen

from cocaine.decorators import coroutine

from . import Action


COLLECTION_TOKENS = 'tokens'
COLLECTION_GROUPS = 'auth-groups'


class Auth(object):
    """Auth groups is a lie"""
    def __init__(self, storage):
        self._storage = storage  # HINT: storage.write(namespace, key, value, tags)

    @coroutine
    def create_group(self, name, token, force=False):
        if not force:
            channel = yield self._storage.find(COLLECTION_GROUPS, ['auth'])
            groups = yield channel.rx.get()
            if name in groups:
                raise ToolsError('authorization group already exists')

        channel = yield self._storage.write(COLLECTION_GROUPS, name, token, ['auth'])
        yield channel.rx.get()

    @coroutine
    def view_group(self, name):
        channel = yield self._storage.read(COLLECTION_GROUPS, name)
        token = yield channel.rx.get()

        channel = yield self._storage.find(COLLECTION_TOKENS, ['auth', 'tokens', name])
        members = yield channel.rx.get()

        raise gen.Return({
            'token': token,
            'members': members,
        })

    @coroutine
    def list_groups(self):
        channel = yield self._storage.find(COLLECTION_GROUPS, ['auth'])
        value = yield channel.rx.get()
        raise gen.Return(value)

    @coroutine
    def remove_group(self, name, drop):
        channel = yield self._storage.remove(COLLECTION_GROUPS, name)
        yield channel.rx.get()

        if drop:
            channel = yield self._storage.find(COLLECTION_TOKENS, ['auth', 'tokens', name])
            members = yield channel.rx.get()

            for service_name in members:
                yield self.remove_member(name, service_name)

    @coroutine
    def add_member(self, name, service):
        channel = yield self._storage.read(COLLECTION_GROUPS, name)
        token = yield channel.rx.get()

        channel = yield self._storage.write(
            COLLECTION_TOKENS, service, token,
            ['auth', 'tokens', name],
        )
        yield channel.rx.get()

    @coroutine
    def remove_member(self, name, service):
        channel = yield self._storage.remove(COLLECTION_TOKENS, service)
        yield channel.rx.get()

    @coroutine
    def edit_group(self, name, updated):
        old = yield self.view_group(name)

        assert 'members' in updated, 'New config must contain members field'
        # Update token only if it was changed.
        if 'token' in updated and updated['token'] != old['token']:
            yield self.create_group(name, updated['token'], force=True)

            for member in set(updated['members']) & set(old['members']):
                yield self.add_member(name, member)

        # Remove excluded members while adding new ones.
        for member in set(updated['members']) - set(old['members']):
            yield self.add_member(name, member)
        for member in set(old['members']) - set(updated['members']):
            yield self.remove_member(name, member)


class AuthAction(Action):
    method = None

    def __init__(self, storage, *args, **kwargs):
        self.instance = self.method.im_class(storage)
        self.args = args
        self.kwargs = kwargs

    @coroutine
    def execute(self):
        value = yield self.method(self.instance, *self.args, **self.kwargs)
        raise gen.Return(value)


class List(AuthAction):
    method = Auth.list_groups


class Create(AuthAction):
    method = Auth.create_group


class View(AuthAction):
    method = Auth.view_group


class Remove(AuthAction):
    method = Auth.remove_group


class AddMember(AuthAction):
    method = Auth.add_member


class ExcludeMember(AuthAction):
    method = Auth.remove_member


class Edit(AuthAction):
    method = Auth.edit_group

    SCHEMA = {
        'token': {
            'type': 'string',
            'required': True,
            'regex': '^[0-9]+:.+$',
        },
        'members': {
            'type': 'list',
            'required': True,
            'schema': {
                'type': 'string',
            },
        },
    }

    def __init__(self, storage, *args, **kwargs):
        super(Edit, self).__init__(storage, *args, **kwargs)
        self._validator = Validator(self.SCHEMA)

    @coroutine
    def execute(self):
        content = yield self.instance.view_group(*self.args, **self.kwargs)
        updated = click.edit(json.dumps(content, indent=4))
        if updated is not None:
            updated = json.loads(updated)
            self._validator.validate(updated)
            if self._validator.errors:
                raise ValueError('failed to validate format: {}'.format(self._validator.errors))
            self.kwargs['updated'] = updated
            yield super(Edit, self).execute()
