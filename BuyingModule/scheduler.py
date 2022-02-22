from datetime import datetime, timedelta

import pytz

from BuyingModule.celery_task import buy_nft
from ScraperModule.SeleniumService.selenium_executor import SeleniumExecutor

print(datetime.now(pytz.utc))
buy_nft.apply_async(eta=datetime.now(pytz.utc)+timedelta(seconds=15), kwargs={"executor": 'run'})
