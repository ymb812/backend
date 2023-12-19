import logging
from fastapi import APIRouter, HTTPException, Header, Depends
from aiogram import Bot
from core.content_sender.content_sender import lesson_sender
from core.webhooks.models import TestResultModel
from core.handlers.registration import start_of_registration
from core.db.models import Test
from core.wlui.context import WLUIContextVar
from configs.settings import env_parameters


def authorize_user(auth_token: str = Header(None)):
    if auth_token != env_parameters.AUTH_TOKEN:
        raise HTTPException(status_code=401, detail='Unauthorized')
    return True


router = APIRouter(dependencies=[Depends(authorize_user)])
logger = logging.getLogger(__name__)
wnl = WLUIContextVar()
bot = Bot(env_parameters.TELEGRAM_BOT_TOKEN, parse_mode='HTML')


# handle test result and send new test
@router.post('/video_lesson_result')
async def test_handler(body: TestResultModel):
    with wnl.use_chat_id(body.user_id):
        logger.info(body)
        test = await Test.filter(video_lesson_order_number=body.video_lesson_order_number).get_or_none()
        logger.info(f'test_id: {test.id}, order_number: {test.video_lesson_order_number}, '
                    f'is_webinar: {body.is_webinar}')
        if not test:
            logger.exception(msg='Get test by video_lesson - test is None')
            raise HTTPException(status_code=404, detail='Test not found')

        if not body.result:
            try:
                await bot.send_message(chat_id=body.user_id, text=test.decline_text)
            except Exception as e:
                logger.exception(msg='Send TEST_RESULT_FALSE msg to user error', exc_info=e)

        else:
            try:
                await bot.send_message(chat_id=body.user_id, text=test.success_text)

                if body.is_webinar:  # /reg start
                    await start_of_registration(is_from_webhook=True, user_id=body.user_id)
                else:  # send next test => video_lesson_order_number += 1
                    logger.info(f'going to send lesson with number {body.video_lesson_order_number + 1}')
                    await lesson_sender(video_lesson_order_number=body.video_lesson_order_number + 1,
                                        user_id=body.user_id)

            except Exception as e:
                logger.exception(msg='Handle TEST_RESULT_TRUE error', exc_info=e)
