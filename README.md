# IMDb Scraper

This is a web scraper for fetching ALL the movie information in the IMDb database. This project is the revamped version of the one I have made before. You can check that one out [here](https://github.com/ekinakkaya/movies-data-scraping).

# todo

- [x] scrape movie counts for every year
- [x] scrape movie links
- [x] fix the unclickable button issues
- [x] refactor the code a bit
- [x] web driver manager
- [x] properly handle where will links be saved and in what format.
- [x] session manager
- [ ] rewrite tests with unittest
- [ ] finish session manager
- [ ] implement session manager in scraper
- [ ] make tests
- [x] make tests for session manager
- [ ] progress bar
- [ ] there is no failsafe for being banned from the site. test this and evaluate
- [ ] add session logic for unexpected closes, crashs, network issues, etc. so the program can keep scraping where it has left off
- [ ] webpage manager

# bugs

**i think i fixed it**
~~i got this mysterious error while testing, idk. i couldn't recreate it~~

```
PS C:\Users\ekin_\projeler\imdb-scraper> & C:/Python312/python.exe c:/Users/ekin_/projeler/imdb-scraper/main.py

DevTools listening on ws://127.0.0.1:1620/devtools/browser/c6ba7d26-c6f8-44d7-bb23-6d9512118d5f
[9252:24480:1026/003608.136:ERROR:interface_endpoint_client.cc(725)] Message 2 rejected by interface blink.mojom.Widget
[9252:24480:1026/003612.525:ERROR:device_event_log_impl.cc(201)] [00:36:12.498] USB: usb_service_win.cc:105 SetupDiGetDeviceProperty({{A45C254E-DF1C-4EFD-8020-67D146A850E0}, 6}) failed: Element not found. (0x490)
Created TensorFlow Lite XNNPACK delegate for CPU.
Traceback (most recent call last):
  File "c:\Users\ekin_\projeler\imdb-scraper\imdb_scraper\imdb_scraper.py", line 255, in scrape_movie_links_in_interval
    more_button_list[0].click()
  File "C:\Python312\Lib\site-packages\selenium\webdriver\remote\webelement.py", line 94, in click
    self._execute(Command.CLICK_ELEMENT)
  File "C:\Python312\Lib\site-packages\selenium\webdriver\remote\webelement.py", line 395, in _execute
    return self._parent.execute(command, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python312\Lib\site-packages\selenium\webdriver\remote\webdriver.py", line 347, in execute
    self.error_handler.check_response(response)
  File "C:\Python312\Lib\site-packages\selenium\webdriver\remote\errorhandler.py", line 229, in check_response
    raise exception_class(message, screen, stacktrace)
selenium.common.exceptions.StaleElementReferenceException: Message: stale element reference: stale element not found in the current frame
  (Session info: chrome=130.0.6723.70); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#stale-element-reference-exception
Stacktrace:
        GetHandleVerifier [0x00007FF7017A3AB5+28005]
        (No symbol) [0x00007FF7017083B0]
        (No symbol) [0x00007FF7015A580A]
        (No symbol) [0x00007FF7015AC2CC]
        (No symbol) [0x00007FF7015AE5E7]
        (No symbol) [0x00007FF7015AE6A0]
        (No symbol) [0x00007FF7015F7B4B]
        (No symbol) [0x00007FF7015E97D6]
        (No symbol) [0x00007FF70161BA3A]
        (No symbol) [0x00007FF7015E9246]
        (No symbol) [0x00007FF70161BC50]
        (No symbol) [0x00007FF70163B8B3]
        (No symbol) [0x00007FF70161B7E3]
        (No symbol) [0x00007FF7015E75C8]
        (No symbol) [0x00007FF7015E8731]
        GetHandleVerifier [0x00007FF701A9643D+3118829]
        GetHandleVerifier [0x00007FF701AE6C90+3448640]
        GetHandleVerifier [0x00007FF701ADCF0D+3408317]
        GetHandleVerifier [0x00007FF70186A40B+841403]
        (No symbol) [0x00007FF70171340F]
        (No symbol) [0x00007FF70170F484]
        (No symbol) [0x00007FF70170F61D]
        (No symbol) [0x00007FF7016FEB79]
        BaseThreadInitThunk [0x00007FFC99FF257D+29]
        RtlUserThreadStart [0x00007FFC9AC6AF08+40]


During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "c:\Users\ekin_\projeler\imdb-scraper\main.py", line 12, in <module>
    scraper.scrape_movies_from_scrape_path("scrape_path.json")
  File "c:\Users\ekin_\projeler\imdb-scraper\imdb_scraper\imdb_scraper.py", line 302, in scrape_movies_from_scrape_path
    self.scrape_movie_links_in_interval(start_date, end_date, movie_count)
  File "c:\Users\ekin_\projeler\imdb-scraper\imdb_scraper\imdb_scraper.py", line 264, in scrape_movie_links_in_interval
    element_position = self.driver.execute_script("return arguments[0].getBoundingClientRect().top;", more_button_list[0])
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python312\Lib\site-packages\selenium\webdriver\remote\webdriver.py", line 407, in execute_script
    return self.execute(command, {"script": script, "args": converted_args})["value"]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python312\Lib\site-packages\selenium\webdriver\remote\webdriver.py", line 347, in execute
    self.error_handler.check_response(response)
  File "C:\Python312\Lib\site-packages\selenium\webdriver\remote\errorhandler.py", line 229, in check_response
    raise exception_class(message, screen, stacktrace)
selenium.common.exceptions.StaleElementReferenceException: Message: stale element reference: stale element not found in the current frame
  (Session info: chrome=130.0.6723.70); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#stale-element-reference-exception
Stacktrace:
        GetHandleVerifier [0x00007FF7017A3AB5+28005]
        (No symbol) [0x00007FF7017083B0]
        (No symbol) [0x00007FF7015A580A]
        (No symbol) [0x00007FF7015AC2CC]
        (No symbol) [0x00007FF7015AE8FF]
        (No symbol) [0x00007FF70163CB90]
        (No symbol) [0x00007FF70161BA3A]
        (No symbol) [0x00007FF70163B8B3]
        (No symbol) [0x00007FF70161B7E3]
        (No symbol) [0x00007FF7015E75C8]
        (No symbol) [0x00007FF7015E8731]
        GetHandleVerifier [0x00007FF701A9643D+3118829]
        GetHandleVerifier [0x00007FF701AE6C90+3448640]
        GetHandleVerifier [0x00007FF701ADCF0D+3408317]
        GetHandleVerifier [0x00007FF70186A40B+841403]
        (No symbol) [0x00007FF70171340F]
        (No symbol) [0x00007FF70170F484]
        (No symbol) [0x00007FF70170F61D]
        (No symbol) [0x00007FF7016FEB79]
        BaseThreadInitThunk [0x00007FFC99FF257D+29]
        RtlUserThreadStart [0x00007FFC9AC6AF08+40]

```