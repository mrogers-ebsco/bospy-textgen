# bospy-textgen

Presentation slides and demo code for a talk on text generation
for the [Boston Python](https://about.bostonpython.com/) NLP study group.

The demo project is a natural language generation (NLG) system
for producing textual weather forecasts from data published by
the National Weather Service via their web API.

## slides/

Contains a PDF of the presentation and LaTeX source code.

## project/

A Python package consisting of the following modules:

| module                | purpose                                                       |
|-----------------------|---------------------------------------------------------------|
| data.py               | Retrieves data from NWS API, provides data object definitions |
| textplanner.py        | Performs text planning functions                              |
| sentenceplanner.py    | Performs sentence planning functions                          |
| linguisticrealiser.py | Performs linguistic realisation functions                     |

## demo/

Contains code for running a live demo.
See this code and the presentation slides for more information
about how the project modules are used.

## License

Source code is published under the MIT license. See LICENSE file for details.

Images from Pexels are used in accordance
with the [license](https://www.pexels.com/license/).
