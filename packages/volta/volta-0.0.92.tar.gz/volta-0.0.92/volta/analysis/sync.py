# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from scipy import interpolate
from scipy import signal
from datetime import datetime

import logging
log = logging.getLogger(__name__)


def torch_status(lines):
    """
    Parse torch statuses from lines
    """
    for line in lines:
        if "newStatus=2" in line:
            yield (
                datetime.strptime(
                    line.split()[1], "%H:%M:%S.%f"),
                1)
        elif "newStatus=1" in line:
            yield (
                datetime.strptime(
                    line.split()[1], "%H:%M:%S.%f"),
                0)


def parse_torch_events(filename, sps=1000):
    """
    Parse torch events from file, considering target sample rate.
    Offset is the number of sample
    """
    log.info("Parsing torch events...")
    with open(filename) as eventlog:
        df = pd.DataFrame.from_records(
            torch_status(eventlog), columns=["offset", "status"])
        df["offset"] = df["offset"].map(
            lambda x: int(np.round((x - df["offset"][0]).total_seconds() * sps)))
        # use only first 20 secs
        df = df[df.offset < int(20*sps)]
        return df


def ref_signal(torch):
    """
    Generate square reference signal
    """
    log.info("Generating ref signal...")
    if len(torch) == 0:
        raise ValueError('Torches not found.')
    f = interpolate.interp1d(torch["offset"], torch["status"], kind="zero")
    log.debug('Torches:\n %s', torch)
    X = np.linspace(0, torch["offset"].values[-1], torch["offset"].values[-1])
    rs = f(X)
    return rs - np.mean(rs)


def cross_correlate(sig, ref, first=30000):
    """
    Calculate cross-correlation with lag. Take only first n lags.
    """
    log.info("Calculating cross-correlation...")
    return signal.fftconvolve(sig[:first], ref[::-1], mode="valid")


def sync(sig, eventlog, sps=1000, first=30000):
    """
    Calculate sync point for android log and electrical current measurements

    Args:
        sig: current measurements, one column
        eventlog: android log with torch on/off events
        sps: current measurements sample rate
        first: number of samples to try as lag

    Returns:
        sync_point, int, amount of samples of electrical current log until synchronization flaslight event
    """
    rs = ref_signal(
        parse_torch_events(eventlog, sps=sps))
    log.debug('Ref sig: %s', rs)
    cc = cross_correlate(sig, rs, first)
    sync_point = np.argmax(cc)
    log.info('sync_point: %s', sync_point)
    return sync_point


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description='Calculate sync point for android log and electrical current measurements.')
    parser.add_argument(
        '-s', '--sps',
        default=1000,
        help='current measurements sample rate')
    parser.add_argument(
        '-f', '--first',
        default=30000,
        help='number of samples to try as lag')
    parser.add_argument(
        '-d', '--debug',
        help='enable debug logging',
        action='store_true')
    parser.add_argument(
        "curr_log",
        help="csv file with electrical current measurements, one column")
    parser.add_argument(
        "android_log", help="android log with torch on/off events")
    args = parser.parse_args()
    logging.basicConfig(
        level="DEBUG" if args.debug else "INFO",
        format='%(asctime)s [%(levelname)s] [VOLTA SYNC] %(filename)s:%(lineno)d %(message)s')
    sync_point = sync(
        pd.read_csv(args.curr_log, names="current")["current"],
        args.android_log,
        sps=args.sps,
        first=args.first,
    )
    log.info("Sync point: %d", sync_point)

if __name__ == '__main__':
    main()
