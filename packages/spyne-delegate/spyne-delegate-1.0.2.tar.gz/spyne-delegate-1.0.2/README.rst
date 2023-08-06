==============
Spyne Delegate
==============

Extension for spyne so you can easy override services using delegate classes.

Example usage:

.. code:: python

    import logging

    from wsgiref.simple_server import make_server
    from wsgiref.validate import validator

    from spyne import Application, Unicode
    from spyne import rpc as original_spyne_rpc

    from spyne.model.complex import ComplexModel
    from spyne.protocol.soap.soap11 import Soap11
    from spyne.server.wsgi import WsgiApplication

    from spynedelegate.meta import DelegateBase, ExtensibleServiceBase, rpc

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)


    # models
    class Chicken(ComplexModel):
        __namespace__ = "spyne.delegate.chicken"
        name = Unicode


    class Cow(ComplexModel):
        __namespace__ = "spyne.delegate.cow"
        name = Unicode


    # delegates
    class ChickenDelegate(DelegateBase):
        @rpc(Chicken, _returns=Chicken.customize(max_occurs='unbounded'))
        def multiplyChickens(self, chicken):  # noqa
            return [chicken, chicken]


    class CowDelegate(DelegateBase):
        @property
        def method_request_string(self):
            # you can access the context with self.ctx
            return self.ctx.method_request_string

        def gen_name(self, name):
            # and you can use self as well
            return "%s -> %s" % (self.method_request_string, name)

        @rpc(Cow, _returns=Unicode)
        def sayMooh(self, cow):  # noqa
            return self.gen_name(cow.name)

        @rpc(Cow, _returns=Unicode)
        def noInheritance(self, cow):  # noqa
            # This method won't be inherited because we set the 
            # collect_base_methods = False in the overridden delegate
            return self.gen_name(cow.name)


    class CowDelegateOverridden(CowDelegate):

        # With this property we don't expose inherited methods from the base
        # class
        collect_base_methods = False

        @rpc(Cow, _returns=Unicode)
        def sayMooh(self, cow):  # noqa
            # call the super and add a 'overridden' string
            result = super(CowDelegateOverridden, self).sayMooh(cow)
            return "%s overridden" % result

        @rpc(Unicode, _returns=Unicode)
        def generateName(self, name):
            # shows that we call a regular supermethod
            return super(CowDelegateOverridden, self).gen_name(name)


    # inheritance
    class FarmDelegate(ChickenDelegate, CowDelegateOverridden):
        pass


    # services
    class ChickenService(ExtensibleServiceBase):
        delegate = ChickenDelegate


    class FarmService(ExtensibleServiceBase):
        delegate = FarmDelegate

        @original_spyne_rpc(_returns=Unicode)
        def thisStillWorks(ctx):  # noqa
            return "Old fashioned spyne"


    farm_application = Application(
        [FarmService],
        tns='spyne.delegate.farm',
        name='farm-application',
        in_protocol=Soap11(validator='lxml'),
        out_protocol=Soap11()
    )

    if __name__ == "__main__":
        wsgi_application = WsgiApplication(farm_application)
        wsgi_server = make_server(
            'localhost', 9876, validator(wsgi_application))

        logger.info('Starting server at %s:%s.' % ('localhost', 9876))
        logger.info('WSDL is at: /?wsdl')

        wsgi_server.serve_forever()


