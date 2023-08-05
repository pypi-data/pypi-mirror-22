from operator import itemgetter

from lxml.builder import ElementMaker
from lxml import etree

from inxs import Config, Rule, Transformation
from inxs.common import sorter

from tests import equal_elements, parse


wp_document = parse("""
<persons>
  <person username="JS1">
    <name>John</name>
    <family-name>Smith</family-name>
  </person>
  <person username="MI1">
    <name>Morka</name>
    <family-name>Ismincius</family-name>
  </person>
</persons>
""")


def test_wikipedia_example_1():
    expected = parse("""
        <root>
          <name username="JS1">John</name>
          <name username="MI1">Morka</name>
        </root>
    """)

    def extract_person(element):
        return element.attrib['username'], element.find('name').text

    def append_person(previous_result, target):
        element = etree.SubElement(target, 'name', {'username': previous_result[0]})
        element.text = previous_result[1]
        return element

    transformation = Transformation(
        Rule(('person',), (extract_person, append_person)),
        config=Config(result_object='context.target',
                      context={'target': etree.Element('root')}))

    # that's three (or not counting line-breaks: six) lines less sloc than the XSLT implementation

    assert equal_elements(transformation(wp_document), expected)


def test_wikipedia_example_2():
    expected = parse("""
        <html xmlns="http://www.w3.org/1999/xhtml">
          <head> <title>Testing XML Example</title> </head>
          <body>
            <h1>Persons</h1>
              <ul>
                <li>Ismincius, Morka</li>
                <li>Smith, John</li>
              </ul>
          </body>
        </html>
    """)

    e = ElementMaker(namespace='http://www.w3.org/1999/xhtml',
                     nsmap={None: 'http://www.w3.org/1999/xhtml'})

    def generate_skeleton(context, e):
        context.html = e.html(
            e.head(e.title('Testing XML Example')),
            e.body(e.h1('Persons'), e.ul()))
        context.persons_list = context.html.xpath('./body/ul', smart_prefix=True)[0]

    def extract_person(element, persons):
        persons.append((element.find('name').text, element.find('family-name').text))

    def list_persons(previous_result, persons_list, e):
        persons_list.extend(e.li(f'{x[1]}, {x[0]}') for x in previous_result)

    transformation = Transformation(
        generate_skeleton,
        Rule(('person',), extract_person),
        sorter('persons', itemgetter(1)),
        list_persons,
        config=Config(result_object='context.html', e=e, context={'persons': []}))

    # that's seven (or not counting line-breaks: twelve) lines less sloc than the XSLT implementation

    assert equal_elements(transformation(wp_document), expected)
