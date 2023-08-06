Usage
=====

Command line invocation
-----------------------

::

    usage: changelogdir [-h] [-o OUTPUT] [-c CONFIG] [-d DIRECTORY]

    Generate changelogs from a directory structure.

    optional arguments:
      -h, --help            show this help message and exit
      -o OUTPUT, --output OUTPUT
                            File to write to
      -c CONFIG, --config CONFIG
                            Path to config file (default: '.changelogdirrc')
      -d DIRECTORY, --directory DIRECTORY
                            Override path to changelog directory

    If no output file is specified, write to STDOUT.

Typically, you do not need to specify any arguments.

::

    changelogdir > CHANGELOG.md

is equal to::

    changelogdir -c .changelogdirrc -d CHANGELOG -o CHANGELOG.md

Configuration
-------------

The configuration file is optional.  If no configuration file is found or
specified, it defaults to::

    [changelogdir]
    directory = CHANGELOG
    file_extension = md
    header = # Changelog
    section_header = ## {section_name}
    subsection_header = ### {subsection_name}

When adding a configuration file, you only have to specify the keys that you
want to change from their defaults.

directory
~~~~~~~~~

Directory relative to the configuration file that contains the changelog
structure.

file_extension
~~~~~~~~~~~~~~

The extension used by entry files.

header
~~~~~~

A string of text that is put at the very top of the output.  This key, as well
as `section_header`_ and `subsection_header`_, can span multiple lines::

    header = Changelog
             =========

section_header
~~~~~~~~~~~~~~

A string of text that is put at the top of every section.  There are two
variables available that can be placed between curly braces, ``{section_name}``
and ``{section_date}``::

    section_header = ## {section_name} - {section_date}

section_name
++++++++++++

The directory name of the section *after* the first underscore.  So, if you have
a directory named "zzz_Unreleased", *section_name* is equal to "Unreleased".
See `Ordering`_ for an explanation.

Typically, you would name your section directories "X.Y.Z".

section_date
++++++++++++

A special variable that is equal to the contents of the "date" file inside of
your section directory.  Typically, you want to put the release date in
YYYY-MM-DD inside of that file.

subsection_header
~~~~~~~~~~~~~~~~~

The same as `section_header`_, except you only have access to the
``{subsection_name}`` variable.

subsection_name
+++++++++++++++

See `section_name`_.

Typically, you would name your subsection directories (see
`Keep a Changelog <http://keepachangelog.com>`_):

- "Added" for new features.

- "Changed" for changes in existing functionality.

- "Deprecated" for once-stable features removed in upcoming releases.

- "Removed" for deprecated features removed in this release.

- "Fixed" for any bug fixes.

- "Security" to invite users to upgrade in case of vulnerabilities.

Directory structure
-------------------

The directory structure of your project might look somewhat like this::

    demo-project
    ├── CHANGELOG
    │   ├── 1.0.0
    │   │   ├── 000_first-entry.rst
    │   │   ├── 000_Security
    │   │   │   └── security-fix.rst
    │   │   ├── Added
    │   │   │   └── some-feature.rst
    │   │   ├── date
    │   │   └── Deprecated
    │   │       └── x11.rst
    │   ├── 2.0.0
    │   │   └── date
    │   └── zzz_Unreleased
    │       ├── 000_first-entry.rst
    │       ├── date
    │       ├── typical-entry.rst
    │       └── zzz_footer.rst
    └── .changelogdirrc

You can find this directory structure at
https://gitlab.com/carmenbianca/changelogdir/tree/master/tests/demo-project.

For clarity's sake, we will describe this structure with the following glossary:

- *Project root* - The very root of your project.  This contains your
  ``CHANGELOG`` directory and ``.changelogdirrc`` file.

- *Configuration file* - The ``.changelogdirrc`` file.

- *Changelog directory* - The ``CHANGELOG`` directory.

- *Section* - All subdirectories of the changelog directory.  Typically, these
  would be releases (X.Y.Z, zzz_Unreleased).

- *Subsection* - All subdirectories of a section.  See `subsection_name`_ to get
  an idea for what these might be used for.  Subsections are entirely optional.

- *Entry* - All files with your specified file extension, belonging to either a
  section or a subsection.

- *Special file* - Any file that has a special purpose.  Currently, this only
  covers *date*.

The above structure renders to:

.. literalinclude:: ../tests/demo-project/expected.rst
    :language: restructuredtext

All sections, subsections and entries are padded by one empty line above them.

Ordering
~~~~~~~~

The sections, subsections and entries are ordered alphabetically by their file
and directory names:

- You can add "XXX\_" before your file or directory name to influence the order
  in which they appear.  "XXX\_" itself is not shown in the rendered changelog.
  See `section_name`_.

- Subsections and entries are in *ascending* order.  This is the expected
  behaviour by most users.  The subsection "Added" appears before "Deprecated",
  and subsection "000_Security" appears before "Added".

- Sections are in *descending* order.  This isn't very intuitive until you
  realise that this causes the *highest*/*newest* sections to appear at the top.
  Typically, you might name your "Unreleased" section "zzz_Unreleased" to make
  sure that it is always on top.
