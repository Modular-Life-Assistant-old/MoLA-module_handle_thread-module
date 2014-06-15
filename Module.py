from core import ModuleManager

import threading

class Module:
    __thread_list = {}

    def __init__(self):
        ModuleManager.add_method_action(
            'thread',
            handle_start=self.create_thread,
            handle_stop=self.stop_thread
        )

    def create_thread(self, module_name, method_handle):
        def add_thread(handle):
            try:
                handle()

            except Exception as e:
                Log.crash(e)

        thread = threading.Thread(
            name=str(method_handle),
            target=add_thread,
            args=(method_handle,)
        )
        thread.start()

        if not module_name in self.__thread_list:
            self.__thread_list[module_name] = []

        self.__thread_list[module_name].append(thread)

    def stop_thread(self, module_name, method_handle):
        for thread in self.__thread_list[module_name]:
            thread._Thread__stop()
            self.__thread_list.remove(thread)
