"""Functions used by `concrete_inspect.py` to print data in a Communication.

The function implementations provide useful examples of how to
interact with many different Concrete datastructures.
"""
from __future__ import print_function
from __future__ import unicode_literals

from .util.metadata import get_index_of_tool
from .util.unnone import lun
from .util.tokenization import (
    get_tokenizations, get_tagged_tokens, NoSuchTokenTagging,
)
from collections import defaultdict
from operator import attrgetter

try:
    unicode
except NameError:
    unicode = str


def _reconcile_index_and_tool(lst_of_conc, given_idx, tool):
    """Given a list of Concrete objects with metadata (e.g., `DependencyParse`s)
    and a default index, find the index of the object whose `.metadata.tool`
    matches the provided query tool name `tool`.

    When no tool is provided (but with an iterable list), this returns the
    provided default index (even if it\'s not a valid index).
    If the tool isn't found, the list is None or empty, this returns -1.
    """
    valid_lst = lst_of_conc is not None and len(lst_of_conc) > 0
    idx = given_idx if valid_lst else -1
    if tool is not None:
        idx = get_index_of_tool(lst_of_conc, tool)
    return idx


def _valid_index_lun(lst, idx):
    """Return True iff `idx` is a valid index into
    the given (non-None) list. If `lst` is None,
    return False.
    """

    if lst is None or len(lst) == 0:
        return False
    return idx >= 0 and idx < len(lst)


def _filter_by_tool(lst, tool):
    return filter(lambda x: tool is None or x.metadata.tool == tool, lst)


def _get_tagged_token_strs_by_token_index(tagged_tokens, num_tokens):
    tagged_tokens_by_token_index = dict(
        (tagged_token.tokenIndex, tagged_token)
        for tagged_token in tagged_tokens
    )
    return [
        (
            tagged_tokens_by_token_index[token_index].tag
            if token_index in tagged_tokens_by_token_index
            else u''
        )
        for token_index in range(num_tokens)
    ]


def _get_tagged_tokens_or_empty(*args, **kwargs):
    try:
        return get_tagged_tokens(*args, **kwargs)
    except NoSuchTokenTagging:
        return []


def print_conll_style_tags_for_communication(
        comm, char_offsets=False, dependency=False, lemmas=False, ner=False,
        pos=False, other_tags=None,
        dependency_tool=None, lemmas_tool=None, ner_tool=None, pos_tool=None):

    """Print 'ConLL-style' tags for the tokens in a Communication

    Args:
        comm (Communication):
        char_offsets (bool): Flag for printing token text specified by
          a :class:`.Token`'s (optional) :class:`.TextSpan`
        dependency (bool): Flag for printing dependency parse HEAD tags
        lemmas (bool): Flag for printing lemma tags
        ner (bool): Flag for printing Named Entity Recognition tags
        pos (bool): Flag for printing Part-of-Speech tags
    """
    if other_tags is None:
        other_tags = ()

    header_fields = [u"INDEX", u"TOKEN"]
    if char_offsets:
        header_fields.append(u"CHAR")
    if lemmas:
        header_fields.append(u"LEMMA")
    if pos:
        header_fields.append(u"POS")
    if ner:
        header_fields.append(u"NER")
    if dependency:
        header_fields.append(u"HEAD")
        header_fields.append(u"DEPREL")
    for tag in other_tags:
        header_fields.append(tag)
    print(u"\t".join(header_fields))
    dashes = ["-" * len(fieldname) for fieldname in header_fields]
    print(u"\t".join(dashes))

    for tokenization in get_tokenizations(comm):
        token_tag_lists = []

        if char_offsets:
            token_tag_lists.append(
                _get_char_offset_tags_for_tokenization(comm, tokenization))
        if lemmas:
            token_tag_lists.append(
                _get_tagged_token_strs_by_token_index(
                    _get_tagged_tokens_or_empty(
                        tokenization, tagging_type=u'LEMMA', tool=lemmas_tool),
                    len(tokenization.tokenList.tokenList)))
        if pos:
            token_tag_lists.append(
                _get_tagged_token_strs_by_token_index(
                    _get_tagged_tokens_or_empty(
                        tokenization, tagging_type=u'POS', tool=pos_tool),
                    len(tokenization.tokenList.tokenList)))
        if ner:
            token_tag_lists.append([
                (tag if tag != u'NONE' else u'')
                for tag in _get_tagged_token_strs_by_token_index(
                    _get_tagged_tokens_or_empty(
                        tokenization, tagging_type=u'NER', tool=ner_tool),
                    len(tokenization.tokenList.tokenList)
                )
            ])
        if dependency:
            token_tag_lists.append(
                _get_conll_head_tags_for_tokenization(tokenization,
                                                      tool=dependency_tool))
            token_tag_lists.append(
                _get_conll_deprel_tags_for_tokenization(tokenization,
                                                        tool=dependency_tool))
        for tag in other_tags:
            token_tag_lists.append(
                _get_tagged_token_strs_by_token_index(
                    _get_tagged_tokens_or_empty(
                        tokenization, tagging_type=tag),
                    len(tokenization.tokenList.tokenList)))
        print_conll_style_tags_for_tokenization(tokenization,
                                                token_tag_lists)
        print()


def print_conll_style_tags_for_tokenization(tokenization, token_tag_lists):
    """Print 'ConLL-style' tags for the tokens in a tokenization

    Args:
        tokenization (Tokenization):
        token_tag_lists: A list of lists of token tag strings
    """
    if tokenization.tokenList:
        for i, token in enumerate(tokenization.tokenList.tokenList):
            token_tags = [unicode(token_tag_list[i])
                          for token_tag_list in token_tag_lists]
            fields = [unicode(i + 1), token.text]
            fields.extend(token_tags)
            print(u"\t".join(fields))


def _print_entity_mention_content(em, prefix=''):
    print(prefix + u"tokens:     %s" % (
        u" ".join(_get_tokens_for_entityMention(em))))
    if em.text:
        print(prefix + u"text:       %s" % em.text)
    print(prefix + u"entityType: %s" % em.entityType)
    print(prefix + u"phraseType: %s" % em.phraseType)


def print_entities(comm, tool=None):
    """Print information for :class:`.Entity` objects and their
    associated :class:`.EntityMention` objects

    Args:
        comm (Communication):
        tool (str): If not `None`, only print information for
                    :class:`.EntitySet` objects with a matching
                    `metadata.tool` field
    """
    if comm.entitySetList:
        for entitySet_index, entitySet in enumerate(comm.entitySetList):
            if tool is None or entitySet.metadata.tool == tool:
                print(u"Entity Set %d (%s):" % (entitySet_index,
                                                entitySet.metadata.tool))
                for entity_index, entity in enumerate(entitySet.entityList):
                    print(u"  Entity %d-%d:" % (entitySet_index, entity_index))
                    for em_index, em in enumerate(entity.mentionList):
                        print(u"      EntityMention %d-%d-%d:" % (
                            entitySet_index, entity_index, em_index))
                        _print_entity_mention_content(em, prefix=' ' * 10)
                        for (cm_index, cm) in enumerate(em.childMentionList):
                            print(u"          child EntityMention #%d:" % cm_index)
                            _print_entity_mention_content(cm, prefix=' ' * 14)
                    print()
                print()


def print_metadata(comm, tool=None):
    """Print metadata for tools used to annotate Communication

    Args:
        comm (Communication):
        tool (str): If not `None`, only print :class:`.AnnotationMetadata`
                    information for objects with a matching
                    `metadata.tool` field
    """
    if tool is None or comm.metadata.tool == tool:
        print(u"Communication:  %s\n" % comm.metadata.tool)

    dependency_parse_tools = set()
    parse_tools = set()
    tokenization_tools = set()
    token_tagging_tools = set()
    for tokenization in get_tokenizations(comm):
        tokenization_tools.add(tokenization.metadata.tool)
        if tokenization.tokenTaggingList:
            for tokenTagging in tokenization.tokenTaggingList:
                token_tagging_tools.add(tokenTagging.metadata.tool)
        if tokenization.dependencyParseList:
            for dependencyParse in tokenization.dependencyParseList:
                dependency_parse_tools.add(dependencyParse.metadata.tool)
        if tokenization.parseList:
            for parse in tokenization.parseList:
                parse_tools.add(parse.metadata.tool)

    communication_tagging_tools = set()
    for communication_tagging in lun(comm.communicationTaggingList):
        communication_tagging_tools.add(communication_tagging.metadata.tool)

    if tool is not None:
        dependency_parse_tools = dependency_parse_tools.intersection([tool])
        parse_tools = parse_tools.intersection([tool])
        tokenization_tools = tokenization_tools.intersection([tool])
        token_tagging_tools = token_tagging_tools.intersection([tool])
        communication_tagging_tools = communication_tagging_tools.intersection(
            [tool])

    if tokenization_tools:
        for toolname in sorted(tokenization_tools):
            print(u"  Tokenization:  %s" % toolname)
        print()
    if dependency_parse_tools:
        for toolname in sorted(dependency_parse_tools):
            print(u"    Dependency Parse:  %s" % toolname)
        print()
    if parse_tools:
        for toolname in sorted(parse_tools):
            print(u"    Parse:  %s" % toolname)
        print()
    if token_tagging_tools:
        for toolname in sorted(token_tagging_tools):
            print(u"    TokenTagging:  %s" % toolname)
        print()

    if comm.entityMentionSetList:
        for i, em_set in enumerate(comm.entityMentionSetList):
            if tool is None or em_set.metadata.tool == tool:
                print(u"  EntityMentionSet #%d:  %s" % (
                    i, em_set.metadata.tool))
        print()
    if comm.entitySetList:
        for i, entitySet in enumerate(comm.entitySetList):
            if tool is None or entitySet.metadata.tool == tool:
                print(u"  EntitySet #%d:  %s" % (
                    i, entitySet.metadata.tool))
        print()
    if comm.situationMentionSetList:
        for i, sm_set in enumerate(comm.situationMentionSetList):
            if tool is None or sm_set.metadata.tool == tool:
                print(u"  SituationMentionSet #%d:  %s" % (
                    i, sm_set.metadata.tool))
        print()
    if comm.situationSetList:
        for i, situationSet in enumerate(comm.situationSetList):
            if tool is None or situationSet.metadata.tool == tool:
                print(u"  SituationSet #%d:  %s" % (
                    i, situationSet.metadata.tool))
        print()

    if communication_tagging_tools:
        for toolname in sorted(communication_tagging_tools):
            print(u"  CommunicationTagging:  %s" % toolname)
        print()


def print_sections(comm, tool=None):
    """Print information for all :class:`.Section` object, according to their spans.

    Args:
        comm (Communication):
        tool (str): If not `None`, only print information for
                    :class:`.Section` objects with a matching
                    `metadata.tool` field
    """
    if tool is None or comm.metadata.tool == tool:
        text = comm.text
        for sect_idx, sect in enumerate(lun(comm.sectionList)):
            ts = sect.textSpan
            if ts is None:
                print(u"Section %s does not have a textSpan ")
                "field set" % (sect.uuid.uuidString)
                continue
            print(u"Section %d (%s), from %d to %d:" % (
                sect_idx, sect.uuid.uuidString, ts.start, ts.ending))
            print(u"%s" % (text[ts.start:ts.ending]))
            print()
        print()


def print_situation_mentions(comm, tool=None):
    """Print information for all :class:`.SituationMention` (some of which
    may not have a :class:`.Situation`)

    Args:
        comm (Communication):
        tool (str): If not `None`, only print information for
                    :class:`.SituationMention` objects with a matching
                    `metadata.tool` field
    """
    for sm_set_idx, sm_set in enumerate(lun(comm.situationMentionSetList)):
        if tool is None or sm_set.metadata.tool == tool:
            print(u"Situation Set %d (%s):" % (sm_set_idx,
                                               sm_set.metadata.tool))
            for sm_idx, sm in enumerate(sm_set.mentionList):
                print(u"  SituationMention %d-%d:" % (sm_set_idx, sm_idx))
                _print_situation_mention(sm)
                print()
            print()


def print_situations(comm, tool=None):
    """Print information for all :class:`.Situation` objects and their
    associated :class:`.SituationMention` objects

    Args:
        comm (Communication):
        tool (str): If not `None`, only print information for
                    :class:`.Situation` objects with a matching
                    `metadata.tool` field
    """
    for s_set_idx, s_set in enumerate(lun(comm.situationSetList)):
        if tool is None or s_set.metadata.tool == tool:
            print(u"Situation Set %d (%s):" % (s_set_idx,
                                               s_set.metadata.tool))
            for s_idx, situation in enumerate(s_set.situationList):
                print(u"  Situation %d-%d:" % (s_set_idx, s_idx))
                _p(6, 18, u"situationType", situation.situationType)
                for sm_idx, sm in enumerate(lun(situation.mentionList)):
                    print(u" " * 6 + u"SituationMention %d-%d-%d:" % (
                        s_set_idx, s_idx, sm_idx))
                    _print_situation_mention(sm)
                print()
            print()


def _print_situation_mention(situationMention):
    """Helper function for printing info for a SituationMention"""
    if situationMention.text:
        _p(10, 20, u"text", situationMention.text)
    if situationMention.situationType:
        _p(10, 20, u"situationType", situationMention.situationType)
    for arg_idx, ma in enumerate(lun(situationMention.argumentList)):
        print(u" " * 10 + u"Argument %d:" % arg_idx)
        if ma.role:
            _p(14, 16, u"role", ma.role)
        if ma.entityMention:
            _p(14, 16, u"entityMention",
                u" ".join(_get_tokens_for_entityMention(ma.entityMention)))
        if ma.propertyList:
            # PROTO-ROLE PROPERTIES: Format a separate list for each
            # distinct annotator (metadata.tool) which tool should be
            # either None or a string. Sort by annotator
            # (metadata.tool) and then by property (p.value)
            last_tool = False
            for p in sorted(ma.propertyList,
                            key=lambda x: (x.metadata.tool, x.value)):
                tool = p.metadata.tool
                if tool != last_tool:
                    print(u" " * 14 + u"Properties (%s):" % tool)
                    last_tool = tool
                _p(18, 20, p.value, u"%1.1f" % p.polarity)
        # A SituationMention can have an argumentList with a
        # MentionArgument that points to another SituationMention---
        # which could conceivably lead to loops.  We currently don't
        # traverse the list recursively, instead looking at only
        # SituationMentions referenced by top-level SituationMentions
        if ma.situationMention:
            print(u" " * 14 + u"situationMention:")
            if situationMention.text:
                _p(18, 20, u"text", situationMention.text)
            if situationMention.situationType:
                _p(18, 20, u"situationType", situationMention.situationType)


def _p(indent_level, justified_width, fieldname, content):
    """Text alignment helper function"""
    print (
        (u" " * indent_level) +
        (fieldname + u":").ljust(justified_width) +
        content
    )


def print_text_for_communication(comm, tool=None):
    """Print `text field of :class:`.Communication`

    Args:
        comm (Communication):
        tool (str): If not `None`, only print `text` field of
                    :class:`.Communication` objects with a matching
                    `metadata.tool` field
    """
    if tool is None or comm.metadata.tool == tool:
        print(comm.text)


def print_id_for_communication(comm, tool=None):
    """Print ID field of :class:`.Communication`

    Args:
        comm (Communication):
        tool (str): If not `None`, only print ID of
                    :class:`.Communication` objects with a matching
                    `metadata.tool` field

    """
    if tool is None or comm.metadata.tool == tool:
        print(comm.id)


def print_communication_taggings_for_communication(comm, tool=None):
    """Print information for :class:`.CommunicationTagging` objects

    Args:
        comm (Communication):
        tool (str): If not `None`, only print information for
                    :class:`.CommunicationTagging` objects with a
                    matching `metadata.tool` field
    """
    communication_taggings = _filter_by_tool(
        lun(comm.communicationTaggingList), tool)
    for tagging in communication_taggings:
        print('%s: %s' % (
            tagging.taggingType,
            ' '.join('%s:%.3f' % p for p in
                     zip(tagging.tagList, tagging.confidenceList))
        ))


def print_tokens_with_entityMentions(comm, tool=None):
    """Print information for :class:`.Token` objects that are part of an :class:`.EntityMention`

    Args:
        comm (Communication):
        tool (str): If not `None`, only print information for tokens
                    that are associated with an
                    :class:`.EntityMention` that is part of an
                    :class:`.EntityMentionSet` with a matching
                    `metadata.tool` field
    """
    em_by_tkzn_id = _get_entityMentions_by_tokenizationId(
        comm, tool=tool)
    em_entity_num = _get_entity_number_for_entityMention_uuid(comm, tool=tool)
    tokenizations_by_section = _get_tokenizations_grouped_by_section(comm)

    for tokenizations_in_section in tokenizations_by_section:
        for tokenization in tokenizations_in_section:
            if tokenization.tokenList:
                text_tokens = [token.text
                               for token
                               in tokenization.tokenList.tokenList]
                u = tokenization.uuid.uuidString
                if u in em_by_tkzn_id:
                    for em in em_by_tkzn_id[u]:
                        first_token_index = em.tokens.tokenIndexList[0]
                        last_token_index = em.tokens.tokenIndexList[-1]
                        entity_number = em_entity_num[em.uuid.uuidString]
                        text_tokens[first_token_index] = (
                            u"<ENTITY ID=%d>%s" %
                            (entity_number, text_tokens[first_token_index])
                        )
                        text_tokens[last_token_index] = (
                            u"%s</ENTITY>" % text_tokens[last_token_index]
                        )
                print(u" ".join(text_tokens))
        print()


def print_tokens_for_communication(comm, tool=None):
    """Print token text for a :class:`.Communication`

    Args:
        comm (Communication):
        tool (str): If not `None`, only print token text for
                    :class:`.Communication` objects with a matching
                    `metadata.tool` field
    """
    tokenizations_by_section = _get_tokenizations_grouped_by_section(
        comm, tool=tool)

    for tokenizations_in_section in tokenizations_by_section:
        for tokenization in tokenizations_in_section:
            if tokenization.tokenList:
                text_tokens = [token.text
                               for token
                               in tokenization.tokenList.tokenList]
                print(u" ".join(text_tokens))
        print()


def print_penn_treebank_for_communication(comm, tool=None):
    """Print Penn-Treebank parse trees for all :class:`.Tokenization` objects

    Args:
        comm (Communication):
        tool (str): If not `None`, only print information for
                    :class:`.Tokenization` objects with a matching
                    `metadata.tool` field
    """
    tokenizations = get_tokenizations(comm)

    for tokenization in tokenizations:
        if tokenization.parseList:
            for parse in tokenization.parseList:
                if tool is None or tool == parse.metadata.tool:
                    print(penn_treebank_for_parse(parse) + u"\n\n")


def penn_treebank_for_parse(parse):
    """Get a Penn-Treebank style string for a Concrete Parse object

    Args:
        parse (Parse):

    Returns:
        str: A string containing a Penn Treebank style parse tree representation
    """
    def _traverse_parse(nodes, node_index, indent=0):
        s = u""
        indent += len(nodes[node_index].tag) + 2
        if nodes[node_index].childList:
            s += u"(%s " % nodes[node_index].tag
            for i, child_node_index in enumerate(nodes[node_index].childList):
                if i > 0:
                    s += u"\n" + u" " * indent
                s += _traverse_parse(nodes, child_node_index, indent)
            s += u")"
        else:
            s += nodes[node_index].tag
        return s

    sorted_nodes = sorted(parse.constituentList, key=attrgetter('id'))
    return _traverse_parse(sorted_nodes, 0)


def _get_char_offset_tags_for_tokenization(comm, tokenization):
    if tokenization.tokenList:
        char_offset_tags = [None] * len(tokenization.tokenList.tokenList)

        if comm.text:
            for i, token in enumerate(tokenization.tokenList.tokenList):
                if token.textSpan:
                    char_offset_tags[i] = comm.text[
                        token.textSpan.start:token.textSpan.ending]
        return char_offset_tags


def _deps_for_tokenization(tokenization,
                           dependency_parse_index=0,
                           tool=None):
    """
    Return a generator of the dependencies (Dependency objects) for
    a tokenization under the given tool.
    """
    if tokenization.tokenList is not None:
        # Tokens that are not part of the dependency parse
        # (e.g. punctuation) are represented using an empty string
        dp_idx = _reconcile_index_and_tool(tokenization.dependencyParseList,
                                           dependency_parse_index,
                                           tool)

        if _valid_index_lun(tokenization.dependencyParseList, dp_idx):
            dp = tokenization.dependencyParseList[dp_idx]
            if tool is None or dp.metadata.tool == tool:
                for dependency in dp.dependencyList:
                    yield dependency


def _sorted_dep_list_for_tokenization(tokenization,
                                      dependency_parse_index=0,
                                      tool=None):
    """
    Return output of _deps_for_tokenization in a list whose length
    is equal to the number of tokens in this tokenization's token list,
    where the element at index i is a dependency if there is a
    dependency whose dep field is i and None otherwise.
    """
    if tokenization.tokenList is not None:
        dep_list = [None] * len(tokenization.tokenList.tokenList)
        for dep in _deps_for_tokenization(
                tokenization, dependency_parse_index=dependency_parse_index,
                tool=tool):
            dep_list[dep.dep] = dep
        return dep_list
    else:
        return []


def _get_conll_head_tags_for_tokenization(tokenization,
                                          dependency_parse_index=0,
                                          tool=None):
    """Get a list of ConLL 'HEAD tags' for a tokenization

    In the ConLL data format:

        http://ufal.mff.cuni.cz/conll2009-st/task-description.html

    the HEAD for a token is the (1-indexed) index of that token's
    parent token.  The root token of the dependency parse has a HEAD
    index of 0.

    Args:
        tokenization (Tokenization):

    Returns:
        str[]: A list of ConLL 'HEAD tag' strings, with one HEAD tag
               for each token in the supplied tokenization.  If a
               token does not have a HEAD tag (e.g. punctuation
               tokens), the HEAD tag is an empty string.

               If the tokenization does not have a Dependency Parse,
               this function returns a list of empty strings for each
               token in the supplied tokenization.
    """
    return list(map(
        lambda dep: '' if dep is None else (
            0 if dep.gov is None else dep.gov + 1),
        _sorted_dep_list_for_tokenization(
            tokenization, dependency_parse_index=dependency_parse_index,
            tool=tool)))


def _get_conll_deprel_tags_for_tokenization(tokenization,
                                            dependency_parse_index=0,
                                            tool=None):
    """Get a list of ConLL 'DEPREL tags' for a tokenization

    In the ConLL data format:

        http://ufal.mff.cuni.cz/conll2009-st/task-description.html

    the DEPREL for a token is the type of that token's dependency with
    its parent.

    Args:
        tokenization (Tokenization):

    Returns:
        A list of ConLL 'DEPREL tag' strings, with one DEPREL tag for
        each token in the supplied tokenization.  If a token does not
        have a DEPREL tag (e.g. punctuation tokens), the DEPREL tag is
        an empty string.

        If the tokenization does not have a Dependency Parse, this
        function returns a list of empty strings for each token in the
        supplied tokenization.
    """
    return list(map(
        lambda dep: '' if dep is None else (
            '' if dep.edgeType is None else dep.edgeType),
        _sorted_dep_list_for_tokenization(
            tokenization, dependency_parse_index=dependency_parse_index,
            tool=tool)))


def _get_entityMentions_by_tokenizationId(comm, tool=None):
    """Get entity mentions for a Communication grouped by Tokenization
    UUID string

    Args:
        comm (Communication):

    Returns:
        A dictionary of lists of EntityMentions, where the dictionary
        keys are Tokenization UUID strings.
    """
    mentions_by_tkzn_id = defaultdict(list)
    for entitySet in lun(comm.entitySetList):
        for entity in entitySet.entityList:
            for entityMention in entity.mentionList:
                if (tool is None or
                        entityMention.entityMentionSet.metadata.tool == tool):
                    u = entityMention.tokens.tokenizationId.uuidString
                    mentions_by_tkzn_id[u].append(entityMention)
    return mentions_by_tkzn_id


def _get_entity_number_for_entityMention_uuid(comm, tool=None):
    """Create mapping from EntityMention UUID to (zero-indexed)
    'Entity Number'

    Args:
        comm (Communication):

    Returns:
        A dictionary where the keys are EntityMention UUID strings,
        and the values are "Entity Numbers", where the first Entity is
        assigned number 0, the second Entity is assigned number 1,
        etc.
    """
    entity_number_for_entityMention_uuid = {}
    entity_number_counter = 0

    if comm.entitySetList:
        for entitySet in comm.entitySetList:
            for entity in entitySet.entityList:
                any_mention = False
                for entityMention in entity.mentionList:
                    if (tool is None or
                            entityMention.entityMentionSet.metadata.tool ==
                            tool):
                        entity_number_for_entityMention_uuid[
                            entityMention.uuid.uuidString
                        ] = entity_number_counter
                    any_mention = True
                if any_mention:
                    entity_number_counter += 1
    return entity_number_for_entityMention_uuid


def _get_tokenizations_grouped_by_section(comm, tool=None):
    """Returns a list of lists of Tokenization objects in a Communication

    Args:
        comm (Communication):

    Returns:
        Returns a list of lists of Tokenization objects, where the
        Tokenization objects are grouped by Section
    """
    tokenizations_by_section = []

    if comm.sectionList:
        for section in comm.sectionList:
            tokenizations_in_section = []
            if section.sentenceList:
                for sentence in section.sentenceList:
                    if sentence.tokenization:
                        if (tool is None or
                                sentence.tokenization.metadata.tool == tool):
                            tokenizations_in_section.append(
                                sentence.tokenization)
            tokenizations_by_section.append(tokenizations_in_section)

    return tokenizations_by_section


def _get_tokens_for_entityMention(entityMention):
    """Get list of token strings for an EntityMention

    Args:
        entityMention (EntityMention):

    Returns:
        A list of token strings
    """
    tokens = []
    for tokenIndex in entityMention.tokens.tokenIndexList:
        tokens.append(entityMention.tokens.tokenization.tokenList.tokenList[
                      tokenIndex].text)
    return tokens


def _get_tokentaggings_of_type(tokenization, taggingType, tool=None):
    """Returns a list of :class:`.TokenTagging` objects with the specified taggingType

    Args:
        tokenization (Tokenization):
        taggingType (str): A string value for the specified TokenTagging.taggingType

    Returns:
        A list of TokenTagging objects
    """
    return [
        tt for tt in tokenization.tokenTaggingList
        if tt.taggingType.lower() == taggingType.lower() and (
            tool is None or tt.metadata.tool == tool)
    ]
