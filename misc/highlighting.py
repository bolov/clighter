import vim
import string
import clighter_helper
from clang import cindex


OCCURRENCES_PRI = -11
SYNTAX_PRI = -12

def match_prop(prop, value):
    """
    returns true if prop is None or if prop == value
    """
    return prop is None or prop == value


class SyntaxGroup:
    """
    secondary_kind: kind of declaration or kind of template or None
    """
    def __init__(self, group_name, cursor_kind, secondary_kind=None):
        self.group_name = group_name
        self.cursor_kind = cursor_kind
        self.secondary_kind = secondary_kind

    def isMatch(self, cursor_kind, secondary_kind):
        return match_prop(self.cursor_kind, cursor_kind) and \
               match_prop(self.secondary_kind, secondary_kind)

SYNTAX_GROUPS = [
    SyntaxGroup("clighterNamespaceDecl", cindex.CursorKind.NAMESPACE),
    SyntaxGroup("clighterNamespaceRef", cindex.CursorKind.NAMESPACE_REF),

    SyntaxGroup("clighterStructDecl", cindex.CursorKind.STRUCT_DECL),
    SyntaxGroup("clighterClassDecl", cindex.CursorKind.CLASS_DECL),
    SyntaxGroup("clighterUnionDecl", cindex.CursorKind.UNION_DECL),
    SyntaxGroup("clighterEnumDecl", cindex.CursorKind.ENUM_DECL),
    SyntaxGroup("clighterTypedefDecl", cindex.CursorKind.TYPEDEF_DECL),
    SyntaxGroup("clighterTypedefDecl", cindex.CursorKind.TYPE_ALIAS_DECL),

    SyntaxGroup("clighterStructRef", cindex.CursorKind.TYPE_REF, cindex.CursorKind.STRUCT_DECL),
    SyntaxGroup("clighterClassRef", cindex.CursorKind.TYPE_REF, cindex.CursorKind.CLASS_DECL),
    SyntaxGroup("clighterUnionRef", cindex.CursorKind.TYPE_REF, cindex.CursorKind.UNION_DECL),
    SyntaxGroup("clighterEnumRef", cindex.CursorKind.TYPE_REF, cindex.CursorKind.ENUM_DECL),
    SyntaxGroup("clighterTemplateTypeParamRef",
        cindex.CursorKind.TYPE_REF, cindex.CursorKind.TEMPLATE_TYPE_PARAMETER),
    SyntaxGroup("clighterOtherTypeRef", cindex.CursorKind.TYPE_REF),

    SyntaxGroup("clighterEnumConstantDecl", cindex.CursorKind.ENUM_CONSTANT_DECL),
    SyntaxGroup("clighterEnumConstantRef",
        cindex.CursorKind.DECL_REF_EXPR, cindex.CursorKind.ENUM_CONSTANT_DECL),

    SyntaxGroup("clighterTemplateTypeParamDecl", cindex.CursorKind.TEMPLATE_TYPE_PARAMETER),
    SyntaxGroup("clighterTemplateTypeParamDecl", cindex.CursorKind.TEMPLATE_TEMPLATE_PARAMETER),
    SyntaxGroup("clighterTemplateTypeParamRef",
        cindex.CursorKind.TEMPLATE_REF, cindex.CursorKind.TEMPLATE_TEMPLATE_PARAMETER),

    SyntaxGroup("clighterTemplateNonTypeParamDecl", cindex.CursorKind.TEMPLATE_NON_TYPE_PARAMETER),
    SyntaxGroup("clighterTemplateNonTypeParamRef",
        cindex.CursorKind.DECL_REF_EXPR, cindex.CursorKind.TEMPLATE_NON_TYPE_PARAMETER),

    SyntaxGroup("clighterClassTemplateDecl", cindex.CursorKind.CLASS_TEMPLATE),
    SyntaxGroup("clighterClassTemplateRef",
        cindex.CursorKind.TEMPLATE_REF, cindex.CursorKind.CLASS_TEMPLATE),

    SyntaxGroup("clighterClassTemplatePartialSpecDecl",
        cindex.CursorKind.CLASS_TEMPLATE_PARTIAL_SPECIALIZATION),
    SyntaxGroup("clighterClassTemplatePartialSpecRef",
        cindex.CursorKind.TEMPLATE_REF, cindex.CursorKind.CLASS_TEMPLATE_PARTIAL_SPECIALIZATION),

    SyntaxGroup("clighterFunctionTemplateDecl",
        cindex.CursorKind.FUNCTION_TEMPLATE, cindex.CursorKind.FUNCTION_DECL),
    SyntaxGroup("clighterMethodTemplateDecl",
        cindex.CursorKind.FUNCTION_TEMPLATE, cindex.CursorKind.CXX_METHOD),
    SyntaxGroup("clighterConstructorTemplateDecl",
        cindex.CursorKind.FUNCTION_TEMPLATE, cindex.CursorKind.CONSTRUCTOR),

    SyntaxGroup("clighterFunctionTemplateRef",
        cindex.CursorKind.TEMPLATE_REF, cindex.CursorKind.FUNCTION_TEMPLATE),

    SyntaxGroup("clighterMethodDecl", cindex.CursorKind.CXX_METHOD),
    SyntaxGroup("clighterMethodRef", cindex.CursorKind.MEMBER_REF, cindex.CursorKind.CXX_METHOD),
    SyntaxGroup("clighterMethodRef",
            cindex.CursorKind.MEMBER_REF_EXPR, cindex.CursorKind.CXX_METHOD),
    SyntaxGroup("clighterMethodRef", cindex.CursorKind.DECL_REF_EXPR, cindex.CursorKind.CXX_METHOD),

    SyntaxGroup("clighterConstructorDecl", cindex.CursorKind.CONSTRUCTOR),
    SyntaxGroup("clighterConstructorRef",
            cindex.CursorKind.MEMBER_REF, cindex.CursorKind.CONSTRUCTOR),
    SyntaxGroup("clighterConstructorRef",
            cindex.CursorKind.MEMBER_REF_EXPR, cindex.CursorKind.CONSTRUCTOR),
    SyntaxGroup("clighterConstructorRef",
            cindex.CursorKind.CALL_EXPR, cindex.CursorKind.CONSTRUCTOR),

    SyntaxGroup("clighterDtorDecl", cindex.CursorKind.DESTRUCTOR),
    SyntaxGroup("clighterDtorRef", cindex.CursorKind.MEMBER_REF, cindex.CursorKind.DESTRUCTOR),
    SyntaxGroup("clighterDtorRef", cindex.CursorKind.MEMBER_REF_EXPR, cindex.CursorKind.DESTRUCTOR),

    SyntaxGroup("clighterDataMemberDecl", cindex.CursorKind.FIELD_DECL),
    SyntaxGroup("clighterDataMemberRef", cindex.CursorKind.MEMBER_REF),
    SyntaxGroup("clighterDataMemberRef", cindex.CursorKind.MEMBER_REF_EXPR),

    SyntaxGroup("clighterFunctionDecl", cindex.CursorKind.FUNCTION_DECL),
    SyntaxGroup("clighterFunctionRef",
        cindex.CursorKind.DECL_REF_EXPR, cindex.CursorKind.FUNCTION_DECL),

    SyntaxGroup("clighterParamDecl", cindex.CursorKind.PARM_DECL),
    SyntaxGroup("clighterParamRef", cindex.CursorKind.DECL_REF_EXPR, cindex.CursorKind.PARM_DECL),

    SyntaxGroup("clighterVarDecl", cindex.CursorKind.VAR_DECL),
    SyntaxGroup("clighterVarRef", cindex.CursorKind.DECL_REF_EXPR, cindex.CursorKind.VAR_DECL),
]

CUSTOM_SYNTAX_GROUP = {
    cindex.CursorKind.INCLUSION_DIRECTIVE: 'clighterInclusionDirective',
    cindex.CursorKind.MACRO_INSTANTIATION: 'clighterMacroInstantiation',
    cindex.CursorKind.VAR_DECL: 'clighterVarDecl',
    cindex.CursorKind.STRUCT_DECL: 'clighterStructDecl',
    cindex.CursorKind.UNION_DECL: 'clighterUnionDecl',
    cindex.CursorKind.CLASS_DECL: 'clighterClassDecl',
    cindex.CursorKind.ENUM_DECL: 'clighterEnumDecl',
    cindex.CursorKind.PARM_DECL: 'clighterParmDecl',
    cindex.CursorKind.FUNCTION_DECL: 'clighterFunctionDecl',
    cindex.CursorKind.FUNCTION_TEMPLATE: 'clighterFunctionDecl',
    cindex.CursorKind.CXX_METHOD: 'clighterFunctionDecl',
    cindex.CursorKind.CONSTRUCTOR: 'clighterFunctionDecl',
    cindex.CursorKind.DESTRUCTOR: 'clighterFunctionDecl',
    cindex.CursorKind.FIELD_DECL: 'clighterFieldDecl',
    cindex.CursorKind.ENUM_CONSTANT_DECL: 'clighterEnumConstantDecl',
    cindex.CursorKind.NAMESPACE: 'clighterNamespace',
    cindex.CursorKind.CLASS_TEMPLATE: 'clighterClassDecl',
    cindex.CursorKind.TEMPLATE_TYPE_PARAMETER: 'clighterTemplateTypeParameter',
    cindex.CursorKind.TEMPLATE_NON_TYPE_PARAMETER: 'clighterTemplateNoneTypeParameter',
    cindex.CursorKind.TYPE_REF: 'clighterTypeRef',  # class ref
    cindex.CursorKind.NAMESPACE_REF: 'clighterNamespaceRef',  # namespace ref
    cindex.CursorKind.TEMPLATE_REF: 'clighterTemplateRef',  # template class ref
    cindex.CursorKind.DECL_REF_EXPR:
    {
        cindex.TypeKind.FUNCTIONPROTO: 'clighterDeclRefExprCall',  # function call
        cindex.TypeKind.ENUM: 'clighterDeclRefExprEnum',  # enum ref
        cindex.TypeKind.TYPEDEF: 'clighterTypeRef',  # ex: cout
    },
    cindex.CursorKind.MEMBER_REF: 'clighterDeclRefExprCall',  # ex: designated initializer
    cindex.CursorKind.MEMBER_REF_EXPR:
    {
        cindex.TypeKind.UNEXPOSED: 'clighterMemberRefExprCall',  # member function call
    },
}


def clear_all():
    __vim_clear_match_pri(OCCURRENCES_PRI, SYNTAX_PRI)
    hl_window.symbol = None
    vim.current.window.vars['clighter_hl'] = [
        -1, [], []]  # [hl_tick, syntax_range, occurrences_range]


def clear_occurrences():
    __vim_clear_match_pri(OCCURRENCES_PRI)
    vim.current.window.vars['clighter_hl'][2] = []
    hl_window.symbol = None


def config_win_context(init):
    if not init and 'clighter_hl' in vim.current.window.vars:
        return

    clear_all()
    vim.current.window.vars['clighter_hl'] = [
        -1, [], []]  # [hl_tick, syntax_range, symbol_range]


def hl_window(clang_service, do_occurrences):
    cc = clang_service.get_cc(vim.current.buffer.name)
    if not cc:
        return

    parse_tick = cc.parse_tick

    tu = cc.current_tu
    if not tu:
        return

    top = string.atoi(vim.eval("line('w0')"))
    bottom = string.atoi(vim.eval("line('w$')"))
    height = bottom - top + 1

    symbol = None

    if vim.eval('g:ClighterOccurrences') == '1':
        vim_cursor = clighter_helper.get_vim_cursor(tu)
        symbol = clighter_helper.get_vim_symbol(vim_cursor)

    occurrences_range = w_range = [top, bottom]
    syntax_range = [max(top - height, 1), min(
        bottom + height, len(vim.current.buffer))]

    config_win_context(False)

    if vim.current.window.vars['clighter_hl'][0] < parse_tick:
        clear_all()
    else:
        if not __is_subrange(
            w_range, list(
                vim.current.window.vars['clighter_hl'][1])):
            __vim_clear_match_pri(SYNTAX_PRI)
        else:
            syntax_range = None

        if not __is_subrange(
            w_range, list(
                vim.current.window.vars['clighter_hl'][2])) or (
            hl_window.symbol and (
                not symbol or symbol != hl_window.symbol)):
            clear_occurrences()
        else:
            occurrences_range = None

    if not do_occurrences:
        occurrences_range = None

    hl_window.symbol = symbol

    __do_highlight(
        tu,
        vim.current.buffer.name,
        syntax_range,
        occurrences_range,
        parse_tick)


def __do_highlight(tu, file_name, syntax_range, occurrences_range, tick):
    file = tu.get_file(file_name)

    if not syntax_range and (not hl_window.symbol or not occurrences_range):
        return

    if syntax_range:
        vim.current.window.vars['clighter_hl'][1] = syntax_range

    if occurrences_range and hl_window.symbol:
        vim.current.window.vars['clighter_hl'][2] = occurrences_range

    union_range = __union(syntax_range, occurrences_range)

    location1 = cindex.SourceLocation.from_position(
        tu, file, line=union_range[0], column=1)
    location2 = cindex.SourceLocation.from_position(
        tu, file, line=union_range[1] + 1, column=1)
    tokens = tu.get_tokens(
        extent=cindex.SourceRange.from_locations(
            location1,
            location2))

    syntax = {}
    occurrence = {'clighterOccurrences':[]}
    for token in tokens:
        if (token.kind == cindex.TokenKind.IDENTIFIER) or \
           (token.kind == cindex.TokenKind.KEYWORD and token.spelling == "operator") or \
           (token.kind == cindex.TokenKind.PUNCTUATION and \
                   (token.cursor.kind in [cindex.CursorKind.FUNCTION_DECL,
                                          cindex.CursorKind.DECL_REF_EXPR,
                                          cindex.CursorKind.CXX_METHOD,
                                          cindex.CursorKind.MEMBER_REF_EXPR,
                                          ])):
            pass
        else:
            continue

        t_cursor = token.cursor
        t_cursor._tu = tu

        # t_cursor = cindex.Cursor.from_location(
            # tu,
            # cindex.SourceLocation.from_position(
                # tu, file,
                # token.location.line,
                # token.location.column
            # )
        # )

        pos = [token.location.line, token.location.column, len( token.spelling)]

        if __is_in_range(token.location.line, syntax_range):
            group = __get_syntax_group(t_cursor)
            if group:
                if not syntax.has_key(group):
                    syntax[group] = []

                syntax[group].append(pos)

        if hl_window.symbol and __is_in_range(token.location.line, occurrences_range):
            t_symbol = clighter_helper.get_semantic_symbol(t_cursor)
            if t_symbol and token.spelling == t_symbol.spelling and t_symbol == hl_window.symbol:
                occurrence['clighterOccurrences'].append(pos)

    cmd = "call MatchIt({0}, {1})".format(syntax, SYNTAX_PRI)
    vim.command(cmd)

    cmd = "call MatchIt({0}, {1})".format(occurrence , OCCURRENCES_PRI)
    vim.command(cmd)

    vim.current.window.vars['clighter_hl'][0] = tick


def __get_default_syn(cursor_kind):
    if cursor_kind.is_preprocessing():
        return 'clighterPrepro'
    elif cursor_kind.is_declaration():
        return 'clighterDecl'
    elif cursor_kind.is_reference():
        return 'clighterRef'
    else:
        return None


def get_type_decl(cursor):
    """
    returns the cursor to the declaration of the type
    referenced by @cursor
    recurse into typedefs and using aliases
    """
    decl = cursor.get_definition()

    while decl.kind == cindex.CursorKind.TYPEDEF_DECL or \
            decl.kind == cindex.CursorKind.TYPE_ALIAS_DECL:
        decl = decl.underlying_typedef_type.get_declaration()

    return decl

def get_template_kind(cursor):
    """
    Given a cursor that represents a template,
    returns the cursor kind of the specializations would be generated by instantiating the template.
    or None
    """
    tk = cindex.conf.lib.clang_getTemplateCursorKind(cursor)
    template_kind = cindex.CursorKind.from_id(tk)

    return template_kind if template_kind != cindex.CursorKind.NO_DECL_FOUND else None

def __get_syntax_group(cursor):

    decl = get_type_decl(cursor) if cursor.kind == cindex.CursorKind.TYPE_REF else cursor.referenced
    decl_kind = decl.kind if decl else None
    template_kind = get_template_kind(cursor)

    secondary_kind = template_kind if template_kind is not None else decl_kind

    for syntax_groups in SYNTAX_GROUPS:
        if syntax_groups.isMatch(cursor.kind, secondary_kind):
            return syntax_groups.group_name

    return None

    group = __get_default_syn(cursor_kind)

    custom = CUSTOM_SYNTAX_GROUP.get(cursor_kind)
    if custom:
        if cursor_kind == cindex.CursorKind.DECL_REF_EXPR:
            custom = custom.get(type_kind)
            if custom:
                group = custom
        elif cursor_kind == cursor_kind == cindex.CursorKind.MEMBER_REF_EXPR:
            custom = custom.get(type_kind)
            if custom:
                group = custom
            else:
                group = 'clighterMemberRefExprVar'
        else:
            group = custom

    if group in vim.eval('g:clighter_highlight_blacklist'):
        return None

    return group


def __vim_clear_match_pri(*priorities):
    cmd = "call s:clear_match_pri({0})".format(list(priorities))
    vim.command(cmd)


def __union(range1, range2):
    if range1 and range2:
        return [min(range1[0], range2[0]), max(range1[1], range2[1])]
    elif range1 and not range2:
        return range1
    elif not range1 and range2:
        return range2
    else:
        return None


def __is_in_range(value, range):
    if not range:
        return False

    if value >= range[0] and value <= range[1]:
        return True

    return False


def __is_subrange(inner, outer):
    if not inner:
        return True

    if not outer:
        return False

    if inner[0] < outer[0]:
        return False

    if inner[1] > outer[1]:
        return False

    return True
