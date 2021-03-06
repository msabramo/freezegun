import sure
import time
from .fake_module import (
    equal_to_anything,
    fake_date_function,
    fake_datetime_function,
    fake_gmtime_function,
    fake_localtime_function,
    fake_strftime_function,
    fake_time_function,
)
from . import fake_module
from freezegun import freeze_time
from freezegun.api import FakeDatetime
import datetime


@freeze_time("2012-01-14")
def test_import_datetime_works():
    fake_datetime_function().day.should.equal(14)


@freeze_time("2012-01-14")
def test_import_date_works():
    fake_date_function().day.should.equal(14)


@freeze_time("2012-01-14")
def test_import_time():
    local_time = datetime.datetime(2012, 1, 14)
    utc_time = local_time - datetime.timedelta(seconds=time.timezone)
    expected_timestamp = time.mktime(utc_time.timetuple())
    fake_time_function().should.equal(expected_timestamp)


def test_start_and_stop_works():
    freezer = freeze_time("2012-01-14")

    result = fake_datetime_function()
    result.__class__.should.equal(datetime.datetime)
    result.__class__.shouldnt.equal(FakeDatetime)

    freezer.start()
    fake_datetime_function().day.should.equal(14)
    fake_datetime_function().should.be.a(datetime.datetime)
    fake_datetime_function().should.be.a(FakeDatetime)

    freezer.stop()
    result = fake_datetime_function()
    result.__class__.should.equal(datetime.datetime)
    result.__class__.shouldnt.equal(FakeDatetime)


def test_isinstance_works():
    date = datetime.date.today()
    now = datetime.datetime.now()

    freezer = freeze_time('2011-01-01')
    freezer.start()
    isinstance(date, datetime.date).should.equal(True)
    isinstance(date, datetime.datetime).should.equal(False)
    isinstance(now, datetime.datetime).should.equal(True)
    isinstance(now, datetime.date).should.equal(True)
    freezer.stop()


@freeze_time('2011-01-01')
def test_avoid_replacing_equal_to_anything():
    assert fake_module.equal_to_anything.description == 'This is the equal_to_anything object'


@freeze_time("2012-01-14 12:00:00")
def test_import_localtime():
    struct = fake_localtime_function()
    struct.tm_year.should.equal(2012)
    struct.tm_mon.should.equal(1)
    struct.tm_mday.should.equal(14)


@freeze_time("2012-01-14 12:00:00")
def test_fake_gmtime_function():
    struct = fake_gmtime_function()
    struct.tm_year.should.equal(2012)
    struct.tm_mon.should.equal(1)
    struct.tm_mday.should.equal(14)


@freeze_time("2012-01-14")
def test_fake_strftime_function():
    fake_strftime_function().should.equal('2012')
