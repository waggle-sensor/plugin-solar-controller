import argparse
import logging
import time
import functools

import requests
import schedule
import util

from waggle.plugin import Plugin

def catch_exceptions(cancel_on_failure=False):
    def catch_exceptions_decorator(job_func):
        @functools.wraps(job_func)
        def wrapper(*args, **kwargs):
            try:
                return job_func(*args, **kwargs)
            except:
                import traceback
                print(traceback.format_exc())
                if cancel_on_failure:
                    return schedule.CancelJob
        return wrapper
    return catch_exceptions_decorator


@catch_exceptions(cancel_on_failure=True)
def job(args):
    topic_names = list(util.registry_to_topicname_table.values())
    logging.info(f'Topic names to be published: {topic_names}')

    url = f'http://{args.host}/readreg'
    logging.info(f'URL to pull data from: {url}')

    registers = list(util.registry_to_topicname_table.keys())
    resp = requests.post(url, data=",".join(registers))
    resp.raise_for_status()

    logging.debug(f'Raw response: {resp.headers}, {resp.text}')
    with Plugin() as plugin:
        for r in resp.text.split(","):
            sp = r.strip().split("=")
            if len(sp) != 2:
                logging.error(f'{r} must follow register=value format')
                return schedule.CancelJob
            reg = sp[0]
            raw_value = sp[1]
            topic_name = util.registry_to_topicname_table[reg]
            value = util.transform_func[reg](raw_value)
            if reg in util.meta_table:
                meta = util.meta_table[reg]
            else:
                meta = {}
            plugin.publish(topic_name, value, meta=meta)
            logging.debug(f"{topic_name}, {value}, {meta} published")


def main(args):
    logging.info(f'Starting the task every {args.interval} seconds')
    if args.interval < 5:
        logging.error(f'{args.interval} must be greater than 5 seconds. Else, Plugin may not behave well')
    schedule.every(args.interval).seconds.do(job, args=args)

    while len(schedule.get_jobs()) > 0:
        schedule.run_pending()
        logging.debug("sleeping")
        time.sleep(1)
    logging.info("No jobs are available. They might have been removed due to an error")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--debug", dest="debug",
        action="store_true",
        help="Enable debugging")
    parser.add_argument(
        "--host", dest="host",
        action="store", type=str,
        help="IP address of the solar controller")
    parser.add_argument(
        "--publish-interval", dest="interval",
        action="store", default=60, type=int,
        help="Publish interval in seconds")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        format='%(asctime)s %(message)s',
        datefmt='%Y/%m/%d %H:%M:%S')

    exit(main(args))
