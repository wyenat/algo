    .text

/*
void echanger(int64_t tab[], int64_t i, int64_t j)
{
    int64_t tmp;
    tmp = tab[i];
    tab[i] = tab[j];
    tab[j] = tmp;
}
*/
    .globl echanger
echanger:
#_DEBUT_PROF_
    # tab : %rdi
    # i : %rsi
    # j : %rdx
    # uint64_t tmp : 8 octets, %rbp - 16
    enter $16, $0
    # tmp = tab[i];
    movq (%rdi, %rsi, 8), %rax
    movq %rax, -16(%rbp)
    # tab[i] = tab[j];
    movq (%rdi, %rdx, 8), %rax
    movq %rax, (%rdi, %rsi, 8)
    # tab[j] = tmp;
    movq -16(%rbp), %rax
    movq %rax, (%rdi, %rdx, 8)
    leave
#_FIN_PROF_
    ret

/*
void placer_pivot(int64_t tab[], uint64_t cour, uint64_t *prem, uint64_t *der)
{
    int64_t val_pivot = tab[cour];
    val_pivot = tab[cour];
    *prem = 0;
    *der = 0;
    echanger(tab, cour, *prem);
    while (cour > *der) {
        if (tab[cour] < val_pivot) {
            echanger(tab, cour, *prem);
            (*prem)++;
            (*der)++;
            echanger(tab, cour, *der);
        } else if (val_pivot < tab[cour]) {
            cour--;
        } else {
            (*der)++;
            echanger(tab, cour, *der);
        }
    }
}
*/
    .globl placer_pivot
placer_pivot:
#_DEBUT_PROF_
    # tab : %rdi
    # cour : %rsi
    # prem : %rdx
    # der : %rcx
    # int64_t val_pivot : 8 octets, %rbp - 8
    # sauvegarde de prem : %rbp - 16
    # on devrait sauvegarder les autres parametres, mais comme
    #   on a ecrit la fonction appelee, et qu'on sait qu'elle ne
    #   les modifie pas, on peut accepter l'optimisation
    enter $16, $0
    # val_pivot = tab[cour];
    movq (%rdi, %rsi, 8), %rax
    movq %rax, -8(%rbp)
    # *prem = 0;
    movq $0, (%rdx)
    # *der = 0;
    movq $0, (%rcx)
    # echanger(tab, cour, *prem);
    movq %rdx, -16(%rbp)
    movq (%rdx), %rdx
    call echanger
    movq -16(%rbp), %rdx
while:
    # while (cour > *der) {
    cmpq %rsi, (%rcx)
    jae fin_while
    ## if (tab[cour] < val_pivot) {
    movq -8(%rbp), %rax
    cmpq (%rdi, %rsi, 8), %rax
    jl piv_inf
    je piv_egal
    # echanger(tab, cour, *prem);
    movq %rdx, -16(%rbp)
    movq (%rdx), %rdx
    call echanger
    movq -16(%rbp), %rdx
    # (*prem)++;
    addq $1, (%rdx)
    # (*der)++;
    addq $1, (%rcx)
    # echanger(tab, cour, *der);
    movq %rdx, -16(%rbp)
    movq (%rcx), %rdx
    call echanger
    movq -16(%rbp), %rdx
    jmp fin_if
    # } else if (val_pivot < tab[cour]) {
piv_inf:
    # cour--;
    subq $1, %rsi
    jmp fin_if
    # } else {
piv_egal:
    # (*der)++;
    addq $1, (%rcx)
    # echanger(tab, cour, *der);
    movq %rdx, -16(%rbp)
    movq (%rcx), %rdx
    call echanger
    movq -16(%rbp), %rdx
fin_if:
    jmp while
fin_while:
    leave
#_FIN_PROF_
    ret

/*
void tab_vers_liste(int64_t tab[], uint64_t taille, struct cell_t **liste)
{
    *liste = NULL;
    for (uint64_t i = 0; i < taille; i++) {
        struct cell_t *cell = malloc(sizeof(struct cell_t));
        cell->val = tab[taille - i - 1];
        cell->suiv = *liste;
        *liste = cell;
    }
}
*/

    .globl tab_vers_liste
tab_vers_liste:
#_DEBUT_PROF_
    # tab : %rdi
    # taille : %rsi
    # liste : %rdx
    # i : 8 octets, %rbp - 16
    # cell : 8 octets, %rbp - 8
    # sauvegarde des 3 parametres : 3 * 8 octets
    enter $48, $0
    # *liste = NULL;
    movq $0, (%rdx)
    # for (uint64_t i = 0;
    movq $0, -16(%rbp)
for:
    # i < taille;
    cmpq -16(%rbp), %rsi
    jbe fin_for
    # struct cell_t *cell = malloc(sizeof(struct cell_t));
    movq %rdi, -48(%rbp)
    movq %rsi, -40(%rbp)
    movq %rdx, -32(%rbp)
    movq $16, %rdi
    call malloc
    movq %rax, -8(%rbp)
    movq -48(%rbp), %rdi
    movq -40(%rbp), %rsi
    movq -32(%rbp), %rdx
    # cell->val = tab[taille - i - 1];
    movq %rsi, %r10
    subq -16(%rbp), %r10
    subq $1, %r10
    movq (%rdi, %r10, 8), %r10
    movq -8(%rbp), %rax
    movq %r10, (%rax)
    # cell->suiv = *liste;
    movq (%rdx), %rax
    movq -8(%rbp), %r10
    movq %rax, 8(%r10)
    # *liste = cell;
    movq -8(%rbp), %rax
    movq %rax, (%rdx)
    # i++) {
    addq $1, -16(%rbp)
    jmp for
fin_for:
    leave
#_FIN_PROF_
    ret

