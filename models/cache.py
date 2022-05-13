import aioredis

redis = aioredis.from_url('redis://localhost', encoding='utf-8', decode_responses=True)

MAILING = 'mailing'
