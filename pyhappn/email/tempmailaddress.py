import logging
import time

logger = logging.getLogger(__file__)


def get_new_email(cls):
    logger.info('Starting Email')

    logger.info('visiting tempmailaddress.com')
    cls.fb_browser.execute_script(
        '''window.open("https://www.tempmailaddress.com/","_blank");''')
    time.sleep(2)

    cls.fb_browser.windows.current = cls.fb_browser.windows.current.next
    time.sleep(2)

    button = cls.fb_browser.find_by_css('#email')
    if button:
        cls.email = button[0].text
        time.sleep(2)
    else:
        raise Exception('Error')

    cls.fb_browser.windows.current = cls.fb_browser.windows.current.next
    time.sleep(2)


def confirm_email_fb(cls):
    cls.fb_browser.windows.current = cls.fb_browser.windows.current.next
    ok = False
    while ok is False:
        logger.info('Verifing email')
        tr = cls.fb_browser.find_by_css('.newMail')
        total = len(tr)
        for i in range(total):
            try:
                if 'Facebook' in cls.fb_browser.find_by_css('.newMail')[i].find_by_css('td')[0].text:
                    logger.info('click email')
                    i.click()
                    time.sleep(10)
                    with cls.fb_browser.get_iframe(1) as iframe:
                        logger.info('click link')
                        iframe.find_by_css('.mb_blk a')[0].click()
                        cls.code = iframe.find_by_css('.mb_text td')[0].value
                        ok = True
                    if ok is True:
                        break
            except Exception:
                continue

    cls.fb_browser.windows.current = cls.fb_browser.windows.current.next

    code_in_cliff = cls.fb_browser.find_by_css('#code_in_cliff')

    if code_in_cliff:
        code_in_cliff[0].fill(cls.code)
        time.sleep(1)
        cls.fb_browser.find_by_name('confirm')[0].click()

    time.sleep(1)
