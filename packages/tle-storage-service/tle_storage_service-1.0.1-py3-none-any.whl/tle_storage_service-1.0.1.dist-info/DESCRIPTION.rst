TLEStorageService
_________________

Small aiohttp server application for TLE storage


Requirements
------------

- aio-nasa-tle-loader >= 1.0.0
- aio-space-track-api >= 2.1.1
- aiohttp >= 2.1.0
- aiopg >= 0.13.0
- alembic >= 0.9.2
- pyaml >=16.12.2
- sqlalchemy >= 1.1.10
- ujson >= 1.35


Installing
__________

::

    pip install tle-storage-service


Getting started
---------------

Start aiohttp application:

.. code-block:: python

    #!/usr/bin/env python3
    # -*- coding: utf-8 -*-
    import logging
    import os

    from aiohttp import web

    from tle_storage_service import TleStorageService, load_cfg, LOG_FORMAT

    DIR = os.path.abspath(os.path.dirname(__file__))


    if __name__ == '__main__':
        logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
        app = TleStorageService(config=load_cfg(path=os.path.join(DIR, 'config', 'server.yaml')))
        web.run_app(app, port=8080)


Create periodic script for refresh db

.. code-block:: python

    #!/usr/bin/env python3
    # -*- coding: utf-8 -*-
    import asyncio
    import logging
    import os

    from aio_nasa_tle_loader import AsyncNasaTLELoader
    from aio_space_track_api import AsyncSpaceTrackApi
    from aiopg.sa import create_engine

    from tle_storage_service import periodic_task, load_cfg, nasa, space_track, LOG_FORMAT

    DIR = os.path.abspath(os.path.dirname(__file__))
    CFG = load_cfg(path=os.path.join(DIR, 'config', 'periodic.yaml'))

    logger = logging.getLogger(__name__)


    @periodic_task(CFG['sync'].get('space-track', 4) * 3600)
    async def call_space_track(engine, api_params, satellites, loop):
        async with AsyncSpaceTrackApi(loop=loop, **api_params) as api:
            await space_track(engine, api, satellites)


    @periodic_task(CFG['sync'].get('nasa', 0.5) * 3600)
    async def call_nasa(engine, loop):
        async with AsyncNasaTLELoader(loop=loop) as loader:
            await nasa(engine, loader)


    async def run(db_params, api_params, satellites, loop):
        async with create_engine(loop=loop, **db_params) as engine:
            await asyncio.gather(
                call_nasa(engine, loop),
                call_space_track(engine, api_params, satellites, loop),
                loop=loop
            )


    def notify_callback(msg):
        logger.info('[%s] Receive msg <- "%s"', msg.channel, msg.payload)


    if __name__ == '__main__':

        logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)

        loop = asyncio.get_event_loop()
        loop.create_task(run(CFG['db'],
                             CFG['space-track'],
                             CFG['sync']['satellites'],
                             loop))

        try:
            loop.run_forever()
        finally:
            loop.close()


More code examples into `examples` directory

Source code
-----------

The latest developer version is available in a github repository:
https://github.com/nkoshell/tle-storage-service

