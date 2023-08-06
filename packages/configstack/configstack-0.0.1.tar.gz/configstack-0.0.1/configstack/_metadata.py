# maildrake/_metadata.py
# Part of ConfigStack, a library for configuring Python programs.
#
# Copyright © 2008–2017 Ben Finney <ben+python@benfinney.id.au>
#
# This is free software, and you are welcome to redistribute it under
# certain conditions; see the end of this file for copyright
# information, grant of license, and disclaimer of warranty.

""" Package metadata for the ‘configstack’ distribution. """

import datetime
import os.path

try:
    import semver
except ImportError:
    # We won't be able to parse Semantic Versioning values.
    semver = NotImplemented


distribution_name = "configstack"

version_file_name = "VERSION"
version_file_path = os.path.join(
        os.path.dirname(__file__),
        version_file_name)


class DistributionVersionUnknown(ValueError):
    """ Exception raised when the version of this distribution is unknown. """


def get_version_text(datafile_path=version_file_path):
    """ Get the version string from the version data file.

        :param filename: Filesystem path of the version data file.
        :return: The version string, as text.

        """
    try:
        with open(datafile_path) as infile:
            text = infile.read().strip()
    except (OSError, IOError) as exc:
        raise DistributionVersionUnknown(
                "could not read file {}".format(datafile_path)
                ) from exc

    return text


def get_version_fields(datafile_path=version_file_path):
    """ Get the version fields from the version data file.

        :param filename: Filesystem path of the version data file.
        :return: The version fields, as a dictionary.

        """
    if semver is NotImplemented:
        raise DistributionVersionUnknown("library ‘semver’ not available")

    version_text = get_version_text(datafile_path)

    try:
        fields = semver.parse(version_text)
    except ValueError as exc:
        raise DistributionVersionUnknown(
                "error parsing version text from {}".format(datafile_path)
                ) from exc

    fields['text'] = version_text
    return fields


try:
    version_fields = get_version_fields()
except DistributionVersionUnknown:
    version_fields = {}
    version_info = ()
    version_text = "UNKNOWN"
else:
    version_info = (
            version_fields['major'],
            version_fields['minor'],
            version_fields['patch'],
            version_fields['prerelease'],
            version_fields['build'],
            )
    version_text = version_fields['text']


author_name = "Ben Finney"
author_email = "ben+python@benfinney.id.au"
author = "{name} <{email}>".format(name=author_name, email=author_email)


class YearRange:
    """ A range of years spanning a period. """

    def __init__(self, begin, end=None):
        self.begin = begin
        self.end = end

    def __unicode__(self):
        template = "{range.begin:04d}–{range.end:04d}"
        if (self.end is None) or (self.end <= self.begin):
            template = "{range.begin:04d}"
        text = template.format(range=self)
        return text

    __str__ = __unicode__

    def __repr__(self):
        template = "{type}({range.begin:d}, {range.end:d})"
        if self.end is None:
            template = "{type}({range.begin:d})"
        text = template.format(type=type(self).__name__, range=self)
        return text


def make_year_range(begin_year, end_date=None):
    """ Construct the year range given a start and possible end date.

        :param begin_year: The beginning year (text, 4 digits) for the
            range.
        :param end_date: The end date (text, ISO-8601 format) for the
            range, or a non-date token string.
        :return: The range of years as a `YearRange` instance.

        If the `end_date` is not a valid ISO-8601 date string, the
        range has ``None`` for the end year.

        """
    begin_year = int(begin_year)

    try:
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    except (TypeError, ValueError):
        # Specified end_date value is not a valid date.
        end_year = None
    else:
        end_year = end_date.year

    year_range = YearRange(begin=begin_year, end=end_year)

    return year_range


copyright_year_begin = "2006"
copyright_year_current = "2017"
copyright_year_range = make_year_range(
    copyright_year_begin, copyright_year_current)

copyright = "Copyright © {year_range} {author}".format(
        year_range=copyright_year_range, author=author)
license = "GNU GPL-3+"
url = "https://pagure.io/python-configstack/"


# Copyright © 2008–2017 Ben Finney <ben+python@benfinney.id.au>
#
# This is free software: you may copy, modify, and/or distribute this work
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; version 3 of that license or any later version.
# No warranty expressed or implied. See the file ‘LICENSE.GPL-3’ for details.


# Local variables:
# coding: utf-8
# mode: python
# End:
# vim: fileencoding=utf-8 filetype=python :
