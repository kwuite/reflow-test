"""
reflow.main
"""

import asyncio
from typing import Any, Tuple

from reflow.base.intro import Intro
from reflow.base.protocols import IntroProtocol
from reflow.reflow import Reflow
from reflow.schema.constructor import SchemaConstructor


async def main():
    contract = {
        'uuid': '7066f4b3-2790-48ab-a832-8fcfb6daf45a',
        'type': 'execute',
        'execute': {
            'flows': [
                'reflow.stores.fetched_api_data',
                'reflow.extractors.extracted_token_id',
                'reflow.stores.saved_data',
                'reflow.extractors.extracted_api_url',
                'reflow.signals.read',
                'reflow.stores.translated_data',
                'reflow.extractors.extracted_locale',
                'reflow.base.query',
                'reflow.stores.connection',
            ]
        },
        'input': {
            'api_url': 'https://kelvin.io/api/v1',
            'token_id': 'SeWT29Dz',
            'db_host': '127.0.0.1',
            'db_port': 5432,
            'db_user': 'admin',
            'db_password': 'password',
            'db_name': 'test',
            'locale': 'en',
        },
    }

    # get the flowables
    intro: Intro = Intro(contract=contract)
    resolved_intro: IntroProtocol = await intro.output()
    flowables: Tuple[Any] = resolved_intro.contract._flowables
    flowables += (intro, )

    reflow = Reflow(name='Text translation flow').run_pipeline(flowables)
    resolved = await reflow.activate()

    schema_constructor = SchemaConstructor(reflow=reflow)

    # uml_schema = schema_constructor.as_uml_schema()
    # reflow_as_uml = uml_schema.schema
    # await uml_schema.save_to_file(file_name='reflow_as_uml')
    # print('Reflow as UML:')
    # print(reflow_as_uml)
    # print('\n')

    # d2_schema = reflow.as_d2_schema()
    # reflow_as_d2 = d2_schema.schema
    # await d2_schema.save_to_file(file_name='reflow_as_d2')
    # print('Reflow as D2:')
    # print(reflow_as_d2)
    # print('\n')

    print(resolved)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
