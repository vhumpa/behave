from behave.formatter.base import Formatter
import lxml.etree as ET
import base64
import os.path


class Counter(dict):
    '''Dict subclass for counting hashable objects.  Sometimes called a bag
    or multiset.  Elements are stored as dictionary keys and their counts
    are stored as dictionary values.

    >>> Counter('zyzygy')
    Counter({'y': 3, 'z': 2, 'g': 1})

    '''

    def __init__(self, iterable=None, **kwds):
        '''Create a new, empty Counter object.  And if given, count elements
        from an input iterable.  Or, initialize the count from another mapping
        of elements to their counts.

        >>> c = Counter()                           # a new, empty counter
        >>> c = Counter('gallahad')                 # a new counter from an iterable
        >>> c = Counter({'a': 4, 'b': 2})           # a new counter from a mapping
        >>> c = Counter(a=4, b=2)                   # a new counter from keyword args

        '''
        self.update(iterable, **kwds)

    def __missing__(self, key):
        return 0

    def most_common(self, n=None):
        '''List the n most common elements and their counts from the most
        common to the least.  If n is None, then list all element counts.

        >>> Counter('abracadabra').most_common(3)
        [('a', 5), ('r', 2), ('b', 2)]

        '''
        if n is None:
            return sorted(self.iteritems(), key=itemgetter(1), reverse=True)
        return nlargest(n, self.iteritems(), key=itemgetter(1))

    def elements(self):
        '''Iterator over elements repeating each as many times as its count.

        >>> c = Counter('ABCABC')
        >>> sorted(c.elements())
        ['A', 'A', 'B', 'B', 'C', 'C']

        If an element's count has been set to zero or is a negative number,
        elements() will ignore it.

        '''
        for elem, count in self.iteritems():
            for _ in repeat(None, count):
                yield elem

    # Override dict methods where the meaning changes for Counter objects.

    @classmethod
    def fromkeys(cls, iterable, v=None):
        raise NotImplementedError(
            'Counter.fromkeys() is undefined.  Use Counter(iterable) instead.')

    def update(self, iterable=None, **kwds):
        '''Like dict.update() but add counts instead of replacing them.

        Source can be an iterable, a dictionary, or another Counter instance.

        >>> c = Counter('which')
        >>> c.update('witch')           # add elements from another iterable
        >>> d = Counter('watch')
        >>> c.update(d)                 # add elements from another counter
        >>> c['h']                      # four 'h' in which, witch, and watch
        4

        '''
        if iterable is not None:
            if hasattr(iterable, 'iteritems'):
                if self:
                    self_get = self.get
                    for elem, count in iterable.iteritems():
                        self[elem] = self_get(elem, 0) + count
                else:
                    dict.update(self, iterable) # fast path when counter is empty
            else:
                self_get = self.get
                for elem in iterable:
                    self[elem] = self_get(elem, 0) + 1
        if kwds:
            self.update(kwds)

    def copy(self):
        'Like dict.copy() but returns a Counter instance instead of a dict.'
        return Counter(self)

    def __delitem__(self, elem):
        'Like dict.__delitem__() but does not raise KeyError for missing values.'
        if elem in self:
            dict.__delitem__(self, elem)

    def __repr__(self):
        if not self:
            return '%s()' % self.__class__.__name__
        items = ', '.join(map('%r: %r'.__mod__, self.most_common()))
        return '%s({%s})' % (self.__class__.__name__, items)

    # Multiset-style mathematical operations discussed in:
    #       Knuth TAOCP Volume II section 4.6.3 exercise 19
    #       and at http://en.wikipedia.org/wiki/Multiset
    #
    # Outputs guaranteed to only include positive counts.
    #
    # To strip negative and zero counts, add-in an empty counter:
    #       c += Counter()

    def __add__(self, other):
        '''Add counts from two counters.

        >>> Counter('abbb') + Counter('bcc')
        Counter({'b': 4, 'c': 2, 'a': 1})


        '''
        if not isinstance(other, Counter):
            return NotImplemented
        result = Counter()
        for elem in set(self) | set(other):
            newcount = self[elem] + other[elem]
            if newcount > 0:
                result[elem] = newcount
        return result

    def __sub__(self, other):
        ''' Subtract count, but keep only results with positive counts.

        >>> Counter('abbbc') - Counter('bccd')
        Counter({'b': 2, 'a': 1})

        '''
        if not isinstance(other, Counter):
            return NotImplemented
        result = Counter()
        for elem in set(self) | set(other):
            newcount = self[elem] - other[elem]
            if newcount > 0:
                result[elem] = newcount
        return result

    def __or__(self, other):
        '''Union is the maximum of value in either of the input counters.

        >>> Counter('abbb') | Counter('bcc')
        Counter({'b': 3, 'c': 2, 'a': 1})

        '''
        if not isinstance(other, Counter):
            return NotImplemented
        _max = max
        result = Counter()
        for elem in set(self) | set(other):
            newcount = _max(self[elem], other[elem])
            if newcount > 0:
                result[elem] = newcount
        return result

    def __and__(self, other):
        ''' Intersection is the minimum of corresponding counts.

        >>> Counter('abbb') & Counter('bcc')
        Counter({'b': 1})

        '''
        if not isinstance(other, Counter):
            return NotImplemented
        _min = min
        result = Counter()
        if len(self) < len(other):
            self, other = other, self
        for elem in ifilter(self.__contains__, other):
            newcount = _min(self[elem], other[elem])
            if newcount > 0:
                result[elem] = newcount
        return result


class HTMLFormatter(Formatter):
    name = 'html'
    description = 'Very basic HTML formatter'

    def __init__(self, stream, config):
        super(HTMLFormatter, self).__init__(stream, config)

        self.html = ET.Element('html')

        head = ET.SubElement(self.html, 'head')
        ET.SubElement(head, 'title').text = u'Behave steps'
        ET.SubElement(head, 'meta', {'content': 'text/html;charset=utf-8'})
        ET.SubElement(head, 'style').text =\
            open(os.path.join(os.path.dirname(__file__), ("report.css")),
                'r').read().encode('utf-8')

        self.stream = self.open()
        body = ET.SubElement(self.html, 'body')
        self.suite = ET.SubElement(body, 'div', {'class': 'behave'})

        #Summary
        self.header = ET.SubElement(self.suite, 'div', id='behave-header')
        label = ET.SubElement(self.header, 'div', id='label')
        ET.SubElement(label, 'h1').text = u'Behave features'

        summary = ET.SubElement(self.header, 'div', id='summary')

        totals = ET.SubElement(summary, 'p', id='totals')

        self.current_feature_totals = ET.SubElement(totals, 'p', id='feature_totals')
        self.scenario_totals = ET.SubElement(totals, 'p', id='scenario_totals')
        self.step_totals = ET.SubElement(totals, 'p', id='step_totals')
        self.duration = ET.SubElement(summary, 'p', id='duration')

        expand_collapse = ET.SubElement(summary, 'div', id='expand-collapse')

        expander = ET.SubElement(expand_collapse, 'span', id='expander')
        expander.set('onclick', \
                     "var ols=document.getElementsByClassName('scenario_steps');" +
                     "for (var i=0; i< ols.length; i++) {" +
                         "ols[i].style.display = 'block';" +
                     "}; " +
                     "return false")
        expander.text = u'Expand All'

        spacer = ET.SubElement(expand_collapse, 'span')
        spacer.text = u"  "

        collapser = ET.SubElement(expand_collapse, 'span', id='collapser')
        collapser.set('onclick', \
                     "var ols=document.getElementsByClassName('scenario_steps');" +
                     "for (var i=0; i< ols.length; i++) {" +
                         "ols[i].style.display = 'none';" +
                     "}; " +
                     "return false")
        collapser.text = u'Collapse All'

        self.embed_id = 0
        self.embed_in_this_step = None
        self.embed_data = None
        self.embed_mime_type = None
        self.scenario_id = 0

    def feature(self, feature):
        if not hasattr(self, "all_features"):
            self.all_features = []
        self.all_features.append(feature)

        self.current_feature = ET.SubElement(self.suite, 'div', {'class': 'feature'})
        if feature.tags:
            tags_element = ET.SubElement(self.current_feature, 'span', {'class': 'tag'})
            tags_element.text = u'@' + reduce(lambda d, x: "%s, @%s" % (d, x), feature.tags)
        h2 = ET.SubElement(self.current_feature, 'h2')
        feature_element = ET.SubElement(h2, 'span', {'class': 'val'})
        feature_element.text = u'%s: %s' % (feature.keyword, feature.name)
        if feature.description:
            description_element = ET.SubElement(self.current_feature, 'pre', {'class': 'message'})
            description_element.text = reduce(lambda d, x: "%s\n%s" % (d, x), feature.description)

    def background(self, background):

        self.current_background = ET.SubElement(self.suite, 'div', {'class': 'background'})

        h3 = ET.SubElement(self.current_background, 'h3')
        ET.SubElement(h3, 'span', {'class': 'val'}).text = \
            u'%s: %s' % (background.keyword, background.name)


        self.steps = ET.SubElement(self.current_background, 'ol')

    def scenario(self, scenario):
        if scenario.feature not in self.all_features:
            self.all_features.append(scenario.feature)
        self.scenario_el = ET.SubElement(self.suite, 'div', {'class': 'scenario'})

        scenario_file = ET.SubElement(self.scenario_el, 'span', {'class': 'scenario_file'})
        scenario_file.text = "%s:%s" % (scenario.location.filename, scenario.location.line)

        if scenario.tags:
            tags = ET.SubElement(self.scenario_el, 'span', {'class': 'tag'})
            tags.text = u'@' + reduce(lambda d, x: "%s, @%s" % (d, x), scenario.tags)

        self.scenario_name = ET.SubElement(self.scenario_el, 'h3')
        span = ET.SubElement(self.scenario_name, 'span', {'class': 'val'})
        span.text = u'%s: %s' % (scenario.keyword, scenario.name)

        if scenario.description:
            description_element = ET.SubElement(self.scenario_el, 'pre', {'class': 'message'})
            description_element.text = reduce(lambda d, x: "%s\n%s" % (d, x), scenario.description)

        self.steps = ET.SubElement(self.scenario_el, 'ol',
            {'class': 'scenario_steps',
             'id': 'scenario_%s' % self.scenario_id})

        self.scenario_name.set('onclick', \
                     "ol=document.getElementById('scenario_%s');" % self.scenario_id +
                     "ol.style.display =" +
                     "(ol.style.display == 'none' ? 'block' : 'none');" +
                     "return false")
        self.scenario_id += 1

    def scenario_outline(self, outline):
        self.scenario(self, outline)
        self.scenario_el.set('class', 'scenario outline')

    def match(self, match):
        self.arguments = match.arguments
        if match.location:
            self.location = "%s:%s" % (match.location.filename, match.location.line)
        else:
            self.location = "<unknown>"

    def step(self, step):
        self.arguments = None
        self.embed_in_this_step = None
        self.last_step = step

    def result(self, result):
        self.last_step = result
        step = ET.SubElement(self.steps, 'li', {'class': 'step %s' % result.status})
        step_name = ET.SubElement(step, 'div', {'class': 'step_name'})

        keyword = ET.SubElement(step_name, 'span', {'class': 'keyword'})
        keyword.text = result.keyword + u' '

        step_text = ET.SubElement(step_name, 'span', {'class': 'step val'})
        step_text.text = result.name
        if self.arguments:
            text_start = 0
            for argument in self.arguments:
                if text_start == 0:
                    step_text.text = result.name[:argument.start]
                else:
                    bold.tail = result.name[text_start:argument.start]
                bold = ET.SubElement(step_text, 'b')
                bold.text = str(argument.value)
                text_start = argument.end
            # Add remaining tail
            bold.tail = result.name[self.arguments[-1].end:]

        step_file = ET.SubElement(step, 'div', {'class': 'step_file'})
        ET.SubElement(step_file, 'span').text = self.location

        self.last_step_embed_span = ET.SubElement(step, 'span')
        self.last_step_embed_span.set('class', 'embed')

        if result.text:
            message = ET.SubElement(step, 'div', {'class': 'message'})
            pre = ET.SubElement(message, 'pre', {'style': 'white-space: pre-wrap;'})
            pre.text = result.text

        if result.table:
            table = ET.SubElement(step, 'table')
            tr = ET.SubElement(table, 'tr')
            for heading in result.table.headings:
                ET.SubElement(tr, 'th').text = heading

            for row in result.table.rows:
                tr = ET.SubElement(table, 'tr')
                for cell in row.cells:
                    ET.SubElement(tr, 'td').text = cell

        if result.error_message:
            self.embed_id += 1
            link = ET.SubElement(step, 'a', {'class': 'message'})
            link.set("onclick", \
                 "rslt=document.getElementById('embed_%s');" % self.embed_id +
                 "rslt.style.display =" +
                 "(rslt.style.display == 'none' ? 'block' : 'none');" +
                 "return false")
            link.text = u'Error message'

            embed = ET.SubElement(step, 'pre',
                {'id': "embed_%s" % self.embed_id,
                 'style': 'display: none; white-space: pre-wrap;'})
            embed.text = result.error_message
            embed.tail = u'    '

        if result.status == 'failed':
            style = 'background: #C40D0D; color: #FFFFFF'
            self.scenario_name.set('style', style)
            self.header.set('style', style)

        if result.status == 'undefined':
            style = 'background: #FAF834; color: #000000'
            self.scenario_name.set('style', style)
            self.header.set('style', style)

        if hasattr(self, 'embed_in_this_step') and self.embed_in_this_step:
            self._doEmbed(self.last_step_embed_span,
                          self.embed_mime_type,
                          self.embed_data)
            self.embed_in_this_step = None

    def _doEmbed(self, span, mime_type, data):
        self.embed_id += 1

        link = ET.SubElement(span, 'a')
        link.set("onclick", \
                 "embd=document.getElementById('embed_%s');" % self.embed_id +
                 "embd.style.display =" +
                 "(embd.style.display == 'none' ? 'block' : 'none');" +
                 "return false")

        if 'image/' in mime_type:
            link.text = u'Screenshot'

            embed = ET.SubElement(span, 'img',
                {'id': 'embed_%s' % self.embed_id,
                 'style': 'display: none',
                 'src': u'data:%s;base64,%s' % (mime_type, base64.b64encode(data))
                })
            embed.tail = u'    '

        if 'text/' in mime_type:
            link.text = u'Data'

            embed = ET.SubElement(span, 'pre',
                {'id': "embed_%s" % self.embed_id,
                 'style': 'display: none'})
            embed.text = data
            embed.tail = u'    '

    def embedding(self, mime_type, data):
        if self.last_step.status == 'untested':
            # Embed called during step execution
            self.embed_in_this_step = True
            self.embed_mime_type = mime_type
            self.embed_data = data
        else:
            # Embed called in after_*
            self._doEmbed(self.last_step_embed_span, mime_type, data)

    def close(self):
        if not hasattr(self, "all_features"):
            self.all_features = []
        self.duration.text =\
            u"Finished in %0.1f seconds" %\
                sum(map(lambda x: x.duration, self.all_features))

        # Filling in summary details
        result = []
        statuses = map(lambda x: x.status, self.all_features)
        status_counter = Counter(statuses)
        for k in status_counter:
            result.append('%s: %s' % (k, status_counter[k]))
        self.current_feature_totals.text = u'Features: %s' % ', '.join(result)

        result = []
        scenarios_list = map(lambda x: x.scenarios, self.all_features)
        scenarios = []
        if len(scenarios_list) > 0:
            scenarios = reduce(lambda a, b: a + b, scenarios_list)
        statuses = map(lambda x: x.status, scenarios)
        status_counter = Counter(statuses)
        for k in status_counter:
            result.append('%s: %s' % (k, status_counter[k]))
        self.scenario_totals.text = u'Scenarios: %s' % ', '.join(result)

        result = []
        step_list = map(lambda x: x.steps, scenarios)
        steps = []
        if step_list:
            steps = reduce(lambda a, b: a + b, step_list)
        statuses = map(lambda x: x.status, steps)
        status_counter = Counter(statuses)
        for k in status_counter:
            result.append('%s: %s' % (k, status_counter[k]))
        self.step_totals.text = u'Steps: %s' % ', '.join(result)

        # Sending the report to stream
        if len(self.all_features) > 0:
            self.stream.write(ET.tostring(self.html, pretty_print = True))
