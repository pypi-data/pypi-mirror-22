_bmcs_completion() {
    COMPREPLY=( $( env COMP_WORDS="${COMP_WORDS[*]}" \
                   COMP_CWORD=$COMP_CWORD \
                   _BMCS_COMPLETE=complete $1 ) )
    return 0
}

complete -F _bmcs_completion -o default bmcs;