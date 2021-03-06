py import vim
let s:script_folder_path = escape( expand( '<sfile>:p:h' ), '\' )
py import vim
py import sys
exe 'python sys.path = sys.path + ["' . s:script_folder_path . '/../misc"]'
py import clighter
py import highlighting
py import clang_service
py import refactor
py import compilation_flags

if !empty(g:clighter_libclang_file)
    exe 'python clang_service.ClangService.set_library_file("'.g:clighter_libclang_file.'")'
endif

let s:clighter_enabled=0
execute('source '. s:script_folder_path . '/../after/syntax/clighter.vim')

fun! clighter#ToggleOccurrences()
    if g:ClighterOccurrences==1
        let a:wnr = winnr()
        windo py highlighting.clear_occurrences()
        exe a:wnr.'wincmd w'
    endif

    let g:ClighterOccurrences = !g:ClighterOccurrences

    echohl WarningMsg |
                \echom printf('Cursor Occurrences: %s', g:ClighterOccurrences ? 'Enabled' : 'Disabled') |
                \echohl None
endf

fun! s:clear_match_grp(groups)
    for m in getmatches()
        if index(a:groups, m['group']) >= 0
            call matchdelete(m['id'])
        endif
    endfor
endf

fun! s:clear_match_pri(pri)
    for m in getmatches()
        if index(a:pri, m['priority']) >= 0
            call matchdelete(m['id'])
        endif
    endfor
endf

fun! clighter#Enable()
    silent! au! ClighterAutoStart

    if s:clighter_enabled
        return
    endif

    let a:cwd = getcwd()
    if !filereadable(a:cwd.'/compile_commands.json')
        let a:cwd = ''
    endif

    let a:compile_args = pyeval("compilation_flags.get()")

    let a:start_cmd = printf("clang_service.ClangService().start('%s', %d, %s)", a:cwd, g:clighter_heuristic_compile_args, a:compile_args)

    if !pyeval(a:start_cmd)
        echohl WarningMsg |
                    \ echomsg 'Clighter unavailable: clang service failed, you must setup clang environment for clighter' |
                    \ echohl None
        return
    endif

    py clighter.register_allowed_buffers()
    py clang_service.ClangService().switch(vim.current.buffer.name)

    augroup ClighterEnable
        au!
        au BufWinEnter * py highlighting.config_win_context(True)
        if g:clighter_highlight_mode == 1
            if !g:clighter_occurrences_mode
                au CursorMoved,CursorMovedI * py highlighting.hl_window(clang_service.ClangService(), False)
            else
                au CursorMoved,CursorMovedI * py highlighting.hl_window(clang_service.ClangService(), True)
            endif
        endif
        au CursorHold,CursorHoldI * py highlighting.hl_window(clang_service.ClangService(), True)
        au TextChanged,TextChangedI * py clighter.update_buffer_if_allow()
        au BufEnter * py clighter.clang_service.ClangService().switch(vim.current.buffer.name)
        au FileType * py clighter.on_filetype()
        au BufDelete,BufWipeout * exe 'py clang_service.ClangService().unregister("'. substitute(fnamemodify(expand("<afile>"), ":p"), '\', '/', 'g') . '")'
        au VimLeavePre * py clang_service.ClangService().stop()
    augroup END

    let s:clighter_enabled=1
endf

fun! clighter#Disable()
    silent! au! ClighterEnable
    py clang_service.ClangService().stop()
    let s:clighter_enabled=0
    let a:wnr = winnr()
    windo py highlighting.clear_all()
    exe a:wnr.'wincmd w'
endf

fun! clighter#Rename()
    py refactor.rename(clang_service.ClangService())
endf

fun! clighter#ShowInfo()
    py clighter.show_information()
endf
