import sys
import threading

import telegram
import vk

module = sys.modules[__name__]

t1 = threading.Thread(target=telegram.init)
t2 = threading.Thread(target=vk.init)

t1.start()
t2.start()
t1.join()
t2.join()
