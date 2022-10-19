from unittest import TestCase

from avion.di.container import Container


class TestContainer(TestCase):
    def test_container_can_resolve_single_dependency(self) -> None:
        class HttpClient: pass

        class Service:
            def __init__(self, http: HttpClient):
                self.http = http

        c = Container()
        c.resolve(HttpClient).using(HttpClient)
        c.resolve(Service).using(Service)

        instance = c.get_instance(Service)
        self.assertIsInstance(instance, Service)
        self.assertIsInstance(instance.http, HttpClient)
