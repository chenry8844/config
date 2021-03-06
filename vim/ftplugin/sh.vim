" Vim filetype plugin file
" Language:	sh
" Maintainer:	Dan Sharp <dwsharp at users dot sourceforge dot net>
" Last Changed: 20 Jan 2009
" URL:		http://dwsharp.users.sourceforge.net/vim/ftplugin

if exists("b:did_ftplugin") | finish | endif
let b:did_ftplugin = 1

" Make sure the continuation lines below do not cause problems in
" compatibility mode.
let s:save_cpo = &cpo
set cpo-=C

setlocal commentstring=#%s

" indent setting
" ==============
" Reference: http://henry.precheur.org/vim/python
" With "setlocal" only the local value is changed, thus this value is not 
" used when editing a new buffer.

" a four-space tab indent width is the prefered coding style for python.
setlocal tabstop=4

" amount of spaces you want for a deeper level
" And this allows you to use the < and > keys from visual mode to block
" indent/unindent regions
setlocal shiftwidth=4

" Insert spaces instead of <TAB> character when the <TAB> key is pressed.
setlocal expandtab

" make VIM see multiple space characters as tabstops.
" it makes it easier when pressing BACKSPACE or DELETE.
setlocal softtabstop=4

" default is empty
" Make backspace delete lots of things. 
setlocal backspace=indent,eol,start

" show print margin
setlocal colorcolumn=79

" 自动换行是每行超过 n 个字的时候 vim 自动加上换行符
" 需要注意的是，如果一个段落的首个单词很长，超出了自动换行设置的字符，
" 这种情况下不会换行。
" 于是，中文就悲剧了，因为中文中很少出现空格，字之间没有，句子之间也没有。
" 于是不会触发自动换行的处理。
" 对已经存在的文本，不做自动换行处理，只有新输入文本的才会触发。
" 如要对已存在的文本应用自动换行，只要选中它们，然后按gq就可以了。
setlocal textwidth=78
" 上面所说的中文不能自动换行的问题，可以通过下面的配置解决.
" m   Also break at a multi-byte character above 255.  This is useful for    
"     Asian text where every character is a word on its own.                 
" M   When joining lines, don't insert a space before or after a
"     multi-byte  character.  Overrules the 'B' flag.
setlocal formatoptions+=mM

" Shell:  thanks to Johannes Zellner
if exists("loaded_matchit")
    let s:sol = '\%(;\s*\|^\s*\)\@<='  " start of line
    let b:match_words =
    \ s:sol.'if\>:' . s:sol.'elif\>:' . s:sol.'else\>:' . s:sol. 'fi\>,' .
    \ s:sol.'\%(for\|while\)\>:' . s:sol. 'done\>,' .
    \ s:sol.'case\>:' . s:sol. 'esac\>'
endif

" Change the :browse e filter to primarily show shell-related files.
if has("gui_win32")
    let  b:browsefilter="Bourne Shell Scripts (*.sh)\t*.sh\n" .
		\	"Korn Shell Scripts (*.ksh)\t*.ksh\n" .
		\	"Bash Shell Scripts (*.bash)\t*.bash\n" .
		\	"All Files (*.*)\t*.*\n"
endif

" Undo the stuff we changed.
let b:undo_ftplugin = "setlocal cms< | unlet! b:browsefilter b:match_words"

" Restore the saved compatibility options.
let &cpo = s:save_cpo
unlet s:save_cpo
